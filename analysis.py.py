
# ============================================================
# FLIPKART DATA ANALYTICS PROJECT
# COMPLETE EDA + DATA CLEANING USING PANDAS
# ============================================================

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("flipkart_data_mysql.csv")

print("\n========== DATASET LOADED ==========")
print("Dataset Loaded Successfully")
print("Original Shape:", df.shape)

# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\n========== FIRST 10 ROWS ==========")
print(df.head(10))

print("\n========== LAST 10 ROWS ==========")
print(df.tail(10))

print("\n========== RANDOM 5 ROWS ==========")
print(df.sample(min(5, len(df))))

print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATASET INFO ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").T)

# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

print("\n========== CLEANED COLUMN NAMES ==========")
print(df.columns.tolist())

# ============================================================
# 4. REMOVE DUPLICATE ROWS
# ============================================================

print("\n========== DUPLICATE CHECK ==========")

duplicates = df.duplicated().sum()

print("Duplicate Rows:", duplicates)

df = df.drop_duplicates()

df = df.reset_index(drop=True)

print("Shape After Removing Duplicates:", df.shape)

# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

print("\n========== MISSING VALUES ==========")

missing_values = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
)

missing_report = pd.DataFrame({
    "Missing_Count": missing_values,
    "Missing_Percentage": missing_percentage
})

print(missing_report.sort_values(
    by="Missing_Percentage",
    ascending=False
))

# ============================================================
# 6. CLEAN TEXT DATA
# ============================================================

print("\n========== TEXT CLEANING ==========")

