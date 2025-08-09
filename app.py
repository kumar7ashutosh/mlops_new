import streamlit as st
import pandas as pd
from src.utils.main_utils import load_object

def main():
    st.title("Insurance Prediction")

    # Load preprocessor and model (adjust paths as needed)
    preprocessor = load_object("artifact/08_09_2025_11_49_57/data_transformation/transformed_object/preprocessing.pkl")
    model = load_object("artifact/08_09_2025_11_49_57/model_trainer/trained_model/model.pkl")

    # User inputs
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Age = st.number_input("Age", 18, 100, 30)
    Driving_License = st.selectbox("Driving License", [0,1])
    Region_Code = st.number_input("Region Code", 0, 1000, 28)
    Previously_Insured = st.selectbox("Previously Insured", [0,1])
    Vehicle_Age = st.selectbox("Vehicle Age", ["< 1 Year", "1-2 Year", "> 2 Years"])
    Vehicle_Damage = st.selectbox("Vehicle Damage", ["Yes", "No"])
    Annual_Premium = st.number_input("Annual Premium", 0.0, 100000.0, 30000.0)
    Policy_Sales_Channel = st.number_input("Policy Sales Channel", 0, 200, 152)
    Vintage = st.number_input("Vintage", 0, 365, 150)
    vehicle_age_options = ["< 1 Year", "1-2 Year", "> 2 Years"]

    # Construct dataframe for prediction (raw input)
    input_dict = {
    # all other columns raw
    "Age": [Age],
    "Gender": [Gender],
    "Driving_License": [Driving_License],
    "Region_Code": [Region_Code],
    "Previously_Insured": [Previously_Insured],
    "Annual_Premium": [Annual_Premium],
    "Policy_Sales_Channel": [Policy_Sales_Channel],
    "Vintage": [Vintage],
  }

    for option in vehicle_age_options:
        col_name = "Vehicle_Age_" + option.replace("< ", "lt_").replace("> ", "gt_").replace(" ", "_")
        input_dict[col_name] = [1 if Vehicle_Age == option else 0]

    input_dict["Vehicle_Damage_Yes"] = [1 if Vehicle_Damage == "Yes" else 0]
    input_df = pd.DataFrame(input_dict)

    if st.button("Predict"):
        # Preprocess input
        input_transformed = preprocessor.transform(input_df)

        # Predict
        prediction = model.predict(input_transformed)

        # Show result
        st.success(f"Prediction: {'Valid' if prediction[0]==1 else 'Invalid'}")

if __name__ == "__main__":
    
    main()
