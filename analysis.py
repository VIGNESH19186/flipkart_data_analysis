
# ==============================================================
# FLIPKART DATA ANALYTICS PROJECT
# COMPLETE EDA + DATA CLEANING
# ==============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import glob

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_name = "Flipkart_Normal_Comma_Separated.csv"

file_path = os.path.join(BASE_DIR, file_name)

# If exact filename is not found, search for similar CSV files
if not os.path.exists(file_path):

    csv_files = glob.glob(
        os.path.join(BASE_DIR, "*.csv")
    )

    matching_files = [
        f for f in csv_files
        if "flipkart" in os.path.basename(f).lower()
    ]

    if len(matching_files) == 1:
        file_path = matching_files[0]

    elif len(matching_files) > 1:
        print("Multiple Flipkart CSV files found:")
        for i, f in enumerate(matching_files):
            print(i + 1, os.path.basename(f))

        raise FileNotFoundError(
            "Please keep only the intended CSV file "
            "or specify its exact filename."
        )

    else:
        print("\nCSV files available in project folder:")
        for f in csv_files:
            print(os.path.basename(f))

        raise FileNotFoundError(
            "Flipkart CSV file not found. "
            "Place the dataset inside the same folder as analysis.py."
        )


print("\n========== LOADING DATASET ==========")

df = pd.read_csv(
    file_path,
    encoding="utf-8",
    low_memory=False
)

print("Dataset Loaded Successfully!")
print("File:", os.path.basename(file_path))
print("Original Rows:", df.shape[0])
print("Original Columns:", df.shape[1])



print("\n========== FIRST 10 ROWS ==========")
print(df.head(10))

print("\n========== LAST 10 ROWS ==========")
print(df.tail(10))

print("\n========== RANDOM 5 ROWS ==========")
print(df.sample(min(5, len(df))))

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATASET INFO ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").T)



df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(
        r"[^a-z0-9]+",
        "_",
        regex=True
    )
    .str.strip("_")
)

print("\n========== CLEANED COLUMN NAMES ==========")
print(df.columns.tolist())



print("\n========== DUPLICATE ANALYSIS ==========")

duplicate_count = df.duplicated().sum()

print("Duplicate Rows:", duplicate_count)

df = df.drop_duplicates()

df.reset_index(drop=True, inplace=True)

print("Rows After Removing Duplicates:", len(df))



print("\n========== MISSING VALUE ANALYSIS ==========")

missing_report = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": (
        df.isnull().sum() / len(df) * 100
    )
})

print(
    missing_report.sort_values(
        by="Missing_Percentage",
        ascending=False
    )
)



print("\n========== TEXT CLEANING ==========")

text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:

    df[col] = df[col].apply(
        lambda x: x.strip()
        if isinstance(x, str)
        else x
    )

df.replace(
    r"^\s*$",
    np.nan,
    regex=True,
    inplace=True
)

print("Text Cleaning Completed")



print("\n========== DATE CONVERSION ==========")

date_columns = []

for col in df.columns:

    if "date" in col or col.endswith("_at"):

        original = df[col].copy()

        converted = pd.to_datetime(
            original,
            format="%d-%m-%Y",
            errors="coerce"
        )

        if converted.notna().sum() == 0:

            converted = pd.to_datetime(
                original,
                format="mixed",
                errors="coerce",
                dayfirst=True
            )

        if converted.notna().sum() > 0:

            df[col] = converted
            date_columns.append(col)

            print("Converted Date Column:", col)

if not date_columns:
    print("No date columns detected.")



print("\n========== NUMERICAL DATA CLEANING ==========")

