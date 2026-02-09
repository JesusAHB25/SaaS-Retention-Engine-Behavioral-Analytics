"""
PIPELINE LOGIC: Automated ETL and Behavioral Statistics.
This script extracts raw event data, processes user lifespans, 
and validates hypotheses using SciPy correlation tests.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine

# DATABASE CONNECTION
db_url = "postgresql://postgres:J.e.s.u.s01*@localhost:5432/projects"
engine = create_engine(db_url)

# DATA INGESTION
users_df = pd.read_sql("SELECT * FROM users", engine)
events_df = pd.read_sql("SELECT * FROM events", engine)

# Ensure datetime format for accurate calculations
users_df["signup_date"] = pd.to_datetime(users_df["signup_date"])
events_df["timestamp"] = pd.to_datetime(events_df["timestamp"])

# DATA ENGINEERING
# Calculate the last activity per user to define 'Lifespan'
last_event = events_df.groupby("user_id")["timestamp"].max().reset_index()
last_event.columns = ["user_id", "last_event"]

# Merge activity with user data
master_df = pd.merge(users_df, last_event, on="user_id", how="left")

# Calculate Lifespan in Days (The 'Y' variable for our analysis)
master_df["lifespan_days"] = (master_df["last_event"] - master_df["signup_date"]).dt.days
master_df["lifespan_days"] = master_df["lifespan_days"].fillna(0)

# Identify users who completed the profile (Aha! Moment - The 'X' variable)
# Feature_id 2 = profile_completion
completers = events_df[events_df["feature_id"] == 2]["user_id"].unique()
master_df["has_completed_profile"] = master_df["user_id"].isin(completers).astype(int)

# STATISTICAL VALIDATION (SciPy)
# Quantifying the correlation between profile completion and retention
x = master_df['has_completed_profile']
y = master_df['lifespan_days']
correlation, p_value = stats.pearsonr(x, y)

print(f"Pearson Correlation: {correlation:.4f}")
print(f"P-Value: {p_value:.4e}")
