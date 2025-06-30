import streamlit as st

def apply_custom_styles():
    """Apply custom chestnut brown and yellow ochre gradient styles"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');
    
    /* CSS Variables for Colors */
    :root {
        --chestnut-brown: #954535;
        --dark-chestnut: #7a3529;
        --light-chestnut: #b85a47;
        --yellow-ochre: #cc9900;
        --light-ochre: #e6b800;
        --dark-ochre: #b38600;
        --cream: #f5f1e8;
        --warm-white: #fdfcf7;
        --text-dark: #3e2723;
        --text-light: #6d4c41;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, 
            var(--warm-white) 0%, 
            var(--cream) 50%, 
            #f0e6d2 100%);
        font-family: 'Source Sans Pro', sans-serif;
        color: var(--text-dark);
    }
    
    .stFont {
        font-family: 'Source Sans Pro', sans-serif;
        color: var(--text-dark);
    }
    
    /* Title Styling */
    .main .block-container h1 {
        font-family: 'Playfair Display', serif;
        background: linear-gradient(45deg, var(--chestnut-brown), var(--yellow-ochre));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(149, 69, 53, 0.1);
        color: var(--text-dark);
    }
    
    /* Caption/Subtitle Styling */
    .main .block-container p {
        color: var(--text-dark);
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Headers */
    .main .block-container h2, .main .block-container h3 {
        font-family: 'Playfair Display', serif;
        color: var(--chestnut-brown);
        border-bottom: 2px solid var(--yellow-ochre);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, var(--chestnut-brown), var(--dark-chestnut));
        border-radius: 10px 10px 0 0;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: white;
        width: 100%;
        font-weight: 600;
        border-radius: 8px;
        margin: 0 0.25rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, var(--yellow-ochre), var(--light-ochre)) !important;
        color: var(--text-dark) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Tab Content */
    .stTabs [data-baseweb="tab-panel"] {
        background: var(--warm-white);
        border-radius: 0 0 10px 10px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(149, 69, 53, 0.1);
        border: 1px solid var(--light-chestnut);
        border-top: none;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--chestnut-brown), var(--yellow-ochre));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(149, 69, 53, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, var(--dark-chestnut), var(--dark-ochre));
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(149, 69, 53, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(149, 69, 53, 0.3);
    }
    
    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(45deg, var(--yellow-ochre), var(--light-ochre));
        color: var(--text-dark);
        font-weight: 700;
        color: var(--text-dark);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(45deg, var(--dark-ochre), var(--yellow-ochre));
        color: white;
    }
    
    /* Selectbox and Input Styling */
    .stSelectbox > div > div {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
        color: var(--text-dark);
    }
    
    .stTextArea > div > div > textarea {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
        color: var(--text-dark);
        font-family: 'Source Sans Pro', sans-serif;
    }
    
    .stTextInput > div > div > input {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
        color: var(--text-dark);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--chestnut-brown), var(--yellow-ochre));
    }
    
    .stSlider > div > div > div > div > div {
        background: var(--yellow-ochre);
        border: 3px solid white;
        box-shadow: 0 2px 4px rgba(149, 69, 53, 0.3);
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: var(--warm-white);
        border-radius: 10px;
        padding: 1rem;
        color: var(--text-dark);
        border: 1px solid var(--light-chestnut);
    }
    
    /* Checkbox */
    .stCheckbox > label > div {
        background: var(--yellow-ochre);
        border-color: var(--chestnut-brown);
        color: var(--text-dark);
    }
    
    /* Metrics */
    .metric-container {
        background: linear-gradient(135deg, var(--warm-white), var(--cream));
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid var(--light-chestnut);
        box-shadow: 0 4px 8px rgba(149, 69, 53, 0.1);
        text-align: center;
        color: var(--text-dark);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--warm-white), var(--cream));
        border: 2px solid var(--light-chestnut);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 8px rgba(149, 69, 53, 0.1);
    }
    
    [data-testid="metric-container"] > div {
        color: var(--chestnut-brown);
        font-weight: 600;
        
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, var(--light-chestnut), var(--yellow-ochre));
        border-radius: 10px;
        font-weight: 600;
        color: var(--text-dark);
    }
    
    .streamlit-expanderContent {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-top: none;
        border-radius: 0 0 10px 10px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--cream), var(--warm-white));
        border-right: 3px solid var(--light-chestnut);
    }
    
    /* Success, Warning, Error Messages */
    .stSuccess {
        background: linear-gradient(45deg, #d4edda, #c3e6cb);
        border-left: 5px solid var(--yellow-ochre);
        color: var(--text-dark);
    }
    
    .stWarning {
        background: linear-gradient(45deg, #fff3cd, #ffeaa7);
        border-left: 5px solid var(--chestnut-brown);
        color: var(--text-dark);
    }
    
    .stError {
        background: linear-gradient(45deg, #f8d7da, #f5c6cb);
        border-left: 5px solid var(--dark-chestnut);
        color: var(--text-dark);
    }
    
    .stInfo {
        background: linear-gradient(45deg, var(--cream), var(--warm-white));
        border-left: 5px solid var(--yellow-ochre);
        color: var(--text-dark);
    }
    
    /* DataFrame Styling */
    .dataframe {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
    }
    
    .dataframe thead th {
        background: linear-gradient(90deg, var(--chestnut-brown), var(--yellow-ochre));
        font-weight: 600;
        color: var(--text-dark);
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: var(--cream);
    }
    
    .dataframe tbody tr:hover {
        background: linear-gradient(90deg, var(--cream), var(--warm-white));
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--chestnut-brown), var(--yellow-ochre));
        border-radius: 10px;
    }
    
    /* Custom Classes */
    .book-preview {
        background: var(--warm-white);
        border: 2px solid var(--light-chestnut);
        border-radius: 10px;
        padding: 1rem;
        color: var(--text-dark);
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(149, 69, 53, 0.1);
    }
    
    .gradient-text {
        background: linear-gradient(45deg, var(--chestnut-brown), var(--yellow-ochre));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
        color: var(--text-dark);
    }
    
    /* Plotly Chart Container */
    .js-plotly-plot {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(149, 69, 53, 0.2);
        overflow: hidden;
        border: 2px solid var(--light-chestnut);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--cream);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--chestnut-brown), var(--yellow-ochre));
        border-radius: 10px;
        border: 2px solid var(--cream);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--dark-chestnut), var(--dark-ochre));
    }
    </style>
    """, unsafe_allow_html=True)