# Kenya Energy Sector GHG Projections Dashboard

An interactive Streamlit dashboard visualizing CTF-aligned GHG emission projections for Kenya's energy sector, based on Table 4(a) I/II/III (With Measures, With Additional Measures, Without Measures scenarios).

> ⚠️ **Illustrative example only.** This is a worked demonstration, not Kenya's official government-submitted CTF projections table.

## Features

- **KPI summary cards** — 2040 total emissions vs. 2023 baseline, with % change, per scenario
- **Trajectory chart** — total energy-sector emissions (2023–2040) across all three scenarios
- **Category breakdown** — stacked bars by source category (Power Industries, Manufacturing, Other sectors, Fugitive emissions), toggleable per scenario
- **Scenario comparison** — side-by-side bar chart at any selected year via slider
- **Raw data tables** — expandable view of the underlying figures

## Data

Values are drawn from `Kenya_CTF_Projections_Table.xlsx`, tables:
- `4a_I_WithMeasures` — With Measures (WM)
- `4a_II_WithAddlMeasures` — With Additional Measures (WAM)
- `4a_III_WithoutMeasures` — Without Measures (WOM) / baseline

Units: kt CO₂ eq (energy-sector CO2 emissions from fuel combustion and fugitive emissions).

Note: Category **1.A.3 Transport** is marked `NE` (not estimated) in the source data and is excluded from all totals and charts.

## Requirements

- Python 3.9+
- Packages listed in `requirements.txt`:
  - `streamlit`
  - `pandas`
  - `plotly`

## Setup

```bash
# 1. (Optional but recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run kenya_ctf_app.py
```

or, if `streamlit` isn't on your PATH:

```bash
py -m streamlit run kenya_ctf_app.py
```

Streamlit will open the dashboard in your browser automatically (usually at `http://localhost:8501`).

## Project structure

```
kenya-ctf/
├── kenya_ctf_app.py     # Main Streamlit app
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Customizing

The dataset lives directly in `kenya_ctf_app.py` inside the `data` dictionary near the top of the file. To update figures (e.g. after revising the source workbook), edit the values there — no other code changes are needed since the charts and tables are generated dynamically from that dictionary.

## Source

Original data: `Kenya_CTF_Projections_Table.xlsx` — a worked example of the projections tables required for Biennial Transparency Reports under the UNFCCC's Common Tabular Format (CTF) for Kenya's energy sector.
