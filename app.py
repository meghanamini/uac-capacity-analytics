import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UAC System Capacity & Care Load Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1F4E79, #2E75B6);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; font-size: 1.8rem; margin: 0; }
    .main-header p  { color: #BDD7EE; margin: 0.3rem 0 0; font-size: 0.95rem; }
    .kpi-card {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .kpi-label { font-size: 0.78rem; color: #6B7280; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #1F4E79; line-height: 1.1; }
    .kpi-sub   { font-size: 0.75rem; color: #9CA3AF; margin-top: 0.3rem; }
    .badge-danger  { background:#FEE2E2; color:#991B1B; padding:2px 10px;
                     border-radius:20px; font-size:0.72rem; font-weight:600; }
    .badge-success { background:#D1FAE5; color:#065F46; padding:2px 10px;
                     border-radius:20px; font-size:0.72rem; font-weight:600; }
    .badge-warn    { background:#FEF3C7; color:#92400E; padding:2px 10px;
                     border-radius:20px; font-size:0.72rem; font-weight:600; }
    .insight-box {
        border-left: 4px solid #2E75B6;
        background: #EFF6FF;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        color: #1E3A5F;
    }
    .insight-box.warn    { border-color:#F59E0B; background:#FFFBEB; color:#78350F; }
    .insight-box.success { border-color:#10B981; background:#ECFDF5; color:#064E3B; }
    div[data-testid="stMetric"] { background:white; border-radius:10px;
                                   padding:0.8rem; box-shadow:0 2px 6px rgba(0,0,0,0.06); }
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program__1_.csv")
    df = df[df["Date"].notna()].copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Children in HHS Care"] = (
        df["Children in HHS Care"]
        .astype(str).str.replace(",", "").str.strip()
    )
    df["Children in HHS Care"] = pd.to_numeric(df["Children in HHS Care"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Total System Load"] = (
        df["Children in CBP custody"] + df["Children in HHS Care"]
    )
    df["Net Intake"] = (
        df["Children transferred out of CBP custody"]
        - df["Children discharged from HHS Care"]
    )
    df["7d Rolling HHS"]  = df["Children in HHS Care"].rolling(7).mean()
    df["14d Rolling HHS"] = df["Children in HHS Care"].rolling(14).mean()
    return df

df = load_data()

# ── Monthly aggregation ───────────────────────────────────────────────────────
@st.cache_data
def monthly_agg(data):
    m = data.groupby("Month").agg(
        Apprehended=("Children apprehended and placed in CBP custody*", "sum"),
        CBP_Avg=("Children in CBP custody", "mean"),
        Transferred=("Children transferred out of CBP custody", "sum"),
        HHS_Avg=("Children in HHS Care", "mean"),
        Discharged=("Children discharged from HHS Care", "sum"),
    ).reset_index()
    m["Net_Pressure"] = m["Transferred"] - m["Discharged"]
    m["Ratio"] = (m["Discharged"] / m["Transferred"].replace(0, 1)).round(2)
    return m

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/"
    "Seal_of_the_United_States_Department_of_Health_and_Human_Services.svg/240px-"
    "Seal_of_the_United_States_Department_of_Health_and_Human_Services.svg.png",
    width=80
)
st.sidebar.title("Filters & Controls")

year_options = ["All Years (2023–2025)"] + [str(y) for y in sorted(df["Year"].unique())]
selected_year = st.sidebar.selectbox("Select Year", year_options)

granularity = st.sidebar.radio("Time Granularity", ["Monthly", "Quarterly"])

rolling_toggle = st.sidebar.checkbox("Show rolling averages on HHS trend", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**About**")
st.sidebar.markdown(
    "UAC Program Analytics Framework  \n"
    "Data: HHS Office of Refugee Resettlement  \n"
    "Period: Jan 2023 – Dec 2025  \n"
    "Records: 720 daily observations"
)

# ── Filter data ───────────────────────────────────────────────────────────────
if selected_year == "All Years (2023–2025)":
    filtered = df.copy()
else:
    filtered = df[df["Year"] == int(selected_year)].copy()

monthly = monthly_agg(filtered)

if granularity == "Quarterly":
    filtered["Quarter"] = filtered["Date"].dt.to_period("Q").astype(str)
    monthly = filtered.groupby("Quarter").agg(
        Apprehended=("Children apprehended and placed in CBP custody*", "sum"),
        CBP_Avg=("Children in CBP custody", "mean"),
        Transferred=("Children transferred out of CBP custody", "sum"),
        HHS_Avg=("Children in HHS Care", "mean"),
        Discharged=("Children discharged from HHS Care", "sum"),
    ).reset_index().rename(columns={"Quarter": "Month"})
    monthly["Net_Pressure"] = monthly["Transferred"] - monthly["Discharged"]
    monthly["Ratio"] = (monthly["Discharged"] / monthly["Transferred"].replace(0, 1)).round(2)

x_col = "Month"

# ── KPI computation ───────────────────────────────────────────────────────────
tot_app    = int(filtered["Children apprehended and placed in CBP custody*"].sum())
tot_dis    = int(filtered["Children discharged from HHS Care"].sum())
tot_trans  = int(filtered["Children transferred out of CBP custody"].sum())
avg_hhs    = filtered["Children in HHS Care"].mean()
max_hhs    = int(filtered["Children in HHS Care"].max())
max_date   = filtered.loc[filtered["Children in HHS Care"].idxmax(), "Date"].strftime("%b %d, %Y")
net_press  = tot_trans - tot_dis
ratio      = round(tot_dis / tot_trans, 2) if tot_trans > 0 else 0
vals       = filtered["Children in HHS Care"].dropna()
mean_v     = vals.mean()
std_v      = vals.std()
volatility = round((std_v / mean_v) * 100, 1) if mean_v > 0 else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🏥 System Capacity & Care Load Analytics</h1>
  <p>Unaccompanied Children Program &nbsp;|&nbsp; U.S. Department of Health and Human Services
     &nbsp;|&nbsp; Jan 2023 – Dec 2025</p>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.metric("Avg HHS Care Load", f"{avg_hhs:,.0f}", help="Average daily children in HHS care")
with k2:
    st.metric("Peak HHS Load", f"{max_hhs:,}", delta=f"{max_date}", delta_color="off")
with k3:
    st.metric("Total Apprehended", f"{tot_app:,}")
with k4:
    st.metric("Total Discharged", f"{tot_dis:,}", help="Successful sponsor placements")
with k5:
    st.metric("Discharge Offset Ratio", f"{ratio:.2f}x",
              delta="Clearing faster" if ratio >= 1 else "Intake exceeds discharges",
              delta_color="normal" if ratio >= 1 else "inverse")
with k6:
    st.metric("Volatility Index", f"{volatility}%", help="Coefficient of variation of HHS census")

st.markdown("---")

# ── Insights ──────────────────────────────────────────────────────────────────
st.subheader("📌 Key Insights")
col_i1, col_i2 = st.columns(2)
with col_i1:
    st.markdown(
        f'<div class="insight-box warn">⚠️ <b>Peak load of {max_hhs:,} children</b> in HHS care '
        f'occurred on {max_date}, representing maximum capacity strain in this period.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="insight-box">📈 <b>2024 recorded peak pipeline throughput</b> — '
        '52,552 transfers in and 51,689 discharges out, the highest annual volumes in the dataset.</div>',
        unsafe_allow_html=True
    )
with col_i2:
    st.markdown(
        '<div class="insight-box success">✅ <b>By 2025, HHS care load dropped ~83%</b> from peak, '
        'reaching ~1,972 children — the lowest recorded in the dataset.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight-box">📊 <b>Overall discharge offset ratio of {ratio:.2f}x</b> — '
        'the system successfully placed more children with sponsors than it received in HHS transfers.</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Chart 1: HHS Care Load Trend ─────────────────────────────────────────────
st.subheader("📈 HHS Care Load Over Time")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=filtered["Date"], y=filtered["Children in HHS Care"],
    name="Daily HHS Census", line=dict(color="#2E75B6", width=1.5),
    fill="tozeroy", fillcolor="rgba(46,117,182,0.08)"
))
if rolling_toggle:
    fig1.add_trace(go.Scatter(
        x=filtered["Date"], y=filtered["7d Rolling HHS"],
        name="7-Day Rolling Avg", line=dict(color="#F59E0B", width=2, dash="dot")
    ))
    fig1.add_trace(go.Scatter(
        x=filtered["Date"], y=filtered["14d Rolling HHS"],
        name="14-Day Rolling Avg", line=dict(color="#EF4444", width=2, dash="dash")
    ))
fig1.add_hline(y=max_hhs, line_dash="dot", line_color="#991B1B", line_width=1.5,
               annotation_text=f"Peak: {max_hhs:,}", annotation_position="top right")
fig1.update_layout(
    height=380, margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title="Date", yaxis_title="Children in HHS Care",
    plot_bgcolor="white", paper_bgcolor="white",
    yaxis=dict(gridcolor="#F3F4F6"), xaxis=dict(gridcolor="#F3F4F6")
)
st.plotly_chart(fig1, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("🔵 CBP vs HHS Load")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=monthly[x_col], y=monthly["CBP_Avg"],
                          name="CBP Avg Custody", marker_color="#D85A30"))
    fig2.add_trace(go.Bar(x=monthly[x_col], y=monthly["HHS_Avg"],
                          name="HHS Avg Care", marker_color="#1D9E75"))
    fig2.update_layout(
        height=320, barmode="group", margin=dict(l=10, r=10, t=10, b=60),
        legend=dict(orientation="h", y=1.08), plot_bgcolor="white",
        paper_bgcolor="white", yaxis=dict(gridcolor="#F3F4F6"),
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader("⚖️ Net Intake Pressure")
    colors = ["#EF4444" if v > 0 else "#10B981" for v in monthly["Net_Pressure"]]
    fig3 = go.Figure(go.Bar(
        x=monthly[x_col], y=monthly["Net_Pressure"],
        marker_color=colors, name="Net Pressure"
    ))
    fig3.add_hline(y=0, line_color="#374151", line_width=1)
    fig3.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=60),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#F3F4F6", title="Transfers − Discharges"),
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Chart 3: Full Pipeline ────────────────────────────────────────────────────
st.subheader("🔄 Full Care Pipeline — Apprehensions, Transfers & Discharges")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=monthly[x_col], y=monthly["Apprehended"],
                           name="Apprehended (CBP)", line=dict(color="#7F77DD", width=2)))
fig4.add_trace(go.Scatter(x=monthly[x_col], y=monthly["Transferred"],
                           name="Transferred to HHS", line=dict(color="#1D9E75", width=2)))
fig4.add_trace(go.Scatter(x=monthly[x_col], y=monthly["Discharged"],
                           name="Discharged to Sponsors", line=dict(color="#BA7517", width=2)))
fig4.update_layout(
    height=360, margin=dict(l=20, r=20, t=10, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor="white", paper_bgcolor="white",
    yaxis=dict(gridcolor="#F3F4F6", title="Volume"),
    xaxis=dict(gridcolor="#F3F4F6", tickangle=-45)
)
st.plotly_chart(fig4, use_container_width=True)

# ── Charts row 3 ─────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("📅 Yearly Summary")
    yearly = df.groupby("Year").agg(
        Apprehended=("Children apprehended and placed in CBP custody*", "sum"),
        Transferred=("Children transferred out of CBP custody", "sum"),
        Discharged=("Children discharged from HHS Care", "sum"),
    ).reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=yearly["Year"].astype(str), y=yearly["Apprehended"],
                          name="Apprehended", marker_color="#7F77DD"))
    fig5.add_trace(go.Bar(x=yearly["Year"].astype(str), y=yearly["Transferred"],
                          name="Transferred", marker_color="#1D9E75"))
    fig5.add_trace(go.Bar(x=yearly["Year"].astype(str), y=yearly["Discharged"],
                          name="Discharged", marker_color="#BA7517"))
    fig5.update_layout(
        height=320, barmode="group", margin=dict(l=10, r=10, t=10, b=30),
        legend=dict(orientation="h", y=1.08), plot_bgcolor="white",
        paper_bgcolor="white", yaxis=dict(gridcolor="#F3F4F6")
    )
    st.plotly_chart(fig5, use_container_width=True)

with c4:
    st.subheader("📊 Discharge Offset Ratio")
    ratio_colors = ["#10B981" if v >= 1 else "#EF4444" for v in monthly["Ratio"]]
    fig6 = go.Figure(go.Bar(
        x=monthly[x_col], y=monthly["Ratio"],
        marker_color=ratio_colors, name="Ratio"
    ))
    fig6.add_hline(y=1.0, line_dash="dash", line_color="#374151",
                   annotation_text="Break-even (1.0x)", annotation_position="top left")
    fig6.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=60),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#F3F4F6", title="Discharges / Transfers"),
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig6, use_container_width=True)

# ── Raw data table ────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data Table"):
    display_df = filtered[["Date", "Children apprehended and placed in CBP custody*",
                            "Children in CBP custody",
                            "Children transferred out of CBP custody",
                            "Children in HHS Care",
                            "Children discharged from HHS Care"]].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df.rename(columns={
        "Children apprehended and placed in CBP custody*": "Apprehended (CBP)",
        "Children in CBP custody": "In CBP Custody",
        "Children transferred out of CBP custody": "Transferred to HHS",
        "Children in HHS Care": "In HHS Care",
        "Children discharged from HHS Care": "Discharged"
    }), use_container_width=True, height=300)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#9CA3AF; font-size:0.8rem;'>"
    "U.S. Department of Health and Human Services &nbsp;|&nbsp; "
    "Office of Refugee Resettlement &nbsp;|&nbsp; UAC Program Analytics &nbsp;|&nbsp; "
    "Data: Jan 2023 – Dec 2025</p>",
    unsafe_allow_html=True
)
