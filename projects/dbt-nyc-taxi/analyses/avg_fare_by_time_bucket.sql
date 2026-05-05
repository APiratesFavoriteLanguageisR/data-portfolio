--Insight: Time of day shows more variation than day of week. 
-- Early Morning has the highest avg fare ($14.03), likely airport runs. Morning Rush has the lowest fare and tips. 
-- Overnight passengers tip the most generously.

SELECT
pickup_time_bucket,
Round(AVG(fare_amount), 2) as avg_fare,
Round(AVG(trip_duration_minutes), 2) as avg_trip_duration,
Round(AVG(tip_amount), 2) as avg_tip_amount,
COUNT(*) as trip_count
FROM {{ref('mart_trips')}}
GROUP BY pickup_time_bucket