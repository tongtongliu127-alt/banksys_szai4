import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_train_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "age": [51, 50, 35],
            "job": ["admin.", "services", "technician"],
            "marital": ["divorced", "married", "single"],
            "education": ["professional.course", "high.school", "university.degree"],
            "default": ["no", "unknown", "no"],
            "housing": ["yes", "yes", "no"],
            "loan": ["yes", "no", "no"],
            "contact": ["cellular", "cellular", "telephone"],
            "month": ["aug", "may", "jun"],
            "day_of_week": ["mon", "mon", "tue"],
            "duration": [4621, 4715, 300],
            "campaign": [1, 1, 2],
            "pdays": [112, 412, 999],
            "previous": [2, 2, 0],
            "poutcome": ["failure", "nonexistent", "success"],
            "emp_var_rate": [1.4, -1.8, -0.1],
            "cons_price_index": [90.81, 96.33, 94.0],
            "cons_conf_index": [-35.53, -40.58, -38.0],
            "lending_rate3m": [0.69, 4.05, 2.5],
            "nr_employed": [5219.74, 4974.79, 5100.0],
            "subscribe": ["no", "yes", "yes"],
        }
    )


@pytest.fixture
def sample_df_for_viz():
    """Larger sample for visualizer tests — covers all categories."""
    np.random.seed(42)
    n = 200
    jobs = ["admin.", "blue-collar", "technician", "services", "management"]
    marital = ["married", "single", "divorced"]
    education = ["high.school", "university.degree", "professional.course", "illiterate"]
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    days = ["mon", "tue", "wed", "thu", "fri"]
    outcomes = ["success", "failure", "nonexistent"]

    return pd.DataFrame(
        {
            "age": np.random.randint(18, 90, n),
            "job": np.random.choice(jobs, n),
            "marital": np.random.choice(marital, n),
            "education": np.random.choice(education, n),
            "default": np.random.choice(["yes", "no", "unknown"], n),
            "housing": np.random.choice(["yes", "no", "unknown"], n),
            "loan": np.random.choice(["yes", "no", "unknown"], n),
            "contact": np.random.choice(["cellular", "telephone"], n),
            "month": np.random.choice(months, n),
            "day_of_week": np.random.choice(days, n),
            "duration": np.random.randint(0, 5000, n),
            "campaign": np.random.randint(1, 10, n),
            "pdays": np.random.randint(0, 999, n),
            "previous": np.random.randint(0, 5, n),
            "poutcome": np.random.choice(outcomes, n),
            "emp_var_rate": np.random.uniform(-3, 3, n),
            "cons_price_index": np.random.uniform(90, 100, n),
            "cons_conf_index": np.random.uniform(-50, -30, n),
            "lending_rate3m": np.random.uniform(0, 5, n),
            "nr_employed": np.random.uniform(4900, 5300, n),
            "subscribe": np.random.choice(["yes", "no"], n, p=[0.3, 0.7]),
        }
    )
