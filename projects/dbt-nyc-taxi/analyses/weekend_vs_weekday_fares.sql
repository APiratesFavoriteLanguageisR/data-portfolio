--Insight: Weekend vs weekday comparison shows minimal differences across fare, trip duration, and fare per mile.
-- Weekdays have 2.4x more trips. Pricing appears stable across day types.

SELECT
is_weekend,
Round(AVG(fare_amount), 2) as avg_fare,
Round(AVG(trip_duration_minutes), 2) as avg_trip_duration,
Round(AVG(fare_per_mile), 2) as avg_fare_per_mile,
COUNT(*) as trip_count
FROM {{ref('mart_trips')}}
WHERE is_valid_trip = 1
GROUP BY is_weekend