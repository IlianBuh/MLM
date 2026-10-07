# %% [markdown]
# # Сбор и подготовка данных: датасет scrap_price (цены автомобилей)
# Шаги: 1) импорт, 2) пропуски и выбросы, 3) новые признаки и кодирование, 4) масштабирование.

# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler

sns.set_theme(style="whitegrid")
CSV_PATH = "scrap_price.csv"   # путь к файлу
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)


def save_show(name):
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/{name}.png", dpi=110)
    plt.show()


# %% [markdown]
# ## 1. Импорт датасета

# %%
df = pd.read_csv(CSV_PATH)
print("Размер:", df.shape)
print(df.head())
print(df.info())

# %%
# ID — служебный столбец, для анализа не нужен
df = df.drop(columns=["ID"])
print("Полных дубликатов строк:", df.duplicated().sum())

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()
print("Числовые:", num_cols)
print("Категориальные:", cat_cols)

# %% [markdown]
# ## 2. Пропуски и аномальные значения
# ### 2.1 Пропуски

# %%
missing = df.isna().sum()
print(missing[missing > 0] if missing.sum() else "Пропусков не обнаружено")

plt.figure(figsize=(12, 4))
sns.heatmap(df.isna(), cbar=False, yticklabels=False, cmap="viridis")
plt.title("Карта пропусков (жёлтый = пропуск) — ДО обработки")
save_show("01_missing_before")

# %%
# Универсальное заполнение (сработает, если в данных появятся пропуски):
# числовые — медианой, категориальные — модой
for c in num_cols:
    if df[c].isna().any():
        df[c] = df[c].fillna(df[c].median())
for c in cat_cols:
    if df[c].isna().any():
        df[c] = df[c].fillna(df[c].mode()[0])
print("Пропусков после заполнения:", int(df.isna().sum().sum()))

# %% [markdown]
# ### 2.2 Выбросы: описательная статистика, распределения, boxplot

# %%
print(df[num_cols].describe().T)
print("\nАсимметрия:\n", df[num_cols].skew().round(2))

# %%
plot_cols = [c for c in num_cols if c != "symboling"]
n = len(plot_cols)
ncols = 4
nrows = int(np.ceil(n / ncols))

fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.2 * nrows))
for ax, c in zip(axes.ravel(), plot_cols):
    sns.histplot(df[c], kde=True, ax=ax)
    ax.set_title(c)
for ax in axes.ravel()[n:]:
    ax.axis("off")
fig.suptitle("Распределения числовых признаков — ДО обработки выбросов", y=1.01)
save_show("02_hist_before")

# %%
def boxplots(data, title, fname):
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.2 * nrows))
    for ax, c in zip(axes.ravel(), plot_cols):
        sns.boxplot(x=data[c], ax=ax, color="lightsteelblue")
        ax.set_title(c)
        ax.set_xlabel("")
    for ax in axes.ravel()[n:]:
        ax.axis("off")
    fig.suptitle(title, y=1.01)
    save_show(fname)


boxplots(df, "BoxPlot — ДО обработки выбросов", "03_box_before")

# %%
# Статистический метод: правило межквартильного размаха (IQR)
def iqr_bounds(s, k=1.5):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def outlier_report(data):
    rows = []
    for c in plot_cols:
        lo, hi = iqr_bounds(data[c])
        cnt = int(((data[c] < lo) | (data[c] > hi)).sum())
        rows.append((c, round(lo, 2), round(hi, 2), cnt))
    return pd.DataFrame(rows, columns=["признак", "нижняя граница", "верхняя граница", "выбросов"])


print(outlier_report(df).to_string(index=False))

# Дополнительно: z-score (|z|>3)
z = (df[plot_cols] - df[plot_cols].mean()) / df[plot_cols].std()
print("\nВыбросы по z-score (|z|>3):")
print((z.abs() > 3).sum()[lambda s: s > 0])

# %%
# Устранение: винзоризация (обрезка значений по границам IQR).
# Строки не удаляем — выборка маленькая (205 записей).
# Повторяем, пока по пересчитанным границам выбросов не останется.
df_raw = df.copy()
for it in range(10):
    changed = 0
    for c in plot_cols:
        lo, hi = iqr_bounds(df[c])
        clipped = df[c].clip(lo, hi)
        changed += int((clipped != df[c]).sum())
        df[c] = clipped
    print(f"Итерация {it + 1}: изменено значений = {changed}")
    if changed == 0:
        break

# %%
# Проверка графиками и таблицей
print(outlier_report(df).to_string(index=False))
assert outlier_report(df)["выбросов"].sum() == 0

boxplots(df, "BoxPlot — ПОСЛЕ обработки выбросов", "04_box_after")

fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.2 * nrows))
for ax, c in zip(axes.ravel(), plot_cols):
    sns.histplot(df[c], kde=True, ax=ax, color="seagreen")
    ax.set_title(c)
for ax in axes.ravel()[n:]:
    ax.axis("off")
fig.suptitle("Распределения — ПОСЛЕ обработки выбросов", y=1.01)
save_show("05_hist_after")

plt.figure(figsize=(12, 4))
sns.heatmap(df.isna(), cbar=False, yticklabels=False, cmap="viridis")
plt.title("Карта пропусков — ПОСЛЕ обработки (пропусков нет)")
save_show("06_missing_after")

