import streamlit as st

def apply_custom_theme():
    """
    Applies custom CSS to create a modern dark theme with glassmorphism effects.
    """
    st.markdown(
        """
        <style>
        /* Base Dark Theme */
        .stApp {
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Glassmorphism for containers and sidebars */
        .css-1d391kg, .css-12oz5g7 {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Input Elements */
        .stNumberInput > div > div > input, .stSelectbox > div > div > select {
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 10px;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
        }

        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #f8fafc;
            font-weight: 700;
        }
        
        /* Dataframes */
        .stDataFrame {
            background-color: #1e293b;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
