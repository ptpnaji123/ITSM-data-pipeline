{{ config(
    materialized='table',
    schema='public'
) }}

SELECT
    "Ticket ID",
    "Category",
    "Sub-Category",
    "Priority",
    "Created Date",
    "Resolved Date",
    "Status",
    "Assigned Group",
    "Technician",
    "Customer Impact",
    "Resolution Time (Hrs)",
    "Year",
    "Month",
    "Day"
FROM public.itsm_tickets;
