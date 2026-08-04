import pandas as pd
from fpdf import FPDF
import io

def convert_to_csv(history_records):
    """
    Converts a list of PredictionHistory objects to a CSV byte string.
    """
    data = []
    for r in history_records:
        data.append({
            "ID": r.id,
            "Timestamp": r.timestamp,
            "City": r.city,
            "Temperature (C)": r.temperature_c,
            "Humidity (%)": r.humidity_percent,
            "Household Size": r.household_size,
            "Income Level": r.income_level,
            "Power Outage Hours": r.power_outage_hours,
            "Prediction (kWh)": r.predicted_electricity_kwh,
            "Model": r.model_used
        })
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')

def convert_to_pdf(history_records):
    """
    Converts a list of PredictionHistory objects to a PDF byte string.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Electricity Forecasting Prediction History", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=8)
    
    # Headers
    headers = ["ID", "Time", "Temp", "Hum", "Prediction", "Model"]
    col_widths = [10, 40, 20, 20, 30, 40]
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, str(header), border=1, align="C")
    pdf.ln(10)
    
    # Data rows
    for r in history_records:
        pdf.cell(col_widths[0], 10, str(r.id), border=1, align="C")
        pdf.cell(col_widths[1], 10, str(r.timestamp.strftime("%Y-%m-%d %H:%M")), border=1, align="C")
        pdf.cell(col_widths[2], 10, f"{r.temperature_c:.1f}", border=1, align="C")
        pdf.cell(col_widths[3], 10, f"{r.humidity_percent:.0f}", border=1, align="C")
        pdf.cell(col_widths[4], 10, f"{r.predicted_electricity_kwh:.2f}", border=1, align="C")
        pdf.cell(col_widths[5], 10, str(r.model_used), border=1, align="C")
        pdf.ln(10)
        
    pdf_bytes = pdf.output()
    return bytes(pdf_bytes)
