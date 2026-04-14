SELECT
    {{ dbt_utils.generate_surrogate_key([
    'pickup_datetime', 
    'pickup_location_id', 
    'vendor_id',
    'dropoff_datetime',
    'dropoff_location_id',
    'total_amount'
    ]) }} AS trip_id
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    imp_surcharge,
    airport_fee,
    total_amount,
    pickup_location_id,
    dropoff_location_id,
    data_file_year,
    data_file_month,
    trip_duration_minutes,
    pickup_hour,
    pickup_day_of_week,
    is_weekend,
    fare_per_mile


FROM {{ source('yellow_trips', 'yellow_trips') }}