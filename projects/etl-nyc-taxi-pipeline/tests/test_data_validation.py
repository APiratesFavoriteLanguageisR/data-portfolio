import pandas as pd
import pytest
from src.transform.data_validation import remove_invalid_rows, enforce_numeric_types


def make_valid_row(**overrides):
    """Return a dict representing one valid trip record, with optional field overrides."""
    row = {
        "pickup_datetime": pd.Timestamp("2022-01-01 08:00:00"),
        "dropoff_datetime": pd.Timestamp("2022-01-01 08:30:00"),
        "passenger_count": 2,
        "trip_distance": 3.5,
        "fare_amount": 12.50,
    }
    row.update(overrides)
    return row


REQUIRED_COLS = ["pickup_datetime", "dropoff_datetime", "passenger_count", "trip_distance"]


class TestRemoveInvalidRows:

    def test_keeps_valid_rows(self):
        df = pd.DataFrame([make_valid_row(), make_valid_row()])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 2

    def test_removes_null_in_required_column(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(trip_distance=None),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_zero_passenger_count(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(passenger_count=0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_negative_passenger_count(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(passenger_count=-1),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_passenger_count_above_8(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(passenger_count=9),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_keeps_passenger_count_at_boundary_values(self):
        df = pd.DataFrame([
            make_valid_row(passenger_count=1),
            make_valid_row(passenger_count=8),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 2

    def test_removes_zero_trip_distance(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(trip_distance=0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_negative_trip_distance(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(trip_distance=-1.0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_zero_fare_amount(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(fare_amount=0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_negative_fare_amount(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(fare_amount=-5.0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_pickup_after_dropoff(self):
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(
                pickup_datetime=pd.Timestamp("2022-01-01 09:00:00"),
                dropoff_datetime=pd.Timestamp("2022-01-01 08:00:00"),
            ),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_removes_pickup_equal_to_dropoff(self):
        ts = pd.Timestamp("2022-01-01 08:00:00")
        df = pd.DataFrame([
            make_valid_row(),
            make_valid_row(pickup_datetime=ts, dropoff_datetime=ts),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 1

    def test_empty_dataframe_returns_empty(self):
        df = pd.DataFrame(columns=list(make_valid_row().keys()))
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 0

    def test_all_invalid_returns_empty(self):
        df = pd.DataFrame([
            make_valid_row(trip_distance=0),
            make_valid_row(fare_amount=0),
        ])
        result = remove_invalid_rows(df, REQUIRED_COLS)
        assert len(result) == 0


class TestEnforceNumericTypes:

    def test_converts_string_numbers_to_numeric(self):
        df = pd.DataFrame({"fare_amount": ["12.50", "7.00"]})
        result = enforce_numeric_types(df, ["fare_amount"])
        assert pd.api.types.is_numeric_dtype(result["fare_amount"])

    def test_coerces_invalid_string_to_nan(self):
        df = pd.DataFrame({"fare_amount": ["12.50", "not_a_number"]})
        result = enforce_numeric_types(df, ["fare_amount"])
        assert result["fare_amount"].isna().sum() == 1

    def test_already_numeric_columns_unchanged(self):
        df = pd.DataFrame({"fare_amount": [12.50, 7.00]})
        result = enforce_numeric_types(df, ["fare_amount"])
        assert list(result["fare_amount"]) == [12.50, 7.00]

    def test_missing_column_does_not_raise(self):
        df = pd.DataFrame({"fare_amount": [12.50]})
        result = enforce_numeric_types(df, ["fare_amount", "nonexistent_column"])
        assert "nonexistent_column" not in result.columns

    def test_multiple_columns_converted(self):
        df = pd.DataFrame({
            "fare_amount": ["12.50"],
            "trip_distance": ["3.5"],
            "passenger_count": ["2"],
        })
        result = enforce_numeric_types(df, ["fare_amount", "trip_distance", "passenger_count"])
        for col in ["fare_amount", "trip_distance", "passenger_count"]:
            assert pd.api.types.is_numeric_dtype(result[col])
