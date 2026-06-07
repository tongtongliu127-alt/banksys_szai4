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
