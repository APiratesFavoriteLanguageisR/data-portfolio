SELECT
trip_id,
trip_distance,
CASE
    WHEN trip_distance > 0 and trip_distance <= 1 THEN 'Short Trip'
    WHEN trip_distance > 1 and trip_distance <= 3 THEN 'Medium Trip'
    WHEN trip_distance > 3 and trip_distance <=100 THEN 'Long Trip'
    WHEN trip_distance > 100 THEN 'Very Long Trip'
    WHEN trip_distance <= 0 THEN 'Invalid Trip'
    ELSE 'Unknown'
END as trip_category
FROM {{ ref('stg_yellow_trips') }}