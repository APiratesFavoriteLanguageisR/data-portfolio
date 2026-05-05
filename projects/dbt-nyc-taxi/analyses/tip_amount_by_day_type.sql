-- Insight: Tip amount by day shows Sunday as the most generous tipping day ($2.55) and 
-- Wednesday as the lowest across fare, duration, and tip. Tip generally tracks with fare amount.

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
Round(AVG(trip_duration_minutes), 2) as avg_trip_duration,
Round(AVG(tip_amount), 2) as avg_tip_amount
FROM {{ref('mart_trips')}}
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week