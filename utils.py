import pandas as pd
import streamlit as st

# ---------- Data Loading ----------
@st.cache_data
def load_data():
    """Load and cache the dataset to prevent reloading on every interaction"""
    # Adjust path if necessary
    df = pd.read_csv("data/Cleaned_Motor_Vehicle_Collisions_Crashes.csv")
    return df

# ---------- UI & Styling ----------
def apply_custom_css():
    st.markdown("""
        <style>
        .main { padding-top: 1rem; }
        .stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .insight-box {
            padding: 20px;
            border-left: 5px solid #764ba2;
            background-color: #f9f9f9;
            margin: 10px 0;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def create_header():
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("data/car-crash-icon.png", width=100)
    with col2:
        st.markdown("""
            <h1 style='background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top:10px;'>
            Motor Vehicle Collision Crashes</h1>
        """, unsafe_allow_html=True)
    st.markdown("---")

def main():
    """Initializes the Page Config, Header, and Sidebar Navigation"""
    st.set_page_config(page_title="NYC Collision Analytics", layout="wide", initial_sidebar_state="expanded")
    apply_custom_css()
    create_header()

    menu_options = ["DASHBOARD", "KPI", "TIME", "LOCATION", "CONTRIBUTING FACTORS", "INJURIES", "PREDICTIONS"]
    
    # THE FIX: Simply use key="menu". 
    # Streamlit will automatically create st.session_state.menu and update it instantly.
    st.sidebar.radio(
        "NAVIGATION MENU",
        menu_options,
        key="menu" 
    )

# ---------- Helper Functions ----------
def render_image_with_insight(path, title, insight):
    """Helper to display images with a spinner and styled text"""
    with st.spinner(f"Loading {title}..."):
        st.subheader(title)
        st.image(path, use_container_width=True)
        st.markdown(f"<div class='insight-box'><b>Insight:</b><br>{insight}</div>", unsafe_allow_html=True)

# ---------- Tab Components ----------
def create_dashboard_tab(df):
    with st.spinner("Loading Overview..."):
        m1, m2, m3 = st.columns(3)
        start, end = df['YEAR'].min(), df['YEAR'].max()
        m1.metric("📊 Data Period", f"{start} - {end}", f"{end-start+1} Years")
        m2.metric("📍 Coverage", f"{df['BOROUGH'].nunique()} Boroughs", "NYC Wide")
        m3.metric("📈 Dataset Size", f"{len(df):,}", "Records")

        t1, t2, t3 = st.columns(3)
        t1.metric("Total Crashes", f"{len(df):,}")
        t2.metric("Total Injuries", f"{int(df['NUMBER OF PERSONS INJURED'].sum()):,}")
        t3.metric("Total Deaths", f"{int(df['NUMBER OF PERSONS KILLED'].sum()):,}")

def create_contributing_factors_tab(df):
    t1, t2, t3, t4 = st.tabs(["TOP FACTORS", "VEHICLE TYPES", "DISTRIBUTION PLOT", "SUMMARIZED DATA"])
    
    with t1:
        render_image_with_insight("plots/TopFactorsByBorough.png", "Top Factors by Borough", 
            "The stacked bar chart illustrating 'Top Factors by Borough' reveals that Brooklyn and Queens are the primary hotspots for traffic incidents among named boroughs, while a significant volume of data is categorized under an 'Unknown' location. Across all regions, 'Driver Inattention/Distraction' (orange) and 'Unspecified' (light blue) consistently emerge as the most frequent contributing factors, mirroring the trends seen in the overall share data. While Staten Island shows the lowest total incident count, the proportional makeup of factors remains relatively stable across the five boroughs, with 'Following Too Closely' and 'Failure to Yield Right-of-Way' maintaining their positions as the most common specific moving violations. Interestingly, the 'Unknown' category displays a disproportionately high amount of specific violations like 'Following Too Closely,' suggesting that more detailed reporting often occurs even when the exact geographic borough is not recorded.")
    
    with t2:
        render_image_with_insight("plots/FactorVehicleTypeHeatMap.png", "Crash Frequency by Factor and Vehicle Type", 
            "Based on the provided heatmap displaying 'Crash Frequency by Factor and Vehicle Type,' standard passenger vehicles are responsible for the overwhelming majority of recorded incidents. The visual data is heavily anchored by intense dark blue 'hotspots' at the intersections of Sedans and Station Wagon/Sport Utility Vehicles with the top contributing factors: 'Driver Inattention/Distraction' and 'Unspecified.' These specific combinations represent the absolute highest crash frequencies in the dataset, easily dwarfing all other categories. In stark contrast, vehicles like Box Trucks, Pick-up Trucks, and Taxis exhibit exceptionally low crash frequencies across the board, appearing almost white on the color scale. While secondary factors like 'Following Too Closely' and 'Failure to Yield Right-of-Way' show moderate incidence levels, they are again almost exclusively tied to Sedans and SUVs, highlighting that everyday passenger vehicles and distracted driving are the primary drivers of the overall accident volume.")
    
    with t3:
        render_image_with_insight("plots/FactorDonut.png", "Share of Top Contributing Factors", 
            "Based on the provided donut chart detailing the 'Share of Top Contributing Factors,' the distribution is heavily dominated by just two primary categories: 'Driver Inattention/Distraction' (34.5%) and 'Unspecified' (32.9%). Together, these two factors account for more than two-thirds of all incidents represented in this top group, highlighting distracted driving as the leading known cause, while also revealing a significant gap in specific data collection due to the high volume of unspecified records. The remaining specific moving violations make up a much smaller fraction of the total share; 'Following Too Closely' (11.3%) and 'Failure to Yield Right-of-Way' (9.6%) represent roughly a fifth combined, leaving minor specific infractions like 'Passing or Lane Usage Improper' (6.1%) and 'Backing Unsafely' (5.6%) as the smallest contributors among the major factors.")
        
    with t4:
        with st.spinner("Loading Data Table..."):
            st.subheader("Contributing Factor Data")
            factor_summary = df.groupby('CONTRIBUTING FACTOR').agg(
                Total_Collisions=('COLLISION_ID', 'count'),
                Total_Injuries=('NUMBER OF PERSONS INJURED', 'sum'),
                Avg_Injuries_Per_Collision=('NUMBER OF PERSONS INJURED', 'mean')
            ).reset_index().sort_values(by='Total_Collisions', ascending=False)
            st.dataframe(factor_summary, use_container_width=True)

def create_injuries_tab():
    t1, t2, t3 = st.tabs(["INJURY DISTRIBUTION BY BOROUGH", "TOTAL INJURIES BY HOUR", "INJURED VS KILLED"])
    
    with t1:
        render_image_with_insight("plots/InjuryDistributionbyBorough.png", "Injury Distribution by Borough", 
            "Based on the provided boxplot detailing 'Injury Distribution by Borough,' the typical traffic incident results in very few injuries across all geographic areas, as shown by the medians and interquartile ranges compressed tightly at or near zero. However, the severity of outlier events varies significantly by location. The 'Unknown' location category contains the single most devastating incident recorded (40 injuries) along with a dense cluster of high-casualty events. Among the identified boroughs, Queens and the Bronx experience the most extreme outliers, with single crashes causing upwards of 30 injuries. Conversely, Manhattan stands out with the tightest overall distribution and the lowest maximum injury threshold (peaking below 20). This suggests that while accidents in Manhattan may be frequent, the borough's denser traffic patterns and slower average speeds likely mitigate the risk of the severe, high-impact collisions seen in areas with more open roadways or highways.")
    
    with t2:
        render_image_with_insight("plots/TotalInjuriesbyHour.png", "Total Injuries by Hour", 
            "The line chart of 'Total Injuries by Hour' demonstrates a clear bimodal distribution that closely tracks typical daily commuting patterns. Injuries reach their absolute lowest point during the early morning hours (3:00 AM to 5:00 AM) before experiencing a sharp rise that peaks around 8:00 AM, coinciding with the morning rush hour. Following a minor mid-morning dip, there is a sustained and significant climb throughout the afternoon, culminating in a daily maximum at 5:00 PM (17:00). This evening peak is notably higher and broader than the morning surge, suggesting that the combination of increased traffic volume, driver fatigue, and diminishing daylight during the evening commute creates the highest-risk window for injuries. After 6:00 PM, injury counts steadily decline as traffic volume tapers off into the night.")
    
    with t3:
        render_image_with_insight("plots/Injury_vs_Killed_By_Borough.png", "Injured vs Killed", 
            "Based on the scatter plot grid comparing 'Persons Killed' versus 'Persons Injured' across the boroughs, there is no direct correlation between the volume of injuries and the number of fatalities in a single incident; in fact, extreme events tend to be exclusively one or the other. The vast majority of crashes cluster tightly near zero for both metrics. However, looking at the outliers reveals that the events causing the highest number of injuries (such as those approaching 30 to 40 in the Bronx, Queens, and the 'Unknown' category) remarkably resulted in zero deaths. Conversely, the single most lethal incident—a stark outlier in Manhattan recording 8 fatalities—involved zero non-fatal injuries. This visual pattern suggests two distinct types of severe accidents: concentrated, catastrophic impacts that are immediately lethal to a small group (such as pedestrians or a single vehicle's occupants), and broader, multi-vehicle or mass-transit collisions that cause widespread but ultimately survivable injuries.")

def create_predictions_tab():
    t1, t2, t3 = st.tabs(["LINEAR", "LOGISTIC", "DECISION TREE"])
    
    with t1:
        # Need to work on this
        render_image_with_insight("plots/TopCoefficients.png", "Linear Model Coefficients", 
            "This plot shows the most important features influencing predictions in the linear model.")
    
    with t2:
        sub1, sub2 = st.tabs(["TOP COEFFICIENTS", "PREDICTED PROBABILITY"])
        with sub1:
            render_image_with_insight("plots/TopCoefficients.png", "Logistic Coefficients", 
                "Based on the horizontal bar chart displaying model coefficients, 'Failure to Yield Right-of-Way' stands out as the strongest predictor for increasing the probability of an injury, possessing a coefficient value nearly double that of several other major infractions. While earlier frequency charts indicated that 'Driver Inattention/Distraction' caused the highest raw volume of accidents, this predictive model suggests that 'Failure to Yield' is significantly more likely to actually result in physical harm when a crash does occur. Common moving violations like 'Driver Inattention/Distraction' and 'Following Too Closely' still prominently raise the likelihood of injury, but to a lesser degree. Notably, spatial and temporal features—such as the incident occurring in Brooklyn or on a Sunday—have a positive, yet extremely marginal, influence on injury probability when compared to the severe impact of direct, behavioral driving errors.")
        with sub2:
            render_image_with_insight("plots/PredictedProbability.png", "Predicted Probability Distribution", 
                "The 'Predicted Probability of Injury' histogram provides a high-level view of your model's confidence across the entire dataset. The distribution is unimodal and slightly right-skewed, with the vast majority of predicted probabilities concentrated between 0.20 and 0.35. This indicates that for most traffic incidents in this dataset, the model estimates a 20% to 35% chance of an injury occurring. While there is a secondary 'hump' or shoulder around the 0.45 mark, very few incidents are assigned a high-certainty probability (above 0.60). This suggests that while certain factors (like 'Failure to Yield') significantly increase risk, the presence of an injury in a collision is still subject to a high degree of randomness or depends on variables not fully captured by the current feature set.")
    with t3:
        render_image_with_insight("plots/Injury_vs_Killed_By_Borough.png", "Decision Tree Visual", 
            "Decision Tree visualization utilizing borough-level data to map out injury outcomes.")