# %% [markdown]
# ## 3. Новые признаки и кодирование категориальных
# ### 3.1 Очистка категорий и генерация признаков

# %%
# Бренд из названия + исправление опечаток в исходных данных
df["brand"] = df["name"].str.split().str[0].str.lower().replace({
    "maxda": "mazda", "porcshce": "porsche", "toyouta": "toyota",
    "vokswagen": "volkswagen", "vw": "volkswagen",
})
print(df["brand"].value_counts())

# Новые числовые признаки
df["power_to_weight"] = df["horsepower"] / df["curbweight"]                   # л.с. на фунт массы
df["avg_mpg"] = 0.55 * df["citympg"] + 0.45 * df["highwaympg"]                # комбинированный расход
df["car_volume"] = df["carlength"] * df["carwidth"] * df["carheight"] / 1e6   # габаритный объём
df["engine_per_weight"] = df["enginesize"] / df["curbweight"]                 # литраж на массу

# Порядковое кодирование числа цилиндров (слова -> числа)
cyl_map = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "eight": 8, "twelve": 12}
df["cylinders"] = df["cylindernumber"].map(cyl_map)

# Бинаризация
df["is_gas"] = (df["fueltypes"] == "gas").astype(int)
df["is_turbo"] = (df["aspiration"] == "turbo").astype(int)
df["is_four_door"] = (df["doornumbers"] == "four").astype(int)
df["engine_rear"] = (df["enginelocation"] == "rear").astype(int)
df["risky"] = (df["symboling"] > 0).astype(int)     # symboling>0 — страховщик считает авто более рискованным
df["premium_brand"] = df["brand"].isin(["bmw", "jaguar", "porsche", "audi", "volvo", "saab", "mercedes-benz"]).astype(int)

# %% [markdown]
# ### 3.2 One-Hot Encoding

# %%
ohe_cols = ["carbody", "drivewheels", "enginetype", "fuelsystem", "brand"]
df_enc = pd.get_dummies(df, columns=ohe_cols, drop_first=False, dtype=int)

# Удаляем исходные текстовые столбцы, заменённые закодированными
df_enc = df_enc.drop(columns=["name", "fueltypes", "aspiration", "doornumbers",
                              "enginelocation", "cylindernumber"])
print("Размер после кодирования:", df_enc.shape)
print(df_enc.dtypes.value_counts())

# Проверка: все столбцы числовые, пропусков нет
assert all(pd.api.types.is_numeric_dtype(t) for t in df_enc.dtypes)
assert df_enc.isna().sum().sum() == 0

# %%
# Тепловая карта корреляций для числовых признаков
corr_cols = plot_cols + ["power_to_weight", "avg_mpg", "car_volume", "engine_per_weight",
                         "cylinders", "is_turbo"]
plt.figure(figsize=(13, 10))
sns.heatmap(df_enc[corr_cols].corr(), annot=True, fmt=".1f", cmap="coolwarm",
            center=0, annot_kws={"size": 7})
plt.title("Корреляции (включая новые признаки)")
save_show("07_corr_heatmap")

# %% [markdown]
# ## 4. Стандартизация и нормализация
# Масштабируем только непрерывные признаки; бинарные и OHE-столбцы оставляем как есть.
# Целевую переменную `price` не стандартизируем вместе с признаками.

# %%
binary_like = [c for c in df_enc.columns
               if df_enc[c].nunique() <= 2 and set(df_enc[c].unique()) <= {0, 1}]
cont_cols = [c for c in df_enc.columns
             if c not in binary_like and c != "price"]
print("Масштабируем:", cont_cols)

# Стандартизация: (x - mean) / std
df_std = df_enc.copy()
df_std[cont_cols] = StandardScaler().fit_transform(df_enc[cont_cols])

# Нормализация Min-Max в [0, 1]
df_mm = df_enc.copy()
df_mm[cont_cols] = MinMaxScaler().fit_transform(df_enc[cont_cols])

print("\nСтандартизация: mean≈0, std≈1")
print(df_std[cont_cols].agg(["mean", "std"]).T.round(3).head(8))
print("\nMin-Max: min=0, max=1")
print(df_mm[cont_cols].agg(["min", "max"]).T.round(3).head(8))

# %%
# Сравнение до / после на примере нескольких признаков
show = ["curbweight", "horsepower", "power_to_weight", "avg_mpg"]
fig, axes = plt.subplots(3, len(show), figsize=(15, 8))
for j, c in enumerate(show):
    sns.histplot(df_enc[c], kde=True, ax=axes[0, j]);  axes[0, j].set_title(f"{c}: исходный")
    sns.histplot(df_std[c], kde=True, ax=axes[1, j], color="darkorange"); axes[1, j].set_title("StandardScaler")
    sns.histplot(df_mm[c], kde=True, ax=axes[2, j], color="green"); axes[2, j].set_title("MinMaxScaler")
save_show("08_scaling_compare")

# %%
# Сохранение результатов
df_enc.to_csv(f"{OUT_DIR}/scrap_price_clean_encoded.csv", index=False)
df_std.to_csv(f"{OUT_DIR}/scrap_price_standardized.csv", index=False)
df_mm.to_csv(f"{OUT_DIR}/scrap_price_minmax.csv", index=False)
print("Готово. Файлы сохранены в", OUT_DIR)
