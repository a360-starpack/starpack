import gradio as gr
import pandas as pd
import requests
import io


def predict(age, sex, chest_pain, resting_blood_pressure, cholesterol, fbs, restecg, thalach, exang, oldpeak, slope, ca,
            thal):
    df = pd.DataFrame([{"age": age,
                        "sex": int(sex[0]),
                        "cp": int(chest_pain[0]),
                        "trestbps": resting_blood_pressure,
                        "chol": cholesterol,
                        "fbs": int(fbs),
                        "restecg": int(restecg[0]),
                        "thalach": thalach,
                        "exang": int(exang),
                        "oldpeak": oldpeak,
                        "slope": int(slope[0]),
                        "ca": ca,
                        "thal": int(thal[0]),
                        }])

    bytes_input = df.to_csv(index=False).encode()
    request_file = {"file": (f"test.csv", bytes_input, "application/vnd.ms-excel")}

    output_response = requests.post("http://localhost/models/predict/starpack_deployment", files=request_file)
    print(output_response.text)

    prediction = bool(pd.read_csv(io.StringIO(output_response.text))["tgt_heart_disease"][0])

    return str(prediction)


gradio_app = gr.Interface(fn=predict,
                          inputs=[
                              "number",
                              gr.Radio(["0: Male", "1: Female"]),
                              gr.Radio(["0: Typical Angina", "1: Atypical Angina", "2: Non-anginal Pain",
                                        "3: Asymptomatic"]),
                              "number",
                              "number",
                              gr.Checkbox(),
                              gr.Radio(["0: Normal", "1: ST-T wave abnormality", "2: Left ventricular hypertrophy"]),
                              "number",
                              gr.Checkbox(),
                              "number",
                              gr.Radio(["0: Positive", "1: Flat", "2: Negative"]),
                              gr.Slider(minimum=0, maximum=4),
                              gr.Radio(["1: Normal", "2: Fixed Defect", "3: Reversable Defect"])
                          ],
                          outputs=["text"],
                          )

if __name__ == "__main__":
    gradio_app.launch()
