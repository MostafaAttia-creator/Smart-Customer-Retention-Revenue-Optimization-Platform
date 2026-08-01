import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go


model = joblib.load(r"models\final_model.pkl")
preprocessor = joblib.load(r"models\preprocessor.pkl")


st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn Prediction")
st.write("Machine Learning system to predict customer churn risk and support retention decisions.")

st.sidebar.header("Customer Information")

with st.sidebar.expander("👤 Demographics", expanded=True):
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["Yes", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.number_input("Tenure Months", min_value=0, max_value=100, value=12)

with st.sidebar.expander("📡 Services", expanded=False):
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security", ["Yes", "No"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No"])
    device_protection = st.selectbox("Device Protection", ["Yes", "No"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No"])

with st.sidebar.expander("💳 Billing", expanded=False):
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment = st.selectbox("Payment Method", ["Bank Withdrawal", "Credit Card", "Mailed Check"])
    monthly_charge = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
    total_charge = st.number_input("Total Charges", min_value=0.0, value=1000.0)

predict = st.sidebar.button("Predict Churn", use_container_width=True)


def make_gauge(probability):
    if probability >= 0.7:
        color = "#e05252"
    elif probability >= 0.4:
        color = "#e0a952"
    else:
        color = "#4caf6f"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number={"suffix": "%", "font": {"size": 40}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 40], "color": "rgba(76,175,111,0.15)"},
                {"range": [40, 70], "color": "rgba(224,169,82,0.15)"},
                {"range": [70, 100], "color": "rgba(224,82,82,0.15)"},
            ],
        },
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


if predict:

    customer = pd.DataFrame({
        "Gender": [gender],
        "Senior Citizen": [senior],
        "Partner": [partner],
        "Dependents": [dependents],
        "Tenure Months": [tenure],
        "Phone Service": [phone_service],
        "Multiple Lines": [multiple_lines],
        "Internet Service": [internet_service],
        "Online Security": [online_security],
        "Online Backup": [online_backup],
        "Device Protection": [device_protection],
        "Tech Support": [tech_support],
        "Streaming TV": [streaming_tv],
        "Streaming Movies": [streaming_movies],
        "Contract": [contract],
        "Paperless Billing": [paperless],
        "Payment Method": [payment],
        "Monthly Charges": [monthly_charge],
        "Total Charges": [total_charge]
    })

    processed_customer = preprocessor.transform(customer)
    probability = model.predict_proba(processed_customer)[0][1]
    prediction = probability >= 0.5

    if probability >= 0.7:
        risk = "High Risk"
    elif probability >= 0.4:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    st.subheader("Prediction Result")

    col1, col2 = st.columns([1, 1])

    with col1:
        if prediction:
            st.error("⚠️ Customer is likely to churn")
        else:
            st.success("✅ Customer is likely to stay")

        st.info(f"Customer Risk Level: {risk}")

        st.write("**Key inputs used:**")
        st.write(f"- Contract: {contract}")
        st.write(f"- Tenure: {tenure} months")
        st.write(f"- Monthly Charges: ${monthly_charge:.2f}")
        st.write(f"- Internet Service: {internet_service}")

    with col2:
        st.plotly_chart(make_gauge(probability), use_container_width=True)

else:
    st.info("Fill in the customer details on the left and click **Predict Churn** to see the result.")
