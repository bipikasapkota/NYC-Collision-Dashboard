import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load or generate sample motor vehicle collision data"""

    df = pd.read_csv("data/Cleaned_Motor_Vehicle_Collisions_Crashes.csv")

    print(df.head())
    return df


def create_dashboard_screen():       
    # ---------- Page Config ----------
    st.set_page_config(
        page_title="Motor Vehicle Collision Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # ---------- Sidebar Menu ----------
    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"

    menu_selection = st.sidebar.radio(
        "Select Menu",
        ["DASHBOARD", "KPI", "TIME","LOCATION","CONTRIBUTING FACTORS","INJURIES","PREDICTIONS"]
    )
    st.session_state.menu = menu_selection

    # ---------- Custom CSS ----------
    st.markdown("""
        <style>
        .main {
            padding-top: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .title-text {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
        }
        /* Center all images */
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
        }

        /* Force same image size */
        div[data-testid="stImage"] img {
            width: 100%;
            max-width: 600px;   /* uniform width */
            height: 350px;      /* uniform height */
            object-fit: cover;  /* crop instead of stretch */
            border-radius: 10px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        /* Hover effect */
        div[data-testid="stImage"] img:hover {
            transform: scale(1.03);
            box-shadow: 0px 6px 18px rgba(0,0,0,0.25);
        }   
        </style>
    """, unsafe_allow_html=True)

    # Create two columns: logo and title
    col1, col2 = st.columns([1, 6])  # adjust ratio to make logo smaller
    with col1:
        st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)
        st.image("data/car-crash-icon.png", width=120)  # Logo size
        st.markdown("</div>", unsafe_allow_html=True)
        

    with col2:
        st.markdown("""
            <div style="
                font-size: 2.5rem; 
                font-weight: bold; 
                background: linear-gradient(90deg, #667eea, #764ba2);
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent;
            ">
                Motor Vehicle Collision & Crashes
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    return

def create_dashboard_tab(df):
    # ---------- Top Metrics ----------
    col1, col2, col3 = st.columns(3)

    #Data Period
    with col1:  
        start_date_year = df['YEAR'].min()
        end_date_year = df['YEAR'].max()
        period_years = end_date_year - start_date_year + 1
        st.metric(
            "📊 Data Period",
            f"{start_date_year} - {end_date_year}",
            f"{period_years} Years"
        )

    # Coverage Area
    with col2:
        st.metric("📍 Coverage Area", f"{df['BOROUGH'].nunique()} Boroughs", "NYC Wide")

    # Dataset Size
    with col3:
        st.metric("📈 Dataset Size", f"{len(df):,}", "Records")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Crashes", f"{len(df):,}")                #Total Crashes
    col2.metric("Total Injuries", f"{int(df['NUMBER OF PERSONS INJURED'].sum()):,}")    #Total Injuries
    col3.metric("Total Deaths", f"{int(df['NUMBER OF PERSONS KILLED'].sum()):,}")   #Total Deaths
    return 


def create_contributing_factors_tab(df):
    tab1, tab2, tab3, tab4 = st.tabs([     
        "TOP FACTORS",
        "VEHICLE TYPES",
        "DISTRIBUTION PLOT",
        "SUMMARIZED DATA"
    ])

    with tab1:
        st.image(
            "plots/TopFactorsByBorough.png",
            width=True
        )

    with tab2:
        st.image(
            "plots/FactorVehicleTypeHeatMap.png",
            width=True
        )

    with tab3:
         st.image(
            "plots/FactorDonut.png",
            width=True
        )
   
    with tab4:
        st.subheader("Contributing Factor Data")

        factor_summary = (
        df.groupby('CONTRIBUTING FACTOR')
        .agg(
            Total_Collisions=('COLLISION_ID', 'count'),
            Total_Injuries=('NUMBER OF PERSONS INJURED', 'sum'),
            Avg_Injuries_Per_Collision=('NUMBER OF PERSONS INJURED', 'mean')
        )
        .reset_index()
        .sort_values(by='Total_Collisions', ascending=False)
        )

        st.dataframe(
            factor_summary,
            width=True
        )

    return


def create_injuries_tab():
    tab1, tab2, tab3 = st.tabs([     
        "INJURY DISTRIBUTION BY BOROUGH",
        "TOTAL INJURIES BY HOUR",
        "INJURED VS KILLED"
    ])

    with tab1:
        st.image(
            "plots/InjuryDistributionbyBorough.png",
            width=True
        )

    with tab2:
        st.image(
            "plots/TotalInjuriesbyHour.png",
            width=True
        )
    
    with tab3:
        st.image(
            "plots/Injury_vs_Killed_By_Borough.png",
            width=True
        )

    return


def create_predictions_tab():
    tab1, tab2, tab3, tab4 = st.tabs([     
       "LINEAR"          ,
        "LOGISTIC"        ,
        "DECISION TREE"   ,
       "RANDOM FOREST"   ,
    ])

    with tab1:
        st.image(
            "plots/InjuryDistributionbyBorough.png",
            width=True
        )

    with tab2:
        col1, col2 = st.columns([1, 2]) 
        with col1:
           st.image(
            "plots/TopCoefficients.png"
        )


        with col2:
            st.image(
            "plots/PredictedProbability.png"
        )     
        
    with tab3:
        st.image(
            "plots/Injury_vs_Killed_By_Borough.png",
            width=True
        )

    with tab4:
        st.image(
            "plots/Injury_vs_Killed_By_Borough.png",
            width=True
        )

    return