{{ config(
    schema='public',
    materialized='table'  
) }}

SELECT
  "Ticket ID",
  "Category",
  "Sub-Category",
  "Priority",
  CAST("Created Date" AS TIMESTAMP) AS created_timestamp,
  CAST("Resolved Date" AS TIMESTAMP) AS resolved_timestamp,
  "Status",
  "Assigned Group",
  "Technician",
  "Customer Impact",
  CAST(NULLIF("Resolution Time (Hrs)", '') AS FLOAT) AS resolution_hours,
  "Year",
  "Month",
  "Day"
FROM {{ ref('itsm_tickets') }};