for col in df.select_dtypes(
    include=["object", "string"]
).columns:

    cleaned = (
        df[col]
        .astype("string")
        .str.replace(r"[₹,%]", "", regex=True)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    numeric = pd.to_numeric(
        cleaned,
        errors="coerce"
    )

    original_count = df[col].notna().sum()

    if original_count > 0:

        ratio = numeric.notna().sum() / original_count

        if ratio >= 0.90:
            df[col] = numeric

print("Numerical Cleaning Completed")


# ==============================================================
# 10. NEGATIVE VALUE ANALYSIS
# ==============================================================

print("\n========== NEGATIVE VALUE ANALYSIS ==========")

numeric_columns = df.select_dtypes(
    include=np.number
).columns

for col in numeric_columns:

    negative_count = (df[col] < 0).sum()

    if negative_count > 0:
        print(
            col,
            "Negative Values:",
            negative_count
        )


# ==============================================================
# 11. MISSING VALUE TREATMENT
# ==============================================================

print("\n========== MISSING VALUE TREATMENT ==========")

numeric_columns = df.select_dtypes(
    include=np.number
).columns

categorical_columns = df.select_dtypes(
    include=["object", "string"]
).columns

# Fill numerical missing values with median

for col in numeric_columns:

    if df[col].isnull().sum() > 0:

        median_value = df[col].median()

        if pd.notna(median_value):
            df[col] = df[col].fillna(median_value)


# Fill categorical missing values

for col in categorical_columns:

    if df[col].isnull().sum() > 0:

        df[col] = df[col].fillna("Unknown")


# Handle date columns separately:
# Do not invent missing dates.

print("Missing Value Treatment Completed")


# ==============================================================
# 12. SORT DATA BY DATE - ASCENDING ORDER
# ==============================================================

print("\n========== DATE SORTING ==========")

if date_columns:

    sort_column = (
        "listing_date"
        if "listing_date" in date_columns
        else date_columns[0]
    )

    df = df.sort_values(
        by=sort_column,
        ascending=True,
        na_position="last"
    )

    print("Sorted Column:", sort_column)
    print("Oldest Date to Newest Date")

else:
    print("No Date Column Available for Sorting")

df.reset_index(drop=True, inplace=True)


# ==============================================================
# 13. FINAL MISSING VALUE CHECK
# ==============================================================

print("\n========== FINAL MISSING VALUES ==========")

print(df.isnull().sum())

print(
    "Total Missing Values:",
    df.isnull().sum().sum()
)


# ==============================================================
# 14. NUMERICAL EDA
# ==============================================================

print("\n========== NUMERICAL EDA ==========")

print(df.describe().T)


# ==============================================================
# 15. CATEGORICAL EDA
# ==============================================================

print("\n========== CATEGORICAL EDA ==========")

for col in df.select_dtypes(
    include=["object", "string"]
).columns:

    print("\nColumn:", col)

    print(df[col].value_counts().head(10))


# ==============================================================
# 16. UNIQUE VALUE ANALYSIS
# ==============================================================

print("\n========== UNIQUE VALUE ANALYSIS ==========")

for col in df.columns:

    print(
        col,
        "Unique Values:",
        df[col].nunique()
    )


# ==============================================================
# 17. MISSING VALUE HEATMAP
# ==============================================================

plt.figure(figsize=(12, 6))

sns.heatmap(
    df.isnull(),
    cbar=False,
    cmap="viridis"
)

plt.title("Missing Values Heatmap")

plt.tight_layout()

plt.savefig(
    os.path.join(BASE_DIR, "missing_values_heatmap.png")
)

plt.show()


# ==============================================================
# 18. CORRELATION HEATMAP
# ==============================================================

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

    plt.savefig(
        os.path.join(BASE_DIR, "correlation_heatmap.png")
    )

    plt.show()


# ==============================================================
# 19. NUMERICAL DISTRIBUTION ANALYSIS
# ==============================================================

for col in numeric_df.columns:

    if numeric_df[col].nunique() > 1:

        plt.figure(figsize=(8, 5))

        sns.histplot(
            df[col].dropna(),
            kde=True,
            bins=30
        )

        plt.title(f"Distribution of {col}")

        plt.xlabel(col)
        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                BASE_DIR,
                f"distribution_{col}.png"
            )
        )

        plt.show()


# ==============================================================
# 20. OUTLIER DETECTION
# ==============================================================

print("\n========== OUTLIER DETECTION ==========")

outlier_report = []

