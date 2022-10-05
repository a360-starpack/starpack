import pandas as pd
import pickle
import os
from typing import List
from pathlib import Path


def predict(model_paths: List[Path], patient_metrics: pd.DataFrame) -> pd.DataFrame:

    # Load Pretrained Model
    model_filepath = model_paths[0]
    with open(model_filepath, "rb") as pretrained_model_file:
        pretrained_model = pickle.load(pretrained_model_file)

    # Apply predictions to scoring file
    # Optional, but we will give back the input, with the predictions appended to the 'tgt_heart_disease' column.
    dfOut = patient_metrics
    dfOut["tgt_heart_disease"] = pretrained_model.predict(patient_metrics)

    # Read out the prediction
    return dfOut


# For testing, you can make sure this function properly runs
if __name__ == "__main__":
    input_path = Path(input("Please give the path to the input file: "))
    model_path = Path(input("Please give the path to your model file: "))

    input_type = input_path.suffix

    if input_type == "json":
        input = pd.read_json(input_path)
    elif input_type == ".csv":
        input = pd.read_csv(input_path)

    output = predict(input)

    print(output)
