import pandas as pd
from src.transform.clean_columns import clean_column_names, drop_unused_columns


class TestCleanColumnNames:

    def test_converts_to_lowercase(self):
        df = pd.DataFrame(columns=["TripDistance", "FareAmount"])
        result = clean_column_names(df)
        assert list(result.columns) == ["tripdistance", "fareamount"]

    def test_replaces_spaces_with_underscores(self):
        df = pd.DataFrame(columns=["trip distance", "fare amount"])
        result = clean_column_names(df)
        assert list(result.columns) == ["trip_distance", "fare_amount"]

    def test_strips_leading_and_trailing_whitespace(self):
        df = pd.DataFrame(columns=[" pickup_datetime ", " dropoff_datetime "])
        result = clean_column_names(df)
        assert list(result.columns) == ["pickup_datetime", "dropoff_datetime"]

    def test_combined_cleaning(self):
        df = pd.DataFrame(columns=[" Trip Distance ", "FARE AMOUNT"])
        result = clean_column_names(df)
        assert list(result.columns) == ["trip_distance", "fare_amount"]

    def test_already_clean_columns_unchanged(self):
        df = pd.DataFrame(columns=["pickup_datetime", "trip_distance"])
        result = clean_column_names(df)
        assert list(result.columns) == ["pickup_datetime", "trip_distance"]


class TestDropUnusedColumns:

    def test_drops_specified_columns(self):
        df = pd.DataFrame(columns=["pickup_datetime", "store_and_fwd_flag", "ratecode_id"])
        result = drop_unused_columns(df, ["store_and_fwd_flag", "ratecode_id"])
        assert list(result.columns) == ["pickup_datetime"]

    def test_ignores_columns_not_in_dataframe(self):
        df = pd.DataFrame(columns=["pickup_datetime", "trip_distance"])
        result = drop_unused_columns(df, ["nonexistent_column"])
        assert list(result.columns) == ["pickup_datetime", "trip_distance"]

    def test_empty_drop_list_leaves_dataframe_unchanged(self):
        df = pd.DataFrame(columns=["pickup_datetime", "trip_distance"])
        result = drop_unused_columns(df, [])
        assert list(result.columns) == ["pickup_datetime", "trip_distance"]

    def test_partial_match_only_drops_existing(self):
        df = pd.DataFrame(columns=["pickup_datetime", "store_and_fwd_flag"])
        result = drop_unused_columns(df, ["store_and_fwd_flag", "nonexistent_column"])
        assert list(result.columns) == ["pickup_datetime"]
