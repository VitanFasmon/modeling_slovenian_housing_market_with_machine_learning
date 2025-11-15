"""
Data processing module for Slovenian construction and real estate data.

Provides functions to load, clean, and merge datasets from the Statistical Office of Slovenia.
"""

import logging
import pandas as pd
from pathlib import Path
from pyaxis import pyaxis

logger = logging.getLogger(__name__)


def load_px_file(file_path: str, encoding: str = "cp1250") -> pd.DataFrame:
    """
    Load and parse a PX file into a pandas DataFrame.
    
    Args:
        file_path: Path to the PX file (as string or Path)
        encoding: File encoding (default: cp1250 for Slovenian files)
    
    Returns:
        DataFrame containing the data from the PX file
    """
    file_path = str(file_path)  # ensure string path
    data_dict = pyaxis.parse(file_path, encoding=encoding)
    logger.info(f"Loaded PX file from {file_path}")
    return data_dict["DATA"]


def load_csv_file(file_path: str, encoding: str = "utf-8", **kwargs) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame with error handling and validation.
    
    Args:
        file_path: Path to the CSV file
        encoding: File encoding (default: utf-8)
        **kwargs: Additional arguments to pass to pd.read_csv()
    
    Returns:
        DataFrame containing the data from the CSV file
        
    Raises:
        ValueError: If file cannot be read with any supported encoding
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding, **kwargs)
        logger.info(f"Loaded CSV from {file_path} using {encoding} encoding")
    except UnicodeDecodeError:
        encodings = ['latin1', 'cp1250', 'iso-8859-1', 'windows-1252']
        df = None
        for enc in encodings:
            try:
                df = pd.read_csv(file_path, encoding=enc, **kwargs)
                logger.info(f"Loaded CSV from {file_path} using {enc} encoding (fallback)")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError(f"Failed to read file {file_path} with encodings: {[encoding] + encodings}")
    
    if df.empty:
        logger.warning(f"Loaded CSV file {file_path} is empty")
    
    return df


def convert_to_datetime(series: pd.Series, format_type: str = "month") -> pd.Series:
    """
    Convert a series of dates to datetime format.
    
    Args:
        series: Series containing date strings
        format_type: Type of date format ('month' for YYYYMmm or 'quarter' for YYYYQN)
    
    Returns:
        Series with datetime values
    """
    if format_type == "month":
        return pd.to_datetime(series.str.replace("M", "-"), errors="coerce")
    elif format_type == "quarter":
        return pd.PeriodIndex(series, freq="Q").to_timestamp()
    else:
        raise ValueError(f"Unsupported format_type: {format_type}")


def clean_building_permits_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process building permits data into monthly time series.
    
    Filters for total buildings across all investor types.
    
    Args:
        df: Raw building permits DataFrame
    
    Returns:
        DataFrame with columns: date, num_building_permits
    """
    COLUMN_MAPPING = {
        "INVESTITOR": "investor",
        "KLASIFIKACIJA VRST OBJEKTOV [CC-SI]": "building_class",
        "MESEC": "month",
        "MERITVE": "metric",
        "DATA": "value"
    }

    TOTAL_BUILDINGS_FILTER = {
        "metric": "Število stavb",
        "investor": "Investitor - SKUPAJ",
        "building_class": "1 Stavbe - SKUPAJ"
    }

    df = df.rename(columns=COLUMN_MAPPING)
    df["date"] = convert_to_datetime(df["month"], "month")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    mask = pd.Series(True, index=df.index)
    for col, val in TOTAL_BUILDINGS_FILTER.items():
        mask &= df[col] == val

    df_filtered = df[mask].dropna(subset=["value"])
    result = df_filtered[["date", "value"]].rename(columns={"value": "num_building_permits"})
    
    logger.info(f"Cleaned building permits: {len(result)} months")
    return result


def process_construction_costs_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process construction costs data into quarterly time series.
    
    Filters for total construction costs index.
    
    Args:
        df: Raw construction costs DataFrame
    
    Returns:
        DataFrame with columns: date, construction_cost_index
    """
    COLUMN_MAPPING = {
        "ČETRTLETJE": "quarter",
        "VRSTE GRADBENIH STROŠKOV": "cost_type",
        "DATA": "index_value"
    }

    df = df.copy()
    df.columns = df.columns.str.strip()

    df = df.rename(columns=COLUMN_MAPPING)
    df["index_value"] = pd.to_numeric(df["index_value"], errors="coerce")
    df["date"] = convert_to_datetime(df["quarter"], "quarter")

    cost_type_col = "cost_type" if "cost_type" in df.columns else "VRSTE GRADBENIH STROŠKOV"
    df_filtered = df[df[cost_type_col] == "Gradbeni stroški - SKUPAJ"]

    result = df_filtered[["date", "index_value"]].rename(
        columns={"index_value": "construction_cost_index"}
    )
    
    logger.info(f"Cleaned construction costs: {len(result)} quarters")
    return result


