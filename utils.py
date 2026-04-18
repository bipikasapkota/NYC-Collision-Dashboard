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
            padding-top: 2rem;
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
                    margin-top: 10px;
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
            use_container_width=True
        )
        st.write("""
        ### Insight:
        The stacked bar chart illustrating "Top Factors by Borough" reveals that Brooklyn and Queens are the primary hotspots for traffic incidents among named boroughs, while a significant volume of data is categorized under an "Unknown" location. Across all regions, "Driver Inattention/Distraction" (orange) and "Unspecified" (light blue) consistently emerge as the most frequent contributing factors, mirroring the trends seen in the overall share data. While Staten Island shows the lowest total incident count, the proportional makeup of factors remains relatively stable across the five boroughs, with "Following Too Closely" and "Failure to Yield Right-of-Way" maintaining their positions as the most common specific moving violations. Interestingly, the "Unknown" category displays a disproportionately high amount of specific violations like "Following Too Closely," suggesting that more detailed reporting often occurs even when the exact geographic borough is not recorded.
                 """)

    with tab2:
        st.image(
            "plots/FactorVehicleTypeHeatMap.png",
            use_container_width=True
        )
        st.write("""
        ### Insight:
        Based on the provided heatmap displaying "Crash Frequency by Factor and Vehicle Type," standard passenger vehicles are responsible for the overwhelming majority of recorded incidents. The visual data is heavily anchored by intense dark blue "hotspots" at the intersections of Sedans and Station Wagon/Sport Utility Vehicles with the top contributing factors: "Driver Inattention/Distraction" and "Unspecified." These specific combinations represent the absolute highest crash frequencies in the dataset, easily dwarfing all other categories. In stark contrast, vehicles like Box Trucks, Pick-up Trucks, and Taxis exhibit exceptionally low crash frequencies across the board, appearing almost white on the color scale. While secondary factors like "Following Too Closely" and "Failure to Yield Right-of-Way" show moderate incidence levels, they are again almost exclusively tied to Sedans and SUVs, highlighting that everyday passenger vehicles and distracted driving are the primary drivers of the overall accident volume.
        """)      

    with tab3:
         st.image(
            "plots/FactorDonut.png",
            use_container_width=True
        )
         st.write("""
        ### Insight:
        Based on the provided donut chart detailing the "Share of Top Contributing Factors," the distribution is heavily dominated by just 
                  two primary categories: "Driver Inattention/Distraction" (34.5%) and "Unspecified" (32.9%). Together, these two factors account for more than two-thirds of all incidents represented in this top group, highlighting distracted driving as the leading known cause, while also revealing a significant gap in specific data collection due to the high volume of unspecified records. The remaining specific moving violations make up a much smaller fraction of the total share; "Following Too Closely" (11.3%) and "Failure to Yield Right-of-Way" (9.6%) represent roughly a fifth combined, leaving minor specific infractions like "Passing or Lane Usage Improper" (6.1%) and "Backing Unsafely" (5.6%) as the smallest contributors among the major factors.
        """)
         
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
            use_container_width=True
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
            use_container_width=True
        )
        st.write("""
        ### Insight:
        Based on the provided boxplot detailing "Injury Distribution by Borough," the typical traffic incident results in very few injuries across all geographic areas, as shown by the medians and interquartile ranges compressed tightly at or near zero. However, the severity of outlier events varies significantly by location. The "Unknown" location category contains the single most devastating incident recorded (40 injuries) along with a dense cluster of high-casualty events. Among the identified boroughs, Queens and the Bronx experience the most extreme outliers, with single crashes causing upwards of 30 injuries. Conversely, Manhattan stands out with the tightest overall distribution and the lowest maximum injury threshold (peaking below 20). This suggests that while accidents in Manhattan may be frequent, the borough's denser traffic patterns and slower average speeds likely mitigate the risk of the severe, high-impact collisions seen in areas with more open roadways or highways.
            """)

    with tab2:
        st.image(
            "plots/TotalInjuriesbyHour.png",
            use_container_width=True
        )
    
        st.write("""
        ### Insight:       
        The line chart of "Total Injuries by Hour" demonstrates a clear bimodal distribution that closely tracks typical daily commuting patterns. Injuries reach their absolute lowest point during the early morning hours (3:00 AM to 5:00 AM) before experiencing a sharp rise that peaks around 8:00 AM, coinciding with the morning rush hour. Following a minor mid-morning dip, there is a sustained and significant climb throughout the afternoon, culminating in a daily maximum at 5:00 PM (17:00). This evening peak is notably higher and broader than the morning surge, suggesting that the combination of increased traffic volume, driver fatigue, and diminishing daylight during the evening commute creates the highest-risk window for injuries. After 6:00 PM, injury counts steadily decline as traffic volume tapers off into the night.
                 """)
        
    with tab3:
        st.image(
            "plots/Injury_vs_Killed_By_Borough.png",
            use_container_width=True
        )

        st.write("""
        ### Insight:
        Based on the scatter plot grid comparing "Persons Killed" versus "Persons Injured" across the boroughs, there is no direct correlation between the volume of injuries and the number of fatalities in a single incident; in fact, extreme events tend to be exclusively one or the other. The vast majority of crashes cluster tightly near zero for both metrics. However, looking at the outliers reveals that the events causing the highest number of injuries (such as those approaching 30 to 40 in the Bronx, Queens, and the "Unknown" category) remarkably resulted in zero deaths. Conversely, the single most lethal incident—a stark outlier in Manhattan recording 8 fatalities—involved zero non-fatal injuries. This visual pattern suggests two distinct types of severe accidents: concentrated, catastrophic impacts that are immediately lethal to a small group (such as pedestrians or a single vehicle's occupants), and broader, multi-vehicle or mass-transit collisions that cause widespread but ultimately survivable injuries.
            """)

    return


