import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

st.set_page_config(layout="wide")

# =========================
# 🎨 CUSTOM STYLING
# =========================
st.markdown("""
<style>
.metric-card {
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 10px;
}
.metric-title {
    color: #94A3B8;
    font-size: 14px;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
}
.small-note {
    color: #94A3B8;
    font-size: 12px;
    text-align: center;
}
.section-title {
    font-size: 22px;
    margin-bottom: 10px;
}
.bullet-note {
    font-size: 16px;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TEAM COLORS & FLAGS
# =========================
team_colors = {
    "India": ("#FF9933", "#000080", "#138808"),
    "Australia": ("#FFD700", "#006447", "#000000"),
    "Pakistan": ("#006400", "#FFFFFF", "#008000"),
    "England": ("#0056B3", "#FFFFFF", "#000000"),
    "South Africa": ("#007A33", "#FFD700", "#000000"),
    "West Indies": ("#800000", "#FFC60B", "#FFFFFF"),
    "New Zealand": ("#000000", "#808080", "#FFFFFF"),
    "Sri Lanka": ("#002366", "#FDB913", "#FFFFFF"),
    "Bangladesh": ("#006600", "#F42A41", "#FFFFFF"),
    "Afghanistan": ("#D52B1E", "#000000", "#FFFFFF"),
    "USA": ("#002868", "#BF0A30", "#FFFFFF"),
    "Ireland": ("#169B62", "#FFFFFF", "#FF8200"),
    "Canada": ("#FF0000", "#FFFFFF", "#000000"),
    "Italy": ("#009246", "#FFFFFF", "#CE2B37"),
    "Netherlands": ("#EF7C00", "#FFFFFF", "#21468B"),
    "Namibia": ("#007A5E", "#FCD116", "#DB1C2C"),
    "Zimbabwe": ("#007934", "#FCCE10", "#000000"),
    "Nepal": ("#DC143C", "#003893", "#FFFFFF"),
    "Oman": ("#CE1126", "#FFFFFF", "#000000"),
    "UAE": ("#00732F", "#FFFFFF", "#CE1126")
}

team_flags = {
    "India": "🇮🇳",
    "Australia": "🇦🇺",
    "Pakistan": "🇵🇰",
    "England": "🏴",
    "South Africa": "🇿🇦",
    "West Indies": "🇼🇸",
    "New Zealand": "🇳🇿",
    "Sri Lanka": "🇱🇰",
    "Bangladesh": "🇧🇩",
    "Afghanistan": "🇦🇫",
    "USA": "🇺🇸",
    "Ireland": "🇮🇪",
    "Canada": "🇨🇦",
    "Italy": "🇮🇹",
    "Netherlands": "🇳🇱",
    "Namibia": "🇳🇦",
    "Zimbabwe": "🇿🇼",
    "Nepal": "🇳🇵",
    "Oman": "🇴🇲",
    "UAE": "🇦🇪"
}

# =========================
# LOAD DATA FROM GOOGLE SHEETS
# =========================
sheet_id = "1js8s1QySOIUDcIED7rAvWOD3nd10X1lX7iO3R9oU4gM"
sheet_name = "Sheet1"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =========================
# INLINE FILTERS
# =========================
st.title("🏏 Bowler Performance – T20 World Cup 2026")

col1, col2, col3 = st.columns(3)

with col1:
    bowler = st.selectbox("Select Bowler", sorted(df["Bowler Name"].unique()))

bowler_all_df = df[df["Bowler Name"] == bowler]

with col2:
    opponent_list = ["Overall Tournament"] + sorted(bowler_all_df["Batting Team"].unique())
    opponent = st.selectbox("Select Opponent", opponent_list)

with col3:
    phase_filter = st.multiselect(
        "Select Phases",
        sorted(df["Phase"].unique()),
        default=sorted(df["Phase"].unique())
    )

# Filter Data
if opponent != "Overall Tournament":
    bowler_df = bowler_all_df[bowler_all_df["Batting Team"] == opponent]
else:
    bowler_df = bowler_all_df.copy()

bowler_df = bowler_df[bowler_df["Phase"].isin(phase_filter)]
valid_balls = bowler_df[bowler_df["Valid_Ball"] == 1]

bowler_team = bowler_df["Bowling Team"].iloc[0] if not bowler_df.empty else "Unknown"
primary, secondary, accent = team_colors.get(bowler_team, ("#333333","#666666","#999999"))
flag = team_flags.get(bowler_team, "")

# =========================
# METRICS SECTION
# =========================
st.markdown(f'<div class="section-title"><b>{bowler}</b> – {bowler_team} {flag}</div>', unsafe_allow_html=True)

balls = len(valid_balls)
runs = bowler_df["Total_Runs"].sum()
wickets = bowler_df["Out"].sum()
overs = balls // 6 + (balls % 6) / 10
economy = round(runs / (balls / 6), 2) if balls > 0 else 0
dot_balls = len(valid_balls[valid_balls["Bat_Runs"] == 0])
dot_pct = round((dot_balls / balls) * 100, 1) if balls > 0 else 0
stump_hits = len(valid_balls[valid_balls["Hitting_Stumps"]==1])
stump_pct = round((stump_hits/balls)*100,1) if balls>0 else 0

m1, m2, m3, m4, m5, m6 = st.columns(6, gap="medium")
metrics = [
    ("Overs", overs),
    ("Runs", runs),
    ("Wickets", wickets),
    ("Economy", economy),
    ("Dot %", f"{dot_pct}%"),
    ("% Hitting Stumps", f"{stump_pct}%")
]

for col, (title, value) in zip([m1,m2,m3,m4,m5,m6], metrics):
    col.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {accent}, {primary}); border: 1px solid {secondary};">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# VISUALIZATIONS & NOTES
# =========================
st.markdown('<div class="section-title">Visualizations & Key Insights</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Pitch Map", "Wagon Wheel", "Economy per Length"])

# =========================
# PITCH MAP
# ==========================
with tab1:
    col_chart, col_notes = st.columns([1,2])
    with col_chart:
        st.subheader("Length Distribution")
        fig, ax = plt.subplots(figsize=(4,6))
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')

        ax.add_patch(plt.Rectangle((-1, 0), 2, 20, color="#C19A6B"))
        zones = {"Yorker": (0, 3, "#EF4444"), "Full": (3, 7, "#3B82F6"),
                 "Good": (7, 12, "#22C55E"), "Short": (12, 17, "#FACC15")}
        length_positions = {"Yorker":1.5,"Full":5,"Good":9.5,"Short":14.5}
        length_stats = valid_balls.groupby("Length").agg(Balls=("Length","count"))
        length_stats["Ball %"] = (length_stats["Balls"] / balls * 100) if balls > 0 else 0

        for length, (y1,y2,color) in zones.items():
            ax.axhspan(y1,y2,color=color,alpha=0.25)
            pct = length_stats["Ball %"].get(length,0)
            ax.text(1.1,(y1+y2)/2,f"{length}\n{pct:.1f}%",color="white",va="center")

        for _,row in valid_balls.iterrows():
            y = length_positions.get(row["Length"],16)
            x = np.random.uniform(-0.6,0.6)
            ax.scatter(x,y,color="black",s=25)

        ax.text(0,19.5,"Bowler",ha="center",color="white")
        ax.text(0,0.3,"Batsman",ha="center",color="white")
        ax.set_xlim(-1.3,1.5)
        ax.set_ylim(0,20)
        ax.axis("off")
        st.pyplot(fig)

    with col_notes:
        st.markdown("**Key Notes:**")
        notes = []
        for length in ["Yorker","Full","Good","Short"]:
            pct = length_stats["Ball %"].get(length,0)
            if pct > 0:
                notes.append(f"- Bowls {pct:.1f}% of deliveries as {length}")
            if pct >= 40:
                notes.append(f"  - ⚡ Focus on {length} length, bowler uses this frequently")
        if stump_pct > 20:
            notes.append(f"- ⚡ Hits stumps {stump_pct}% of the time")
        if dot_pct > 50:
            notes.append(f"- ⛔ High dot ball %: {dot_pct}%")
        for n in notes:
            st.markdown(f'<div style="font-size:16px;color:white;margin-bottom:5px">{n}</div>', unsafe_allow_html=True)

# =========================
# WAGON WHEEL (RHB vs LHB) with blue-red gradient and colorbar
# ==========================
with tab2:

    rhb_df = bowler_df[bowler_df["Batsman Type"]=="RHB"]
    lhb_df = bowler_df[bowler_df["Batsman Type"]=="LHB"]

    def calculate_stats(df_type):
        valid = df_type[df_type["Valid_Ball"] == 1]
        balls = len(valid)
        runs = df_type["Total_Runs"].sum()
        wickets = df_type["Out"].sum()
        economy = round(runs / (balls / 6), 2) if balls > 0 else 0
        dot_balls = len(valid[valid["Bat_Runs"]==0])
        dot_pct = round((dot_balls / balls)*100,1) if balls>0 else 0
        stump_hits = len(valid[valid["Hitting_Stumps"]==1])
        stump_pct = round((stump_hits/balls)*100,1) if balls>0 else 0
        return balls, runs, wickets, economy, dot_pct, stump_pct

    rhb_stats = calculate_stats(rhb_df)
    lhb_stats = calculate_stats(lhb_df)

    def plot_wagon(df_type, title, mirror=False):
        fig, ax = plt.subplots(figsize=(5,5))
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')

        numeric_df = df_type.copy()
        numeric_df = numeric_df[pd.to_numeric(numeric_df["Shot_Area"],errors='coerce').notnull()]
        numeric_df["Shot_Area"] = numeric_df["Shot_Area"].astype(int)
        if numeric_df.empty:
            ax.text(0,0,"No Data",ha="center",va="center",color="white",fontsize=14)
            ax.set_xlim(-1,1)
            ax.set_ylim(-1,1)
            ax.axis("off")
            return fig

        zone_runs = numeric_df.groupby("Shot_Area")["Bat_Runs"].sum()
        max_runs = zone_runs.max() if not zone_runs.empty else 1
        cmap = matplotlib.cm.get_cmap("coolwarm")  # Blue → Red

        zone_labels = {
            1:"Third Man",2:"Point",3:"Cover",4:"Long Off",
            5:"Long On",6:"Mid-wicket",7:"Square Leg",8:"Fine Leg"
        }

        for zone in range(1,9):
            angle_start = (np.pi/2)+(zone-1)*(np.pi/4)
            if mirror:
                angle_start = (np.pi/2)-(zone)*(np.pi/4)
            angle_mid = angle_start + (np.pi/8)
            runs_zone = zone_runs.get(zone,0)
            intensity = runs_zone/max_runs if max_runs>0 else 0

            wedge = plt.matplotlib.patches.Wedge(
                (0,0),1,
                np.degrees(angle_start),
                np.degrees(angle_start+np.pi/4),
                facecolor=cmap(intensity),
                edgecolor="white"
            )
            ax.add_patch(wedge)

            ax.text(0.8*np.cos(angle_mid),0.8*np.sin(angle_mid),
                    zone_labels[zone],ha="center",va="center",fontsize=7,color="white")
            ax.text(0.5*np.cos(angle_mid),0.5*np.sin(angle_mid),
                    str(int(runs_zone)),ha="center",va="center",fontsize=10,fontweight="bold",color="white")

        # Add colorbar
        sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.Normalize(vmin=0,vmax=max_runs))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("Runs Intensity", color="white")
        cbar.ax.yaxis.set_tick_params(color="white")
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        ax.set_xlim(-1.2,1.2)
        ax.set_ylim(-1.2,1.2)
        ax.axis("off")
        ax.set_title(title, color="white", fontsize=12)
        return fig

    col_rhb,col_lhb = st.columns(2)
    with col_rhb:
        st.markdown("### 🟢 vs Right Hand Batters (RHB)")
        st.markdown(f"**Balls:** {rhb_stats[0]}  \n**Runs:** {rhb_stats[1]}  \n**Wickets:** {rhb_stats[2]}  \n**Economy:** {rhb_stats[3]}  \n**Dot:** {rhb_stats[4]}%  \n**Hitting Stumps:** {rhb_stats[5]}%")
        st.pyplot(plot_wagon(rhb_df,"RHB Wagon Wheel",mirror=False))

    with col_lhb:
        st.markdown("### 🔵 vs Left Hand Batters (LHB)")
        st.markdown(f"**Balls:** {lhb_stats[0]}  \n**Runs:** {lhb_stats[1]}  \n**Wickets:** {lhb_stats[2]}  \n**Economy:** {lhb_stats[3]}  \n**Dot:** {lhb_stats[4]}%  \n**Hitting Stumps:** {lhb_stats[5]}%")
        st.pyplot(plot_wagon(lhb_df,"LHB Wagon Wheel",mirror=True))

# =========================
# ECONOMY PER LENGTH – separate for RHB & LHB with 4 columns
# =========================
with tab3:
    st.subheader("Economy per Length – RHB vs LHB")

    col_rhb_chart, col_rhb_notes, col_lhb_chart, col_lhb_notes = st.columns([2,1,2,1])

    # -------- RHB --------
    with col_rhb_chart:
        df_type = rhb_df
        length_stats = df_type[df_type["Valid_Ball"]==1].groupby("Length").agg(
            Runs=("Bat_Runs","sum"),
            Balls=("Valid_Ball","count")
        ).reindex(["Yorker","Full","Good","Short"], fill_value=0)
        length_stats["Economy"] = length_stats.apply(
            lambda row: round(row["Runs"] / (row["Balls"]/6),2) if row["Balls"]>0 else 0,
            axis=1
        )

        fig, ax = plt.subplots(figsize=(5,2.5))
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')
        bars = ax.bar(length_stats.index, length_stats["Economy"], color=primary, width=0.5)
        ax.set_ylabel("Economy", color="white", fontsize=9)
        ax.set_xlabel("Length", color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=9)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, height+0.05, str(round(height,1)),
                    ha="center", va="bottom", color="white", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col_rhb_notes:
        st.markdown("**Key Notes – RHB:**")
        notes = []
        for length in ["Yorker","Full","Good","Short"]:
            econ = length_stats["Economy"].get(length,0)
            if econ > 8.5:
                notes.append(f"- ⚠ High economy in {length}: {econ}")
            elif 0 < econ < 6:
                notes.append(f"- Good control in {length}: {econ}")
        for n in notes:
            st.markdown(f'<div style="font-size:16px;color:white;margin-bottom:5px">{n}</div>', unsafe_allow_html=True)

    # -------- LHB --------
    with col_lhb_chart:
        df_type = lhb_df
        length_stats = df_type[df_type["Valid_Ball"]==1].groupby("Length").agg(
            Runs=("Bat_Runs","sum"),
            Balls=("Valid_Ball","count")
        ).reindex(["Yorker","Full","Good","Short"], fill_value=0)
        length_stats["Economy"] = length_stats.apply(
            lambda row: round(row["Runs"] / (row["Balls"]/6),2) if row["Balls"]>0 else 0,
            axis=1
        )

        fig, ax = plt.subplots(figsize=(5,2.5))
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')
        bars = ax.bar(length_stats.index, length_stats["Economy"], color=primary, width=0.5)
        ax.set_ylabel("Economy", color="white", fontsize=9)
        ax.set_xlabel("Length", color="white", fontsize=9)
        ax.tick_params(colors="white", labelsize=9)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, height+0.05, str(round(height,1)),
                    ha="center", va="bottom", color="white", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col_lhb_notes:
        st.markdown("**Key Notes – LHB:**")
        notes = []
        for length in ["Yorker","Full","Good","Short"]:
            econ = length_stats["Economy"].get(length,0)
            if econ > 8.5:
                notes.append(f"- ⚠ High economy in {length}: {econ}")
            elif 0 < econ < 6:
                notes.append(f"- Good control in {length}: {econ}")
        for n in notes:
            st.markdown(f'<div style="font-size:16px;color:white;margin-bottom:5px">{n}</div>', unsafe_allow_html=True)

