SELECT
syt.trip_id,
syt.vendor_id,
syt.pickup_datetime,
syt.dropoff_datetime,
syt.passenger_count,
syt.rate_code,
syt.pickup_location_id,
syt.dropoff_location_id,
syt.trip_duration_minutes,
itb.pickup_hour,
itb.pickup_time_bucket, 
itb.pickup_day_of_week, 
itb.is_weekend, 
itc.trip_distance, 
itc.trip_category,
CASE
    WHEN itc.trip_category = 'Invalid Trip' THEN 0
    ELSE 1
END AS is_valid_trip,
ipt.payment_type, 
ipt.payment_type_description, 
ipt.fare_amount, 
ipt.extra, 
ipt.mta_tax, 
ipt.tip_amount, 
ipt.tolls_amount, 
ipt.imp_surcharge, 
ipt.airport_fee, 
ipt.total_amount, 
ipt.fare_per_mile
FROM {{ ref('stg_yellow_trips') }} AS syt
LEFT JOIN {{ ref('int_payment_type') }} AS ipt USING (trip_id)
LEFT JOIN {{ ref('int_time_buckets') }} AS itb USING (trip_id)
LEFT JOIN {{ ref('int_trip_categorization') }} AS itc USING (trip_id)