for col in numeric_df.columns:

    if df[col].nunique() > 1:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        outliers = df[
            (df[col] < lower_limit) |
            (df[col] > upper_limit)
        ]

        outlier_report.append({
            "Column": col,
            "Outlier_Count": len(outliers),
            "Lower_Limit": lower_limit,
            "Upper_Limit": upper_limit
        })

        print(
            col,
            "Outliers:",
            len(outliers)
        )

        plt.figure(figsize=(8, 4))

        sns.boxplot(x=df[col])

        plt.title(f"Outlier Detection - {col}")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                BASE_DIR,
                f"outliers_{col}.png"
            )
        )

        plt.show()

outlier_report = pd.DataFrame(outlier_report)


# ==============================================================
# 21. DATE-WISE ANALYSIS
# ==============================================================

if date_columns:

    date_column = (
        "listing_date"
        if "listing_date" in date_columns
        else date_columns[0]
    )

    date_df = df.dropna(
        subset=[date_column]
    ).copy()

    date_df["year"] = date_df[date_column].dt.year
    date_df["month"] = date_df[date_column].dt.month
    date_df["month_name"] = date_df[date_column].dt.month_name()

    print("\n========== YEAR-WISE ANALYSIS ==========")

    print(date_df.groupby("year").size())

    print("\n========== MONTH-WISE ANALYSIS ==========")

    monthly_summary = date_df.groupby(
        ["year", "month", "month_name"]
    ).size()

    print(monthly_summary)

    monthly_trend = (
        date_df
        .set_index(date_column)
        .resample("ME")
        .size()
    )

    plt.figure(figsize=(12, 5))

    monthly_trend.plot()

    plt.title("Monthly Product Listing Trend")

    plt.xlabel("Date")
    plt.ylabel("Number of Products")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            BASE_DIR,
            "monthly_listing_trend.png"
        )
    )

    plt.show()


# ==============================================================
# 22. CATEGORY AND BRAND ANALYSIS
# ==============================================================

category_columns = [
    col for col in df.columns
    if "category" in col or "brand" in col
]

for col in category_columns:

    top_10 = df[col].value_counts().head(10)

    print(f"\nTop 10 Values in {col}:")

    print(top_10)

    plt.figure(figsize=(10, 5))

    top_10.plot(kind="bar")

    plt.title(f"Top 10 - {col}")

    plt.xlabel(col)
    plt.ylabel("Count")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            BASE_DIR,
            f"top10_{col}.png"
        )
    )

    plt.show()


# ==============================================================
# 23. FINAL DATASET VALIDATION
# ==============================================================

print("\n========== FINAL DATASET VALIDATION ==========")

print("Final Rows:", df.shape[0])
print("Final Columns:", df.shape[1])

print("Remaining Duplicates:", df.duplicated().sum())

print(
    "Remaining Missing Values:",
    df.isnull().sum().sum()
)

print("\nFinal Data Types:")
print(df.dtypes)

print("\nFinal Dataset Preview:")
print(df.head(10))


# ==============================================================
# 24. EXPORT CLEANED DATASET
# ==============================================================

print("\n========== EXPORTING FILES ==========")

df.to_csv(
    os.path.join(
        BASE_DIR,
        "Flipkart_Cleaned_Dataset.csv"
    ),
    index=False
)

missing_report.to_csv(
    os.path.join(
        BASE_DIR,
        "Flipkart_Missing_Values_Report.csv"
    )
)

df.describe(
    include="all"
).T.to_csv(
    os.path.join(
        BASE_DIR,
        "Flipkart_Statistical_Summary.csv"
    )
)

outlier_report.to_csv(
    os.path.join(
        BASE_DIR,
        "Flipkart_Outlier_Report.csv"
    ),
    index=False
)


# ==============================================================
# 25. COMPLETION SUMMARY
# ==============================================================

print("\n")
print("=" * 55)

print("FLIPKART DATA ANALYTICS PROJECT")
print("=" * 55)

print("Dataset Loaded Successfully")
print("EDA Completed")
print("Data Cleaning Completed")
print("Duplicates Removed")
print("Missing Values Analysed")
print("Date Conversion Completed")
print("Date Sorting Completed")
print("Outlier Detection Completed")
print("Visualizations Generated")
print("Reports Exported")

print("-" * 55)

print("FINAL DATASET SHAPE:", df.shape)

print("OUTPUT FOLDER:", BASE_DIR)

print("=" * 55)

print("\nALL OPERATIONS COMPLETED SUCCESSFULLY!")