def process_residential_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process residential sales data into quarterly time series with average price.
    
    Computes average price per sale as total value / number of sales.
    
    Args:
        df: Raw residential sales DataFrame
    
    Returns:
        DataFrame with columns: date, num_residential_sales, avg_price_eur
    """
    MAPPING = {
        "STANOVANJSKE NEPREMIČNINE": "residential_real_estate",
        "ČETRTLETJE": "quarter",
        "MERITVE": "metric",
        "DATA": "value",
    }

    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.rename(columns=MAPPING)

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = convert_to_datetime(df["quarter"], "quarter")

    cat_col = "residential_real_estate" if "residential_real_estate" in df.columns else "STANOVANJSKE NEPREMIČNINE"
    df_filtered = df[df[cat_col].str.contains("Stanovanjske nepremičnine - SKUPAJ", na=False, regex=False)]

    pivot = (
        df_filtered
        .pivot_table(index="date", columns="metric", values="value", aggfunc="sum")
        .reset_index()
    )

    num_metric = "Število prodaj"
    value_metric = "Vrednost prodaj (v EUR)"

    num_sales = (
        pd.to_numeric(pivot[num_metric], errors="coerce").fillna(0)
        if num_metric in pivot.columns
        else pd.Series(0, index=pivot.index, dtype=float)
    )

    total_value = (
        pd.to_numeric(pivot[value_metric], errors="coerce").fillna(0)
        if value_metric in pivot.columns
        else pd.Series(0, index=pivot.index, dtype=float)
    )

    # Compute average price; set to NA where sales == 0
    avg_price = (total_value / num_sales).replace([pd.NA, float("inf"), float("-inf"), float("nan")], pd.NA)
    avg_price[num_sales == 0] = pd.NA

    result = pd.DataFrame({
        "date": pivot["date"],
        "num_residential_sales": num_sales.astype(float),
        "avg_price_eur": avg_price
    })

    result = result.sort_values("date").reset_index(drop=True)
    
    logger.info(f"Cleaned residential sales: {len(result)} quarters, {result['num_residential_sales'].sum():.0f} total sales")
    return result


def aggregate_to_quarterly(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """
    Aggregate monthly data to quarterly frequency.
    
    Args:
        df: DataFrame with 'date' column and metric column
        value_col: Name of the column to aggregate
    
    Returns:
        DataFrame aggregated to quarter-end frequency
    """
    return (
        df.set_index("date")
        .resample("QE")[value_col]
        .sum()
        .reset_index()
    )


def merge_quarterly_data(
    permits_df: pd.DataFrame,
    costs_df: pd.DataFrame,
    sales_df: pd.DataFrame | None = None
) -> pd.DataFrame:
    """
    Merge quarterly permits, costs, and optional residential sales data.
    
    Performs an inner join between permits and costs, and a left join with sales.
    
    Args:
        permits_df: Quarterly building permits DataFrame
        costs_df: Quarterly construction costs DataFrame
        sales_df: Optional quarterly residential sales DataFrame
    
    Returns:
        Merged DataFrame with columns: date, num_building_permits, construction_cost_index,
        (optionally) num_residential_sales, avg_price_eur
    """
    p = permits_df.copy()
    c = costs_df.copy()

    p["quarter"] = p["date"].dt.to_period("Q").dt.start_time
    c["quarter"] = c["date"].dt.to_period("Q").dt.start_time

    merged = pd.merge(
        p,
        c,
        on="quarter",
        how="inner",
        suffixes=("_permits", "_costs"),
        validate="one_to_one"
    )

    if sales_df is not None:
        s = sales_df.copy()
        s["quarter"] = s["date"].dt.to_period("Q").dt.start_time
        sales_cols = [col for col in ["num_residential_sales", "avg_price_eur"] if col in s.columns]
        s_keep = s[["quarter"] + sales_cols].drop_duplicates(subset=["quarter"])
        merged = pd.merge(merged, s_keep, on="quarter", how="left", validate="one_to_many")

    merged = merged.rename(columns={"quarter": "date"})

    for col in ["date_permits", "date_costs", "date_x", "date_y"]:
        if col in merged.columns:
            merged = merged.drop(columns=[col])

    # Support both legacy and new column names. Prefer `num_building_permits`.
    if "num_building_permits" not in merged.columns:
        if "num_buildings" in merged.columns:
            merged = merged.rename(columns={"num_buildings": "num_building_permits"})
        elif "value" in merged.columns:
            merged = merged.rename(columns={"value": "num_building_permits"})

    if "construction_cost_index" not in merged.columns and "index_value" in merged.columns:
        merged = merged.rename(columns={"index_value": "construction_cost_index"})

    merged = merged.dropna(subset=["num_building_permits", "construction_cost_index"])

    cols = ["date", "num_building_permits", "construction_cost_index"]
    if "num_residential_sales" in merged.columns:
        cols.append("num_residential_sales")
    if "avg_price_eur" in merged.columns:
        cols.append("avg_price_eur")

    cols = [c for c in cols if c in merged.columns]
    merged = merged[cols]

    merged = merged.sort_values("date").reset_index(drop=True)
    
    logger.info(f"Merged data: {len(merged)} quarters from {merged['date'].min().date()} to {merged['date'].max().date()}")
    return merged


def validate_merged_data(df: pd.DataFrame) -> dict:
    """
    Validate the merged dataset for potential issues.
    
    Args:
        df: Merged quarterly DataFrame
    
    Returns:
        Dictionary with validation results and warnings
    """
    warnings = []

    required_cols = ["date", "num_building_permits", "construction_cost_index"]
    for col in required_cols:
        if col not in df.columns:
            warnings.append(f"Missing required column: {col}")

    if df.duplicated().any():
        warnings.append("Duplicate rows found")

    if df["date"].duplicated().any():
        warnings.append("Duplicate quarter timestamps found")

    # Check for gaps in time series using period logic
    qperiods = df["date"].dt.to_period("Q")
    expected = pd.period_range(qperiods.min(), qperiods.max(), freq="Q")
    missing = set(expected) - set(qperiods)
    if missing:
        warnings.append(f"Missing quarters: {sorted(missing)}")

    # Outlier detection
    numeric_cols = ["num_building_permits", "construction_cost_index"]
    if "num_residential_sales" in df.columns:
        numeric_cols.append("num_residential_sales")
    if "avg_price_eur" in df.columns:
        numeric_cols.append("avg_price_eur")

    for col in numeric_cols:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            continue
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outlier_count = ((series < lower) | (series > upper)).sum()
        if outlier_count > 0:
            warnings.append(f"{outlier_count} outliers in {col}")

    # Sales/price consistency
    if "num_residential_sales" in df.columns and "avg_price_eur" in df.columns:
        bad_price_mask = df["avg_price_eur"].notna() & (df["num_residential_sales"].fillna(0) == 0)
        if bad_price_mask.any():
            warnings.append(f"Average price present but zero sales in {bad_price_mask.sum()} quarter(s)")

        valid_prices = df["avg_price_eur"].dropna()
        if not valid_prices.empty:
            if (valid_prices <= 0).any():
                warnings.append("Non-positive average prices detected")
            med = valid_prices.median()
            if med > 0 and (valid_prices > med * 10).any():
                warnings.append("Extremely large average prices detected (> 10x median)")

    if warnings:
        for w in warnings:
            logger.warning(f"Validation: {w}")
    else:
        logger.info("Validation completed: no issues found")

    return {"warnings": warnings, "num_rows": len(df), "date_range": (df["date"].min(), df["date"].max())}
