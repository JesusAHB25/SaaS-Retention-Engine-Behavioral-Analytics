/* COHORT RETENTION ENGINE
   Objective: Segment users by signup month and track activity over time.
*/

WITH cohort_items AS (
    -- Step 1: Define the "Birth Month" for each user
    SELECT 
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM 
        users
),
user_activities AS (
    -- Step 2: Calculate the "Age Month" (distance from signup to event)
    SELECT 
        e.user_id,
        c.cohort_month,
        (EXTRACT(YEAR FROM e.timestamp) - EXTRACT(YEAR FROM c.cohort_month)) * 12 + 
        (EXTRACT(MONTH FROM e.timestamp) - EXTRACT(MONTH FROM c.cohort_month)) AS month_number
    FROM 
        events e
    JOIN 
        cohort_items c ON e.user_id = c.user_id
),
cohort_counts AS (
    -- Step 3: Aggregate unique active users per cohort and month
    SELECT 
        cohort_month,
        month_number,
        COUNT(DISTINCT user_id) AS active_users
    FROM 
        user_activities
    GROUP BY 
        cohort_month, month_number
),
cohort_correlation AS (
    SELECT 
        * 
    FROM
        cohort_counts
    ORDER BY
        cohort_month, month_number
)

SELECT * FROM cohort_correlation;
