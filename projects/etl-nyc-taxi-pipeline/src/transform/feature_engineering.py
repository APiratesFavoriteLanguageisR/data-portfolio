import pandas as pd
import logging


def add_trip_duration(df):
    """
    Create a trip duration feature in minutes.

    Uses pickup and dropoff timestamps to calculate trip duration.
    """

    if {"pickup_datetime", "dropoff_datetime"}.issubset(df.columns):

        df["trip_duration_minutes"] = (
            df["dropoff_datetime"] - df["pickup_datetime"]
        ).dt.total_seconds() / 60

    else:
        logging.warning(
            "Pickup or dropoff datetime columns missing. Trip duration feature skipped."
        )

    return df


def add_time_features(df):
    """
    Extract useful time-based features from pickup datetime.
    """

    if "pickup_datetime" in df.columns:

        df["pickup_hour"] = df["pickup_datetime"].dt.hour
        df["pickup_day_of_week"] = df["pickup_datetime"].dt.dayofweek
        df["is_weekend"] = df["pickup_day_of_week"].isin([5, 6])

    else:
        logging.warning(
            "Pickup datetime column missing. Time features skipped."
        )

    return df


def add_fare_per_mile(df):
    """
    Create a fare-per-mile metric.

    Useful for analyzing fare efficiency across trips.
    """

    if {"fare_amount", "trip_distance"}.issubset(df.columns):

        df["fare_per_mile"] = df["fare_amount"] / df["trip_distance"]

    else:
        logging.warning(
            "fare_amount or trip_distance missing. Fare per mile feature skipped."
        )

    return df


def apply_feature_engineering(df):
    """
    Apply all feature engineering transformations.
    """

    logging.info("Starting feature engineering")

    df = add_trip_duration(df)
    df = add_time_features(df)
    df = add_fare_per_mile(df)

    logging.info("Feature engineering complete")

    return df