text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:
    df[col] = df[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# Replace empty strings with NaN
df = df.replace(r"^\s*$", np.nan, regex=True)

print("Text Cleaning Completed")

# ============================================================
# 7. AUTOMATIC DATE COLUMN DETECTION
# ============================================================

print("\n========== DATE CONVERSION ==========")

for col in df.columns:

    if "date" in col or col.endswith("_at"):
        original = df[col].copy()

        converted = pd.to_datetime(
            original,
            format="%d-%m-%Y",
            errors="coerce"
        )

        # Try alternative formats if first format fails
        if converted.notna().sum() == 0:
            converted = pd.to_datetime(
                original,
                format="mixed",
                errors="coerce"
            )

        if converted.notna().sum() > 0:
            df[col] = converted
            print("Converted Date Column:", col)

# ============================================================
# 8. NUMERICAL DATA CLEANING
# ============================================================

print("\n========== NUMERICAL DATA CLEANING ==========")

for col in df.select_dtypes(include="object").columns:

    # Convert numeric-looking columns to numeric
    cleaned = (
        df[col]
        .astype("string")
        .str.replace(r"[₹,%]", "", regex=True)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    numeric = pd.to_numeric(cleaned, errors="coerce")

    # Convert only when most non-empty values are numeric
    original_nonempty = df[col].notna().sum()

    if original_nonempty > 0:
        numeric_ratio = numeric.notna().sum() / original_nonempty

        if numeric_ratio >= 0.90:
            df[col] = numeric

# ============================================================
# 9. HANDLE MISSING VALUES
# ============================================================

print("\n========== HANDLING MISSING VALUES ==========")

# Numerical columns
numeric_columns = df.select_dtypes(
    include=np.number
).columns

# Categorical columns
categorical_columns = df.select_dtypes(
    include=["object", "string"]
).columns

# Fill numeric missing values with median
for col in numeric_columns:

    if df[col].isnull().sum() > 0:

        median_value = df[col].median()

        df[col] = df[col].fillna(median_value)

# Fill categorical missing values
for col in categorical_columns:

    if df[col].isnull().sum() > 0:

        df[col] = df[col].fillna("Unknown")

print("Missing Value Treatment Completed")

print("\nRemaining Missing Values:")
print(df.isnull().sum())

# ============================================================
# 10. SORT DATA BY DATE IN ASCENDING ORDER
# ============================================================

print("\n========== DATE SORTING ==========")

date_columns = df.select_dtypes(
    include=["datetime", "datetimetz"]
).columns

if len(date_columns) > 0:

    date_column = (
        "listing_date"
        if "listing_date" in date_columns
        else date_columns[0]
    )

    df = df.sort_values(
        by=date_column,
        ascending=True,
        na_position="last"
    )

    print("Sorted By:", date_column)
    print("Oldest To Newest")

else:
    print("No Valid Date Column Found")

df = df.reset_index(drop=True)

# ============================================================
# 11. EDA - NUMERICAL ANALYSIS
# ============================================================

print("\n========== NUMERICAL ANALYSIS ==========")

print(df.describe().T)

# ============================================================
# 12. EDA - CATEGORICAL ANALYSIS
# ============================================================

print("\n========== CATEGORICAL ANALYSIS ==========")

for col in df.select_dtypes(
    include=["object", "string"]
).columns:

    print("\nColumn:", col)

    print(df[col].value_counts().head(10))

# ============================================================
# 13. UNIQUE VALUE ANALYSIS
# ============================================================

print("\n========== UNIQUE VALUES ==========")

for col in df.columns:

    print(
        col,
        "Unique Values:",
        df[col].nunique()
    )

# ============================================================
# 14. MISSING VALUE VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 6))

sns.heatmap(
    df.isnull(),
    cbar=False,
    cmap="viridis"
)

plt.title("Missing Values Heatmap")
plt.tight_layout()
plt.show()

# ============================================================
# 15. CORRELATION HEATMAP
# ============================================================

numeric_df = df.select_dtypes(include=np.number)

if numeric_df.shape[1] >= 2:

    plt.figure(figsize=(12, 8))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

# ============================================================
# 16. NUMERICAL DISTRIBUTION
# ============================================================

for col in numeric_columns:

    if col in df.columns:

        plt.figure(figsize=(8, 4))

        sns.histplot(
            df[col].dropna(),
            kde=True,
            bins=30
        )

        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.show()

# ============================================================
# 17. OUTLIER DETECTION USING BOXPLOT
# ============================================================

for col in numeric_columns:

    if col in df.columns and df[col].nunique() > 1:

        plt.figure(figsize=(8, 4))

        sns.boxplot(x=df[col])

        plt.title(f"Outlier Detection - {col}")

        plt.tight_layout()
        plt.show()

# ============================================================
# 18. DATE-WISE PRODUCT LISTING ANALYSIS
# ============================================================

if len(date_columns) > 0:

    date_column = (
        "listing_date"
        if "listing_date" in df.columns
        else date_columns[0]
    )

    date_analysis = (
        df.dropna(subset=[date_column])
        .set_index(date_column)
        .resample("ME")
        .size()
    )

    plt.figure(figsize=(12, 5))

    date_analysis.plot()

    plt.title("Monthly Product Listing Trend")
    plt.xlabel("Date")
    plt.ylabel("Number of Listings")

    plt.tight_layout()
    plt.show()

    print("\nMonthly Listing Analysis:")
    print(date_analysis)

# ============================================================
# 19. TOP 10 CATEGORY ANALYSIS
# ============================================================

category_candidates = [
    col for col in df.columns
    if "category" in col or "brand" in col
]

for col in category_candidates:

    top_values = df[col].value_counts().head(10)

    plt.figure(figsize=(10, 5))

    top_values.plot(kind="bar")

    plt.title(f"Top 10 - {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()

# ============================================================
# 20. FINAL DATASET CHECK
# ============================================================

print("\n========== FINAL DATASET ==========")

print("Final Shape:", df.shape)

print("\nFinal Data Types:")
print(df.dtypes)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Duplicate Rows:")
print(df.duplicated().sum())

print("\nFinal Dataset Preview:")
print(df.head(10))

# ============================================================
# 21. EXPORT CLEANED DATASET
# ============================================================

df.to_csv(
    "flipkart_cleaned_dataset.csv",
    index=False
)

# Export EDA reports
missing_report.to_csv(
    "missing_values_report.csv"
)

df.describe(include="all").T.to_csv(
    "statistical_summary.csv"
)

print("\n========================================")
print("FLIPKART DATA CLEANING COMPLETED")
print("EDA COMPLETED")
print("CLEANED DATASET EXPORTED SUCCESSFULLY")
print("========================================")
