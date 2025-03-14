{{ config(
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
FROM {{ source('public', 'itsm_tickets') }}  -- ✅ Use DBT source reference, avoid hardcoded schema
