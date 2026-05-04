SELECT
trip_id,
payment_type,
CASE
    WHEN payment_type = '1' THEN 'Credit Card'
    WHEN payment_type = '2' THEN 'Cash'
    WHEN payment_type = '3' THEN 'No Charge'
    WHEN payment_type = '4' THEN 'Dispute'
    WHEN payment_type = '5' THEN 'Unknown'
    WHEN payment_type = '6' THEN 'Voided Trip'
    ELSE 'Unknown'
END AS payment_type_description,
fare_amount,
extra,
mta_tax,
tip_amount,
tolls_amount,
imp_surcharge,
airport_fee,
total_amount,
fare_per_mile
FROM {{ ref('stg_yellow_trips') }}