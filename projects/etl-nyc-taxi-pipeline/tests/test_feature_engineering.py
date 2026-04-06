import pandas as pd
import pytest
from src.transform.feature_engineering import (
    add_trip_duration,
    add_time_features,
    add_fare_per_mile,
)


class TestAddTripDuration:

    def test_calculates_duration_in_minutes(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-01 08:00:00")],
            "dropoff_datetime": [pd.Timestamp("2022-01-01 08:30:00")],
        })
        result = add_trip_duration(df)
        assert result["trip_duration_minutes"].iloc[0] == 30.0

    def test_duration_is_fractional_minutes(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-01 08:00:00")],
            "dropoff_datetime": [pd.Timestamp("2022-01-01 08:00:45")],
        })
        result = add_trip_duration(df)
        assert result["trip_duration_minutes"].iloc[0] == pytest.approx(0.75)

    def test_missing_pickup_column_skips_feature(self):
        df = pd.DataFrame({"dropoff_datetime": [pd.Timestamp("2022-01-01 08:30:00")]})
        result = add_trip_duration(df)
        assert "trip_duration_minutes" not in result.columns

    def test_missing_dropoff_column_skips_feature(self):
        df = pd.DataFrame({"pickup_datetime": [pd.Timestamp("2022-01-01 08:00:00")]})
        result = add_trip_duration(df)
        assert "trip_duration_minutes" not in result.columns


class TestAddTimeFeatures:

    def test_extracts_pickup_hour(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-01 14:35:00")]
        })
        result = add_time_features(df)
        assert result["pickup_hour"].iloc[0] == 14

    def test_extracts_day_of_week(self):
        # 2022-01-01 is a Saturday (dayofweek == 5)
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-01 08:00:00")]
        })
        result = add_time_features(df)
        assert result["pickup_day_of_week"].iloc[0] == 5

    def test_is_weekend_true_for_saturday(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-01 08:00:00")]  # Saturday
        })
        result = add_time_features(df)
        assert result["is_weekend"].iloc[0] == True

    def test_is_weekend_true_for_sunday(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-02 08:00:00")]  # Sunday
        })
        result = add_time_features(df)
        assert result["is_weekend"].iloc[0] == True

    def test_is_weekend_false_for_weekday(self):
        df = pd.DataFrame({
            "pickup_datetime": [pd.Timestamp("2022-01-03 08:00:00")]  # Monday
        })
        result = add_time_features(df)
        assert result["is_weekend"].iloc[0] == False

    def test_missing_pickup_column_skips_features(self):
        df = pd.DataFrame({"fare_amount": [12.50]})
        result = add_time_features(df)
        assert "pickup_hour" not in result.columns
        assert "pickup_day_of_week" not in result.columns
        assert "is_weekend" not in result.columns


class TestAddFarePerMile:

    def test_calculates_fare_per_mile(self):
        df = pd.DataFrame({
            "fare_amount": [10.0],
            "trip_distance": [2.0],
        })
        result = add_fare_per_mile(df)
        assert result["fare_per_mile"].iloc[0] == pytest.approx(5.0)

    def test_fare_per_mile_with_fractional_distance(self):
        df = pd.DataFrame({
            "fare_amount": [7.50],
            "trip_distance": [2.5],
        })
        result = add_fare_per_mile(df)
        assert result["fare_per_mile"].iloc[0] == pytest.approx(3.0)

    def test_missing_fare_amount_skips_feature(self):
        df = pd.DataFrame({"trip_distance": [2.0]})
        result = add_fare_per_mile(df)
        assert "fare_per_mile" not in result.columns

    def test_missing_trip_distance_skips_feature(self):
        df = pd.DataFrame({"fare_amount": [10.0]})
        result = add_fare_per_mile(df)
        assert "fare_per_mile" not in result.columns
