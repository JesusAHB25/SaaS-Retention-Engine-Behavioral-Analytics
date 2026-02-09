SaaS Retention Engine & Behavioral Analytics 🤖🧿
<p align="center"> <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"> <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"> <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"> <img src="https://img.shields.io/badge/SciPy-%238CAAE6.svg?style=for-the-badge&logo=scipy&logoColor=white" alt="SciPy"> <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"> <img src="https://img.shields.io/badge/Seaborn-%234470AD.svg?style=for-the-badge&logo=Seaborn&logoColor=white" alt="Seaborn"> </p>

📈 High-Level Strategy & Insights
<p align="center"> <a href="YOUR_NOTION_LINK_HERE"> <img src="https://img.shields.io/badge/Notion-View_Executive_Report-000000?style=for-the-badge&logo=notion&logoColor=white" alt="Notion Badge"> </a>


<em>Visit the full case study for business recommendations and the behavioral roadmap.</em> </p>

📊 Project Overview
This project develops a data-driven engine to identify the behavioral drivers of user loyalty in a SaaS environment. As a Mathematics Student and Aspiring Data Scientist, I designed an end-to-end pipeline that simulates user behavior, processes event logs via PostgreSQL, and applies Pearson Correlation to validate the "Aha! Moment." The goal is to provide a scientific basis for product onboarding optimizations.

🏗️ Phase 0: Data Engineering & Pre-Processing
🧪 Behavioral Simulation (Synthetic Data)
To ensure a high-fidelity environment, I architected a simulation script using NumPy to generate 600 unique users and thousands of event logs:

Controlled Logic: Programmed differentiated activity paths for "Retained" vs. "Churned" users to test the sensitivity of statistical models.

Feature Catalog: Defined core interactions including login, profile_completion (Feature ID 2), and social_invite.

🏗️ Relational Architecture (Star Schema)
I transformed simulated raw data into a Relational Star Schema within PostgreSQL. This design decouples descriptive user dimensions from the transactional fact table (events), enabling efficient cohort processing.

🛠️ Phase 1: The Retention Logic (SQL CTEs)
The core analytical engine resides in a robust SQL pipeline. I developed a Common Table Expression (CTE) to calculate the "Age Month" of each user, which serves as the foundation for the Retention Matrix:

SQL

WITH cohort_items AS (
    SELECT user_id, DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),
user_activities AS (
    SELECT 
        e.user_id, 
        c.cohort_month,
        (EXTRACT(YEAR FROM e.timestamp) - EXTRACT(YEAR FROM c.cohort_month)) * 12 + 
        (EXTRACT(MONTH FROM e.timestamp) - EXTRACT(MONTH FROM c.cohort_month)) AS month_number
    FROM events e
    JOIN cohort_items c ON e.user_id = c.user_id
)
SELECT cohort_month, month_number, COUNT(DISTINCT user_id) as active_users
FROM user_activities GROUP BY 1, 2;
🔬 Phase 2: Exploratory Data Analysis (EDA)
📈 Cohort Retention & Churn Velocity
Discovery: The heatmap identifies a critical "Retention Leak" in Month 1.

Finding: Retention stabilizes after the second month for users who engage early, suggesting that the first 30 days are the highest-leverage period for user intervention.

🎯 The "Aha! Moment" Validation (Technical Hook)
[!IMPORTANT] Scientific Insight: Using SciPy, I calculated a Pearson Correlation of 0.7459 between has_completed_profile and lifespan_days. With a P-Value of 1.28e-107, we have mathematically proven that Profile Completion (Feature ID 2) is not just an event, but the primary predictor of long-term retention.

🎻 Distribution Density
The Violin Plot analysis reveals that users who reach the "Aha! Moment" show a significantly higher density of active days (40-120 range) compared to the control group, which typically churns within 10 days.

🛠️ Tech Stack & Requirements
Core: Python (3.x), SQL (PostgreSQL).

Libraries: Pandas, NumPy, SciPy (Statistics), SQLAlchemy, Seaborn, Matplotlib.

Environment: Jupyter Notebooks.

📂 Repository Structure
Plaintext

├── data_preprocessing.ipynb # Phase 0: Synthetic simulation and SQL migration
├── database_logic.sql       # Phase 1: Cohort Engine and relational views
├── data_pipeline.py         # Modular ETL: Lifespan calculation & SciPy tests
├── visualizations.py        # Phase 2: Seaborn Heatmaps and Violin Plots
├── SaaS Retention Engine.ipynb # Full project implementation & analysis
└── requirements.txt         # Project dependencies
Developed by Jesús | Mathematics Student & Aspiring Data Scientist 🤖🧿
