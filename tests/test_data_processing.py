"""
Unit tests for data_processing module.

Tests cover data loading, cleaning, merging, and validation functions.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
from datetime import datetime

# Adjust import path to find src module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import (
    load_csv_file,
    convert_to_datetime,
    clean_building_permits_data,
    process_construction_costs_data,
    process_residential_sales_data,
    aggregate_to_quarterly,
    merge_quarterly_data,
    validate_merged_data,
)


class TestLoadCSVFile:
    """Test CSV file loading with encoding fallback."""

    def test_load_csv_utf8(self):
        """Test loading UTF-8 encoded CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("col1,col2\nvalue1,value2\nvalue3,value4\n")
            temp_path = f.name

        try:
            df = load_csv_file(temp_path, encoding='utf-8')
            assert df.shape == (2, 2)
            assert df.iloc[0, 0] == "value1"
        finally:
            Path(temp_path).unlink()

    def test_load_csv_with_encoding_fallback(self):
        """Test encoding fallback when UTF-8 fails."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='latin1') as f:
            f.write("col1,col2\nvalue1,value2\n")
            temp_path = f.name

        try:
            df = load_csv_file(temp_path, encoding='utf-8')
            assert df.shape == (1, 2)
        finally:
            Path(temp_path).unlink()

    def test_load_csv_empty_file(self):
        """Test loading empty CSV file produces warning."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("col1,col2\n")  # Header only, no data rows
            temp_path = f.name

        try:
            df = load_csv_file(temp_path, encoding='utf-8')
            assert df.empty
        finally:
            Path(temp_path).unlink()

    def test_load_csv_with_kwargs(self):
        """Test passing additional kwargs to pd.read_csv."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("col1,col2\n1,2\n3,4\n")
            temp_path = f.name

        try:
            df = load_csv_file(temp_path, encoding='utf-8', dtype={'col1': int})
            assert df['col1'].dtype == int
        finally:
            Path(temp_path).unlink()


class TestConvertToDatetime:
    """Test date conversion functions."""

    def test_convert_month_format(self):
        """Test conversion of YYYYMmm format to datetime."""
        series = pd.Series(['2023-01', '2023-02', '2023-03'])
        result = convert_to_datetime(series, format_type='month')
        
        assert pd.api.types.is_datetime64_any_dtype(result)
        assert result[0] == pd.Timestamp('2023-01-01')
        assert result[1] == pd.Timestamp('2023-02-01')

    def test_convert_quarter_format(self):
        """Test conversion of YYYYQN format to datetime."""
        series = pd.Series(['2023Q1', '2023Q2', '2023Q3', '2023Q4'])
        result = convert_to_datetime(series, format_type='quarter')
        
        assert pd.api.types.is_datetime64_any_dtype(result)
        assert result[0] == pd.Timestamp('2023-01-01')
        assert result[1] == pd.Timestamp('2023-04-01')

    def test_convert_invalid_format_type(self):
        """Test that invalid format type raises ValueError."""
        series = pd.Series(['2023-01-01'])
        with pytest.raises(ValueError):
            convert_to_datetime(series, format_type='invalid')

    def test_convert_coerce_invalid_dates(self):
        """Test that invalid dates are converted to NaT."""
        series = pd.Series(['202301M', 'invalid', '202302M'])
        result = convert_to_datetime(series, format_type='month')
        
        assert pd.isna(result[1])


class TestCleanBuildingPermitsData:
    """Test building permits data cleaning."""

    @pytest.fixture
    def sample_permits_df(self):
        """Create sample building permits DataFrame."""
        return pd.DataFrame({
            "INVESTITOR": ["Investitor - SKUPAJ"] * 3,
            "KLASIFIKACIJA VRST OBJEKTOV [CC-SI]": ["1 Stavbe - SKUPAJ"] * 3,
            "MESEC": ["202301M", "202302M", "202303M"],
            "MERITVE": ["Število stavb", "Število stavb", "Število stavb"],
            "DATA": [100, 150, 120],
        })

    def test_clean_permits_basic(self, sample_permits_df):
        """Test basic building permits cleaning."""
        result = clean_building_permits_data(sample_permits_df)
        
        assert "date" in result.columns
        assert "num_buildings" in result.columns
        assert len(result) == 3
        assert result["num_buildings"].sum() == 370

    def test_clean_permits_filters_metric(self):
        """Test that only 'Število stavb' metric is included."""
        df = pd.DataFrame({
            "INVESTITOR": ["Investitor - SKUPAJ"] * 2,
            "KLASIFIKACIJA VRST OBJEKTOV [CC-SI]": ["1 Stavbe - SKUPAJ"] * 2,
            "MESEC": ["202301M", "202302M"],
            "MERITVE": ["Število stavb", "Druga metrika"],
            "DATA": [100, 200],
        })
        result = clean_building_permits_data(df)
        
        assert len(result) == 1
        assert result["num_buildings"].iloc[0] == 100

    def test_clean_permits_handles_null_values(self):
        """Test that null values are handled properly."""
        df = pd.DataFrame({
            "INVESTITOR": ["Investitor - SKUPAJ"] * 3,
            "KLASIFIKACIJA VRST OBJEKTOV [CC-SI]": ["1 Stavbe - SKUPAJ"] * 3,
            "MESEC": ["202301M", "202302M", "202303M"],
            "MERITVE": ["Število stavb"] * 3,
            "DATA": [100, None, 120],
        })
        result = clean_building_permits_data(df)
        
        assert len(result) == 2  # null value should be dropped


class TestProcessConstructionCostsData:
    """Test construction costs data processing."""

    @pytest.fixture
    def sample_costs_df(self):
        """Create sample construction costs DataFrame."""
        return pd.DataFrame({
            "ČETRTLETJE": ["2023Q1", "2023Q2", "2023Q3"],
            "VRSTE GRADBENIH STROŠKOV": ["Gradbeni stroški - SKUPAJ"] * 3,
            "DATA": [105.5, 107.2, 108.1],
        })

    def test_process_costs_basic(self, sample_costs_df):
        """Test basic construction costs processing."""
        result = process_construction_costs_data(sample_costs_df)
        
        assert "date" in result.columns
        assert "construction_cost_index" in result.columns
        assert len(result) == 3

    def test_process_costs_filters_cost_type(self):
        """Test that only 'Gradbeni stroški - SKUPAJ' is included."""
        df = pd.DataFrame({
            "ČETRTLETJE": ["2023Q1", "2023Q2"],
            "VRSTE GRADBENIH STROŠKOV": ["Gradbeni stroški - SKUPAJ", "Drugi stroški"],
            "DATA": [105.5, 110.0],
        })
        result = process_construction_costs_data(df)
        
        assert len(result) == 1
        assert result["construction_cost_index"].iloc[0] == 105.5

    def test_process_costs_handles_whitespace(self):
        """Test that column name whitespace is stripped."""
        df = pd.DataFrame({
            " ČETRTLETJE ": ["2023Q1"],
            " VRSTE GRADBENIH STROŠKOV ": ["Gradbeni stroški - SKUPAJ"],
            " DATA ": [105.5],
        })
        result = process_construction_costs_data(df)
        
        assert len(result) == 1


class TestProcessResidentialSalesData:
    """Test residential sales data processing."""

    @pytest.fixture
    def sample_sales_df(self):
        """Create sample residential sales DataFrame."""
        return pd.DataFrame({
            "STANOVANJSKE NEPREMIČNINE": ["Stanovanjske nepremičnine - SKUPAJ"] * 3,
            "ČETRTLETJE": ["2023Q1", "2023Q2", "2023Q3"],
            "MERITVE": ["Število prodaj", "Vrednost prodaj (v EUR)", "Število prodaj"],
            "DATA": [100, 5000000, 120],
        })

    def test_process_sales_basic(self):
        """Test basic residential sales processing."""
        df = pd.DataFrame({
            "STANOVANJSKE NEPREMIČNINE": ["Stanovanjske nepremičnine - SKUPAJ"] * 2,
            "ČETRTLETJE": ["2023Q1", "2023Q1"],
            "MERITVE": ["Število prodaj", "Vrednost prodaj (v EUR)"],
            "DATA": [100, 5000000],
        })
        result = process_residential_sales_data(df)
        
        assert "date" in result.columns
        assert "num_residential_sales" in result.columns
        assert "avg_price_eur" in result.columns
        assert len(result) == 1
        assert result["avg_price_eur"].iloc[0] == 50000.0

    def test_process_sales_zero_sales_price_is_na(self):
        """Test that avg_price is NA when num_sales is zero."""
        df = pd.DataFrame({
            "STANOVANJSKE NEPREMIČNINE": ["Stanovanjske nepremičnine - SKUPAJ"] * 2,
            "ČETRTLETJE": ["2023Q1", "2023Q1"],
            "MERITVE": ["Število prodaj", "Vrednost prodaj (v EUR)"],
            "DATA": [0, 5000000],
        })
        result = process_residential_sales_data(df)
        
        assert pd.isna(result["avg_price_eur"].iloc[0])

    def test_process_sales_missing_metric(self):
        """Test handling of missing metrics."""
        df = pd.DataFrame({
            "STANOVANJSKE NEPREMIČNINE": ["Stanovanjske nepremičnine - SKUPAJ"],
            "ČETRTLETJE": ["2023Q1"],
            "MERITVE": ["Število prodaj"],
            "DATA": [100],
        })
        result = process_residential_sales_data(df)
        
        assert pd.isna(result["num_residential_sales"].iloc[0]) or result["num_residential_sales"].iloc[0] == 100


class TestAggregateToQuarterly:
    """Test monthly to quarterly aggregation."""

    def test_aggregate_monthly_to_quarterly(self):
        """Test aggregation of monthly data to quarterly."""
        df = pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=6, freq='MS'),
            "value": [100, 110, 120, 130, 140, 150]
        })
        result = aggregate_to_quarterly(df, 'value')
        
        assert len(result) == 2  # 2 quarters
        assert result["value"].iloc[0] == 330  # Jan+Feb+Mar
        assert result["value"].iloc[1] == 420  # Apr+May+Jun

    def test_aggregate_with_nan_values(self):
        """Test aggregation with NaN values."""
        df = pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=3, freq='MS'),
            "value": [100, np.nan, 120]
        })
        result = aggregate_to_quarterly(df, 'value')
        
        assert result["value"].iloc[0] == 220  # sum ignores NaN


class TestMergeQuarterlyData:
    """Test quarterly data merging."""

    @pytest.fixture
    def sample_permits_quarterly(self):
        """Create sample quarterly permits."""
        return pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=4, freq='QS'),
            "num_buildings": [100, 110, 120, 130]
        })

    @pytest.fixture
    def sample_costs_quarterly(self):
        """Create sample quarterly costs."""
        return pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=4, freq='QS'),
            "construction_cost_index": [105.5, 107.2, 108.1, 109.0]
        })

    @pytest.fixture
    def sample_sales_quarterly(self):
        """Create sample quarterly sales."""
        return pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=4, freq='QS'),
            "num_residential_sales": [50, 55, 60, 65],
            "avg_price_eur": [50000, 52000, 54000, 56000]
        })

    def test_merge_permits_and_costs(self, sample_permits_quarterly, sample_costs_quarterly):
        """Test basic merge of permits and costs."""
        result = merge_quarterly_data(sample_permits_quarterly, sample_costs_quarterly)
        
        assert len(result) == 4
        assert "num_buildings" in result.columns
        assert "construction_cost_index" in result.columns
        assert "num_residential_sales" not in result.columns

    def test_merge_all_datasets(self, sample_permits_quarterly, sample_costs_quarterly, sample_sales_quarterly):
        """Test merge of all three datasets."""
        result = merge_quarterly_data(
            sample_permits_quarterly,
            sample_costs_quarterly,
            sample_sales_quarterly
        )
        
        assert len(result) == 4
        assert "num_buildings" in result.columns
        assert "construction_cost_index" in result.columns
        assert "num_residential_sales" in result.columns
        assert "avg_price_eur" in result.columns

    def test_merge_inner_join_behavior(self):
        """Test that inner join keeps only matching quarters."""
        permits = pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=3, freq='QS'),
            "num_buildings": [100, 110, 120]
        })
        costs = pd.DataFrame({
            "date": pd.date_range('2023-04-01', periods=2, freq='QS'),
            "construction_cost_index": [107.2, 108.1]
        })
        
        result = merge_quarterly_data(permits, costs)
        
        # Should keep overlapping quarters (Q2 2023 and Q3 2023)
        assert len(result) == 2

    def test_merge_left_join_sales(self, sample_permits_quarterly, sample_costs_quarterly):
        """Test that sales are left-joined (non-matching quarters preserved)."""
        sales = sample_permits_quarterly[['date']].copy()
        sales['num_residential_sales'] = [50, np.nan, 60, 65]
        sales['avg_price_eur'] = [50000, np.nan, 54000, 56000]
        
        result = merge_quarterly_data(
            sample_permits_quarterly,
            sample_costs_quarterly,
            sales
        )
        
        assert len(result) == 4  # All quarters preserved


class TestValidateMergedData:
    """Test merged data validation."""

    @pytest.fixture
    def valid_merged_df(self):
        """Create a valid merged DataFrame."""
        return pd.DataFrame({
            "date": pd.date_range('2023-01-01', periods=8, freq='QS'),
            "num_buildings": [100, 110, 120, 130, 140, 150, 160, 170],
            "construction_cost_index": [105.5, 107.2, 108.1, 109.0, 110.0, 111.0, 112.0, 113.0],
            "num_residential_sales": [50, 55, 60, 65, 70, 75, 80, 85],
            "avg_price_eur": [50000, 52000, 54000, 56000, 58000, 60000, 62000, 64000]
        })

    def test_validate_clean_data(self, valid_merged_df):
        """Test validation of clean, complete data."""
        result = validate_merged_data(valid_merged_df)
        
        assert len(result["warnings"]) == 0
        assert result["num_rows"] == 8

    def test_validate_detects_duplicates(self, valid_merged_df):
        """Test that duplicate rows are detected."""
        df_with_dup = pd.concat([valid_merged_df.iloc[[0]], valid_merged_df.iloc[[0]]], ignore_index=True)
        result = validate_merged_data(df_with_dup)
        
        assert any("Duplicate rows" in w for w in result["warnings"])

    def test_validate_detects_duplicate_dates(self, valid_merged_df):
        """Test that duplicate date values are detected."""
        df_with_dup_date = valid_merged_df.copy()
        df_with_dup_date.loc[1, "date"] = df_with_dup_date.loc[0, "date"]
        result = validate_merged_data(df_with_dup_date)
        
        assert any("Duplicate quarter" in w for w in result["warnings"])

    def test_validate_detects_outliers(self, valid_merged_df):
        """Test that outliers are detected."""
        df_with_outlier = valid_merged_df.copy()
        df_with_outlier.loc[0, "num_buildings"] = 10000  # Large outlier
        result = validate_merged_data(df_with_outlier)
        
        assert any("outliers" in w for w in result["warnings"])

    def test_validate_price_without_sales(self, valid_merged_df):
        """Test detection of price without sales."""
        df = valid_merged_df.copy()
        df.loc[0, "num_residential_sales"] = 0
        df.loc[0, "avg_price_eur"] = 50000
        result = validate_merged_data(df)
        
        assert any("Average price present but zero sales" in w for w in result["warnings"])

    def test_validate_non_positive_prices(self, valid_merged_df):
        """Test detection of non-positive prices."""
        df = valid_merged_df.copy()
        df.loc[0, "avg_price_eur"] = -1000
        result = validate_merged_data(df)
        
        assert any("Non-positive average prices" in w for w in result["warnings"])

    def test_validate_extreme_prices(self, valid_merged_df):
        """Test detection of extremely large prices."""
        df = valid_merged_df.copy()
        df.loc[0, "avg_price_eur"] = 64000 * 20  # > 10x median
        result = validate_merged_data(df)
        
        assert any("Extremely large average prices" in w for w in result["warnings"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
