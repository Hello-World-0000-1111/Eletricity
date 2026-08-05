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
        section[data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        section[data-testid="stSidebar"] .stMarkdown h1 {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        /* Customize Sidebar Radio Buttons */
        div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
            background-color: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            width: 100%;
            display: flex;
            align-items: center;
        }

        div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
            background-color: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.4);
            transform: translateX(4px);
        }

        div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-selected="true"] {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
            border-color: #3b82f6 !important;
            font-weight: 600;
        }

        /* Hide the default radio circle in Streamlit to make it look like a button tab list */
        div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label [data-testid="stMarkdownContainer"] p {
            font-size: 15px;
            color: #e2e8f0;
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
