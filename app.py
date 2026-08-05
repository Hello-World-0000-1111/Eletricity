import streamlit as st
import pandas as pd
from src.ui_components import apply_custom_theme
from src.model_integration import predict_electricity
from src.database import init_db, log_prediction, get_prediction_history, check_db_connection, is_sqlite_fallback
from src.export_utils import convert_to_csv, convert_to_pdf

# Initialize Database
init_db()

# Configure Streamlit page
st.set_page_config(
    page_title="Electricity Forecasting AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Dark Theme
apply_custom_theme()

def main():
    # Sidebar Logo and Navigation
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 25px; margin-top: -30px;'>
        <h1 style='font-size: 28px; margin: 0; background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ ElectraAI</h1>
        <p style='color: #64748b; font-size: 13px; margin-top: 5px;'>Demand Forecasting System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<p style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 1px; margin-bottom: 10px;'>Navigation</p>", unsafe_allow_html=True)
    page = st.sidebar.radio(
        "Navigation",
        options=["Predict", "History & Export", "About Model"],
        label_visibility="collapsed"
    )

    # System Status Card
    st.sidebar.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    db_connected = check_db_connection()
    if db_connected:
        if is_sqlite_fallback():
            db_status_color = "#f59e0b"
            db_status_text = "SQLite Fallback"
        else:
            db_status_color = "#10b981"
            db_status_text = "PostgreSQL Connected"
    else:
        db_status_color = "#ef4444"
        db_status_text = "Offline"
    
    st.sidebar.markdown(
        f"""
        <div style='background-color: rgba(30, 41, 59, 0.4); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);'>
            <h4 style='margin: 0 0 10px 0; color: #f8fafc; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>System Status</h4>
            <div style='display: flex; align-items: center; font-size: 12px; margin-bottom: 8px;'>
                <span style='height: 8px; width: 8px; background-color: {db_status_color}; border-radius: 50%; display: inline-block; margin-right: 8px;'></span>
                <span style='color: #94a3b8;'>Database: </span>
                <strong style='color: #e2e8f0; margin-left: 4px;'>{db_status_text}</strong>
            </div>
            <div style='display: flex; align-items: center; font-size: 12px;'>
                <span style='height: 8px; width: 8px; background-color: #3b82f6; border-radius: 50%; display: inline-block; margin-right: 8px;'></span>
                <span style='color: #94a3b8;'>Model: </span>
                <strong style='color: #e2e8f0; margin-left: 4px;'>XGBoost Active</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("⚡ Electricity Demand Forecasting")
    st.markdown("Predict future electricity demand based on environmental and socioeconomic factors.")

    if page == "Predict":

        st.subheader("Enter Prediction Parameters")
        
        # Form for input validation
        with st.form("prediction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                city_mapping = {"Islamabad": 0, "Karachi": 1, "Lahore": 2, "Peshawar": 3, "Quetta": 4}
                city_name = st.selectbox("City", options=list(city_mapping.keys()))
                city = city_mapping[city_name]
                
                temperature_c = st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=25.0)
            
            with col2:
                humidity_percent = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
                household_size = st.number_input("Household Size", min_value=1, max_value=20, value=4)
            
            with col3:
                income_mapping = {"High": 0, "Low": 1, "Middle": 2}
                income_name = st.selectbox("Income Level", options=list(income_mapping.keys()))
                income_level = income_mapping[income_name]
                
                power_outage_hours = st.number_input("Power Outage (Hours)", min_value=0.0, max_value=24.0, value=0.0)
            
            submitted = st.form_submit_button("Predict Electricity Usage")
            
            if submitted:
                with st.spinner("Generating prediction..."):
                    input_data = {
                        "city": city,
                        "temperature_c": temperature_c,
                        "humidity_percent": humidity_percent,
                        "household_size": household_size,
                        "income_level": income_level,
                        "power_outage_hours": power_outage_hours
                    }
                    
                    # Generate Prediction
                    prediction = predict_electricity(input_data)
                    
                    # Log to Database
                    logged = log_prediction(input_data, prediction, model_name="XGBoost")
                    
                    # Display Results
                    st.success("Prediction generated successfully!")
                    
                    # Styled Metric Card
                    st.metric(label="Predicted Electricity Demand (kWh)", value=f"{prediction} kWh", delta="Based on real-time factors")
                    
                    if not logged:
                        st.warning("Prediction was generated but could not be saved to the database. Check connection settings.")
                    elif is_sqlite_fallback():
                        st.info("💡 Saved to SQLite fallback database (Local).")

    elif page == "History & Export":
        st.subheader("Prediction History")
        
        history = get_prediction_history(limit=50)
        
        if not history:
            st.info("No prediction history found. Generate some predictions first!")
        else:
            # Convert to DataFrame for display
            df = pd.DataFrame([{
                "ID": r.id,
                "Time": r.timestamp.strftime("%Y-%m-%d %H:%M"),
                "City": r.city,
                "Temp (°C)": r.temperature_c,
                "Humidity (%)": r.humidity_percent,
                "Prediction (kWh)": r.predicted_electricity_kwh
            } for r in history])
            
            st.dataframe(df, use_container_width=True)
            
            st.markdown("### Export Data")
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = convert_to_csv(history)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name="electricity_predictions.csv",
                    mime="text/csv"
                )
                
            with col2:
                pdf_data = convert_to_pdf(history)
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_data,
                    file_name="electricity_predictions.pdf",
                    mime="application/pdf"
                )

    elif page == "About Model":
        st.subheader("📊 Model Performance & Evaluation")
        
        st.markdown("""
        This application is powered by an advanced machine learning pipeline. 
        Since this is a **regression task** (forecasting continuous electricity demand in kWh), standard classification metrics like Accuracy, Precision, Recall, and F1-Score do not apply. 
        Instead, we evaluate models using regression metrics: **Mean Absolute Error (MAE)**, **Mean Squared Error (MSE)**, and **Root Mean Squared Error (RMSE)**.
        """)

        # Highlight Metrics for current Production Model (XGBoost)
        st.markdown("### 🏆 Production Model: XGBoost")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="Mean Absolute Error (MAE)", value="4.49 kWh", delta="-0.19 kWh vs LSTM (Best)")
        with m_col2:
            st.metric(label="Mean Squared Error (MSE)", value="30.26", delta="-1.83 vs LSTM (Best)")
        with m_col3:
            st.metric(label="Root Mean Squared Error (RMSE)", value="5.50 kWh", delta="-0.16 kWh vs LSTM (Best)")

        # Comparison DataFrame
        st.markdown("### 📈 Model Comparison Summary")
        comparison_data = {
            "Model": ["XGBoost (Production)", "ARIMA", "LSTM", "SARIMA"],
            "MAE (Lower is Better)": [4.4858, 4.6749, 4.7017, 4.7201],
            "MSE (Lower is Better)": [30.2589, 31.9002, 32.0881, 32.4086],
            "RMSE (Lower is Better)": [5.5008, 5.6480, 5.6646, 5.6929]
        }
        df_comp = pd.DataFrame(comparison_data)
        st.dataframe(df_comp, use_container_width=True)

        # Tabs for Plots & Analysis
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Model Comparison Plots", 
            "⚡ XGBoost Predictions", 
            "🧠 LSTM Predictions", 
            "📈 ARIMA & SARIMA"
        ])
        
        with tab1:
            st.markdown("#### Evaluation Metric Visualizations")
            col_img1, col_img2, col_img3 = st.columns(3)
            with col_img1:
                try:
                    st.image("plot/Img14_MAE_Comparision.png", caption="MAE Comparison")
                except:
                    st.info("MAE Comparison plot not found.")
            with col_img2:
                try:
                    st.image("plot/Img15_MSE_Comparision.png", caption="MSE Comparison")
                except:
                    st.info("MSE Comparison plot not found.")
            with col_img3:
                try:
                    st.image("plot/Img16_RMSE_Comparision.png", caption="RMSE Comparison")
                except:
                    st.info("RMSE Comparison plot not found.")

        with tab2:
            st.markdown("#### XGBoost Model Performance")
            try:
                st.image("plot/Img12_XGBoost.png", caption="XGBoost Actual vs Predicted Consumption")
            except:
                st.info("XGBoost prediction plot not found.")

        with tab3:
            st.markdown("#### LSTM Model Performance")
            try:
                st.image("plot/Img13_LSTM_Model.png", caption="LSTM Actual vs Predicted Consumption")
            except:
                st.info("LSTM prediction plot not found.")

        with tab4:
            st.markdown("#### ARIMA & SARIMA Models")
            col_ts1, col_ts2 = st.columns(2)
            with col_ts1:
                try:
                    st.image("plot/Img10_ARIMA_Model.png", caption="ARIMA Forecast")
                except:
                    st.info("ARIMA plot not found.")
            with col_ts2:
                try:
                    st.image("plot/Img11_SARIMA_Model.png", caption="SARIMA Forecast")
                except:
                    st.info("SARIMA plot not found.")


if __name__ == "__main__":
    main()
