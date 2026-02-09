"""
VISUAL ANALYTICS: Communicating Product Health and Retention Impact.
This script generates the final visual assets (Heatmaps/Violin plots) 
to present insights to stakeholders and product teams.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Setup
engine = create_engine("postgresql://postgres:J.e.s.u.s01*@localhost:5432/projects")

# VISUAL 1: COHORT RETENTION HEATMAP
# We use the SQL logic to get the cohort data
query = '''
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
    )
    -- Final Output for Python integration
    cohort_correlation AS (
        SELECT 
            * 
        FROM 
            cohort_counts
        ORDER BY 
            cohort_month, month_number;
    )
'''
sql_table = pd.read_sql(query, engine)

# Transform to matrix and calculate percentages
retention_matrix = sql_table.pivot(index='cohort_month', columns='month_number', values='active_users')
retention_matrix_pct = retention_matrix.div(retention_matrix.iloc[:, 0], axis=0)

# Format index for readability (e.g., July 2025)
retention_matrix_pct.index = pd.to_datetime(retention_matrix_pct.index).strftime('%B %Y')

sns.heatmap(retention_matrix_pct, annot=True, fmt='.1%', cmap="YlGnBu")
plt.title('Monthly User Retention Cohorts (%)', fontsize=15)
plt.show()

# VISUAL 2: LIFESPAN DISTRIBUTION (Violin Plot)
# This proves visually what the Pearson correlation told us
sns.violinplot(data=master_df, x='has_completed_profile', y='lifespan_days', palette="muted")
plt.title('Impact of Profile Completion on User Lifespan', fontsize=14)
plt.xticks([0, 1], ['Incomplete Profile', 'Completed Profile'])
plt.ylabel('Days of Retention')
plt.show()

# VISUAL 3: BUSINESS IMPACT (Retention Lift)
avg_aha = master_df[master_df['has_completed_profile'] == 1]['lifespan_days'].mean()
avg_control = master_df[master_df['has_completed_profile'] == 0]['lifespan_days'].mean()

plt.bar(['Control Group', 'Aha! Moment Group'], [avg_control, avg_aha], color=['gray', 'teal'])
plt.title('Average Lifespan Comparison')
plt.ylabel('Days')
plt.show()