def create_predictions_tab():
    tab1, tab2, tab3 = st.tabs([
        "LINEAR",
        "LOGISTIC",
        "DECISION TREE",
    ])

    # ------------------ TAB 1 ------------------
    with tab1:
        st.image(
            "plots/TopCoefficients.png",
            use_container_width=True
        )

        st.write("""
        ### Insight:
        This plot shows the most important features influencing predictions in the linear model.
        """)

    # ------------------ TAB 2 ------------------
    with tab2:
        subtab1, subtab2 = st.tabs([
            "TOP COEFFICIENTS",
            "PREDICTED PROBABILITY"
        ])

        # ---- Subtab 1 ----
        with subtab1:
            st.image(
                "plots/TopCoefficients.png",
                use_container_width=True
            )

            st.write("""
            ### Insight:
            Based on the horizontal bar chart displaying model coefficients, "Failure to Yield Right-of-Way" stands out as the strongest predictor for increasing the probability of an injury, possessing a coefficient value nearly double that of several other major infractions. While earlier frequency charts indicated that "Driver Inattention/Distraction" caused the highest raw volume of accidents, this predictive model suggests that "Failure to Yield" is significantly more likely to actually result in physical harm when a crash does occur. Common moving violations like "Driver Inattention/Distraction" and "Following Too Closely" still prominently raise the likelihood of injury, but to a lesser degree. Notably, spatial and temporal features—such as the incident occurring in Brooklyn or on a Sunday—have a positive, yet extremely marginal, influence on injury probability when compared to the severe impact of direct, behavioral driving errors.
            """)

        # ---- Subtab 2 ----
        with subtab2:
            st.image(
                "plots/PredictedProbability.png",
                use_container_width=True
            )

            st.write("""
            ### Insight:
            The distribution is unimodal and slightly right-skewed, with the vast majority of predicted probabilities concentrated between 0.20 and 0.35. This indicates that for most traffic incidents in this dataset, the model estimates a 20% to 35% chance of an injury occurring. While there is a secondary "hump" or shoulder around the 0.45 mark, very few incidents are assigned a high-certainty probability (above 0.60). This suggests that while certain factors (like "Failure to Yield") significantly increase risk, the presence of an injury in a collision is still subject to a high degree of randomness or depends on variables not fully captured by the current feature set.
            """)

    # ------------------ TAB 3 ------------------
    with tab3:
        st.image(
            "plots/Injury_vs_Killed_By_Borough.png",
            use_container_width=True
        )

       