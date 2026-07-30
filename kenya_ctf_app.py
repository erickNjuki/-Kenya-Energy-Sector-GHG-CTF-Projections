import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Kenya Energy Sector GHG Projections", layout="wide")

# ---------------------------------------------------------------------------
# Data (extracted from Kenya_CTF_Projections_Table.xlsx, tables 4a I/II/III)
# ---------------------------------------------------------------------------

years = ["2023", "2025", "2030", "2035", "2040"]

categories = [
    "Energy industries (Power Industries)",
    "Manufacturing industries and construction",
    "Other sectors (residential, commercial/institutional, agriculture)",
    "Fugitive emissions from fuels",
]

data = {
    "With Measures (WM)": {
        "Energy industries (Power Industries)": [1002.9, 774.8, 0, 0, 0],
        "Manufacturing industries and construction": [3500, 3746, 4439.4, 5261.2, 6235.1],
        "Other sectors (residential, commercial/institutional, agriculture)": [6000, 6032.8, 6115.6, 6199.5, 6284.6],
        "Fugitive emissions from fuels": [300, 305.7, 320.3, 335.6, 351.7],
        "TOTAL": [10802.9, 10859.3, 10875.3, 11796.3, 12871.4],
    },
    "With Additional Measures (WAM)": {
        "Energy industries (Power Industries)": [1002.9, 767.3, 0, 0, 0],
        "Manufacturing industries and construction": [3500, 3633.4, 3989.5, 4380.5, 4809.8],
        "Other sectors (residential, commercial/institutional, agriculture)": [6000, 5850.5, 5492.7, 5156.9, 4841.5],
        "Fugitive emissions from fuels": [300, 293.3, 277.3, 262.1, 247.7],
        "TOTAL": [10802.9, 10544.5, 9759.5, 9799.5, 9899],
    },
    "Without Measures (WOM) / Baseline": {
        "Energy industries (Power Industries)": [1002.9, 1084.7, 1319.7, 1605.6, 1953.5],
        "Manufacturing industries and construction": [3500, 3822.1, 4763, 5935.6, 7396.8],
        "Other sectors (residential, commercial/institutional, agriculture)": [6000, 6217.9, 6798.1, 7432.3, 8125.8],
        "Fugitive emissions from fuels": [300, 318.3, 369, 427.7, 495.9],
        "TOTAL": [10802.9, 11443, 13249.8, 15401.2, 17972],
    },
}

scenario_colors = {
    "With Measures (WM)": "#2E86AB",
    "With Additional Measures (WAM)": "#3FA34D",
    "Without Measures (WOM) / Baseline": "#C1440E",
}

category_colors = {
    "Energy industries (Power Industries)": "#E4572E",
    "Manufacturing industries and construction": "#17BEBB",
    "Other sectors (residential, commercial/institutional, agriculture)": "#FFC914",
    "Fugitive emissions from fuels": "#7A6FF0",
}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🔋⚡ Kenya Energy Sector GHG Projections")
st.caption(
    "CTF-aligned projections table (Table 4a I/II/III) — illustrative example, "
    "units in kt CO₂ eq. Note: 1.A.3 Transport is marked 'NE' (not estimated) and excluded."
)

st.markdown(
    "> ⚠️ **Illustrative, not official.** This is a worked example, not Kenya's official "
    "government-submitted CTF projections."
)

# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------

st.sidebar.header("Controls")
selected_scenarios = st.sidebar.multiselect(
    "Scenarios to show",
    options=list(data.keys()),
    default=list(data.keys()),
)
show_categories = st.sidebar.checkbox("Break down by category (stacked)", value=False)

if not selected_scenarios:
    st.warning("Select at least one scenario from the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------

kpi_cols = st.columns(len(selected_scenarios))
for col, scenario in zip(kpi_cols, selected_scenarios):
    total_2023 = data[scenario]["TOTAL"][0]
    total_2040 = data[scenario]["TOTAL"][-1]
    pct_change = (total_2040 - total_2023) / total_2023 * 100
    col.metric(
        label=scenario,
        value=f"{total_2040:,.0f} kt CO₂ eq (2040)",
        delta=f"{pct_change:+.1f}% vs 2023",
        delta_color="inverse",
    )

st.divider()

# ---------------------------------------------------------------------------
# Main chart: Total emissions trajectory
# ---------------------------------------------------------------------------

st.subheader("Total energy-sector emissions trajectory")

fig = go.Figure()
for scenario in selected_scenarios:
    fig.add_trace(
        go.Scatter(
            x=years,
            y=data[scenario]["TOTAL"],
            mode="lines+markers",
            name=scenario,
            line=dict(width=3, color=scenario_colors[scenario]),
            marker=dict(size=8),
        )
    )
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="kt CO₂ eq",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=480,
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Category breakdown (stacked bars), per scenario
# ---------------------------------------------------------------------------

if show_categories:
    st.subheader("Emissions by category")
    tabs = st.tabs(selected_scenarios)
    for tab, scenario in zip(tabs, selected_scenarios):
        with tab:
            fig2 = go.Figure()
            for cat in categories:
                fig2.add_trace(
                    go.Bar(
                        x=years,
                        y=data[scenario][cat],
                        name=cat,
                        marker_color=category_colors[cat],
                    )
                )
            fig2.update_layout(
                barmode="stack",
                xaxis_title="Year",
                yaxis_title="kt CO₂ eq",
                legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
                height=480,
            )
            st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Scenario comparison at a chosen year
# ---------------------------------------------------------------------------

st.subheader("Scenario comparison in a given year")
year_choice = st.select_slider("Year", options=years, value="2040")
year_idx = years.index(year_choice)

comp_rows = []
for scenario in selected_scenarios:
    for cat in categories:
        comp_rows.append(
            {"Scenario": scenario, "Category": cat, "Emissions": data[scenario][cat][year_idx]}
        )
comp_df = pd.DataFrame(comp_rows)

fig3 = px.bar(
    comp_df,
    x="Scenario",
    y="Emissions",
    color="Category",
    color_discrete_map=category_colors,
    text_auto=".0f",
)
fig3.update_layout(
    yaxis_title="kt CO₂ eq",
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Raw data table
# ---------------------------------------------------------------------------

with st.expander("View underlying data table"):
    for scenario in selected_scenarios:
        st.markdown(f"**{scenario}**")
        df = pd.DataFrame(data[scenario], index=years).T
        st.dataframe(df, use_container_width=True)
