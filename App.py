import streamlit as st
import pandas as pd
import joblib


model = joblib.load(
    r"D:\Projects\Smart Customer Retention & Revenue Optimization Platform\models\final_model.pkl"
)

preprocessor = joblib.load(
    r"D:\Projects\Smart Customer Retention & Revenue Optimization Platform\models\preprocessor.pkl"
)


st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)


st.title("📊 Customer Churn Prediction")

st.write(
    "Machine Learning system to predict customer churn risk and support retention decisions."
)


st.sidebar.header("Customer Information")


gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)


senior = st.sidebar.selectbox(
    "Senior Citizen",
    ["Yes", "No"]
)


partner = st.sidebar.selectbox(
    "Partner",
    ["Yes", "No"]
)


dependents = st.sidebar.selectbox(
    "Dependents",
    ["Yes", "No"]
)


tenure = st.sidebar.number_input(
    "Tenure Months",
    min_value=0,
    max_value=100,
    value=12
)


phone_service = st.sidebar.selectbox(
    "Phone Service",
    ["Yes", "No"]
)


multiple_lines = st.sidebar.selectbox(
    "Multiple Lines",
    ["Yes", "No"]
)


internet_service = st.sidebar.selectbox(
    "Internet Service",
    [
        "DSL",
        "Fiber optic",
        "No"
    ]
)


online_security = st.sidebar.selectbox(
    "Online Security",
    ["Yes", "No"]
)


online_backup = st.sidebar.selectbox(
    "Online Backup",
    ["Yes", "No"]
)


device_protection = st.sidebar.selectbox(
    "Device Protection",
    ["Yes", "No"]
)


tech_support = st.sidebar.selectbox(
    "Tech Support",
    ["Yes", "No"]
)


streaming_tv = st.sidebar.selectbox(
    "Streaming TV",
    ["Yes", "No"]
)


streaming_movies = st.sidebar.selectbox(
    "Streaming Movies",
    ["Yes", "No"]
)


contract = st.sidebar.selectbox(
    "Contract",
    [
        "Month-to-month",
        "One year",
        "Two year"
    ]
)


paperless = st.sidebar.selectbox(
    "Paperless Billing",
    ["Yes", "No"]
)


payment = st.sidebar.selectbox(
    "Payment Method",
    [
        "Bank Withdrawal",
        "Credit Card",
        "Mailed Check"
    ]
)


monthly_charge = st.sidebar.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=70.0
)


total_charge = st.sidebar.number_input(
    "Total Charges",
    min_value=0.0,
    value=1000.0
)



predict = st.button(
    "Predict Churn"
)



if predict:

    customer = pd.DataFrame({

        "Gender":[gender],

        "Senior Citizen":[senior],

        "Partner":[partner],

        "Dependents":[dependents],

        "Tenure Months":[tenure],

        "Phone Service":[phone_service],

        "Multiple Lines":[multiple_lines],

        "Internet Service":[internet_service],

        "Online Security":[online_security],

        "Online Backup":[online_backup],

        "Device Protection":[device_protection],

        "Tech Support":[tech_support],

        "Streaming TV":[streaming_tv],

        "Streaming Movies":[streaming_movies],

        "Contract":[contract],

        "Paperless Billing":[paperless],

        "Payment Method":[payment],

        "Monthly Charges":[monthly_charge],

        "Total Charges":[total_charge]

    })


    processed_customer = preprocessor.transform(
        customer
    )


    probability = model.predict_proba(
        processed_customer
    )[0][1]


    prediction = (
        probability >= 0.5
    )


    st.subheader(
        "Prediction Result"
    )


    if prediction:

        st.error(
            "⚠️ Customer is likely to churn"
        )

    else:

        st.success(
            "✅ Customer is likely to stay"
        )


    st.metric(
        "Churn Probability",
        f"{probability:.2%}"
    )


    if probability >= 0.7:

        risk = "High Risk"

    elif probability >= 0.4:

        risk = "Medium Risk"

    else:

        risk = "Low Risk"


    st.info(
        f"Customer Risk Level: {risk}"
    )