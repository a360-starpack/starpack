import pandas as pd
import pickle
import os
from typing import Any
from pathlib import Path


def predict(model: Any, patient_metrics: pd.DataFrame) -> pd.DataFrame:

    # Apply predictions to scoring file
    # Optional, but we will give back the input, with the predictions appended to the 'tgt_heart_disease' column.
    dfOut = patient_metrics
    dfOut["tgt_heart_disease"] = model.predict(patient_metrics)

    # Read out the prediction
    return dfOut


# For testing, you can make sure this function properly runs
if __name__ == "__main__":
    input_path = Path(input("Please give the path to the input file: "))
    model_paths = [Path(input("Please give the path to your model file: "))]

    input_type = input_path.suffix

    if input_type == "json":
        input = pd.read_json(input_path)
    elif input_type == ".csv":
        input = pd.read_csv(input_path)

    output = predict(model_paths, input)

    print(output)
