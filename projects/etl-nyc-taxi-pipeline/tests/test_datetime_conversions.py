import pandas as pd
from src.transform.datetime_conversions import convert_datetime_columns


class TestConvertDatetimeColumns:

    def test_converts_string_to_datetime(self):
        df = pd.DataFrame({"pickup_datetime": ["2022-01-01 08:00:00"]})
        result = convert_datetime_columns(df, ["pickup_datetime"])
        assert pd.api.types.is_datetime64_any_dtype(result["pickup_datetime"])

    def test_converts_multiple_columns(self):
        df = pd.DataFrame({
            "pickup_datetime": ["2022-01-01 08:00:00"],
            "dropoff_datetime": ["2022-01-01 08:30:00"],
        })
        result = convert_datetime_columns(df, ["pickup_datetime", "dropoff_datetime"])
        assert pd.api.types.is_datetime64_any_dtype(result["pickup_datetime"])
        assert pd.api.types.is_datetime64_any_dtype(result["dropoff_datetime"])

    def test_coerces_invalid_string_to_nat(self):
        df = pd.DataFrame({"pickup_datetime": ["not_a_date"]})
        result = convert_datetime_columns(df, ["pickup_datetime"])
        assert result["pickup_datetime"].isna().iloc[0]

    def test_missing_column_does_not_raise(self):
        df = pd.DataFrame({"pickup_datetime": ["2022-01-01 08:00:00"]})
        result = convert_datetime_columns(df, ["pickup_datetime", "nonexistent_column"])
        assert "nonexistent_column" not in result.columns

    def test_already_datetime_column_unchanged(self):
        ts = pd.Timestamp("2022-01-01 08:00:00")
        df = pd.DataFrame({"pickup_datetime": [ts]})
        result = convert_datetime_columns(df, ["pickup_datetime"])
        assert result["pickup_datetime"].iloc[0] == ts

    def test_empty_column_list_leaves_dataframe_unchanged(self):
        df = pd.DataFrame({"pickup_datetime": ["2022-01-01 08:00:00"]})
        result = convert_datetime_columns(df, [])
        assert not pd.api.types.is_datetime64_any_dtype(result["pickup_datetime"])
