import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


st.text("test_file")


@st.cache
def load_data():
    working_dir = Path(__file__).parent.resolve()
    df = pd.read_csv(working_dir / "heart_disease_score.csv")

    return df


heart_disease_df = load_data()

st.table(heart_disease_df)
