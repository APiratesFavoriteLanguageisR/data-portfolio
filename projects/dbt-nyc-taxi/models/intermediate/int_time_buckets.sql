SELECT
trip_id,
pickup_hour,
CASE
    WHEN pickup_hour >= 5 and pickup_hour < 8 then 'Early Morning'
    WHEN pickup_hour >= 8 and pickup_hour < 11 then 'Morning Rush'
    WHEN pickup_hour >= 11 and pickup_hour < 16 then 'Midday'
    WHEN pickup_hour >= 16 and pickup_hour < 19 then 'Evening Rush'
    WHEN pickup_hour >= 19 and pickup_hour < 22 then 'Evening'
    WHEN pickup_hour >= 22 OR pickup_hour < 5 then 'Overnight'
    ELSE 'Unknown'
END AS pickup_time_bucket,
pickup_day_of_week,
is_weekend
FROM {{ ref('stg_yellow_trips') }}