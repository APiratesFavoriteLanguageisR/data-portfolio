-- Insight: Day of week has minimal impact on average fare (range: $12.15 - $13.72)
-- Friday and Sunday trend higher, likely due to longer airport/leisure trips
-- Saturday unexpectedly low, possibly reflecting shorter local trips

SELECT
pickup_day_of_week,
CASE
WHEN pickup_day_of_week = 0 THEN 'Monday'
WHEN pickup_day_of_week = 1 THEN 'Tuesday'
WHEN pickup_day_of_week = 2 THEN 'Wednesday'
WHEN pickup_day_of_week = 3 THEN 'Thursday'
WHEN pickup_day_of_week = 4 THEN 'Friday'
WHEN pickup_day_of_week = 5 THEN 'Saturday'
WHEN pickup_day_of_week = 6 THEN 'Sunday'
END AS day_of_week_name,
Round(AVG(fare_amount), 2) as avg_fare,
COUNT(*) as trip_count
FROM {{ref('mart_trips')}}
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week