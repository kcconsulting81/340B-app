"""What-If Scenario Modeler

Allows simulation of financial or compliance impact when adjusting 340B program variables
such as waste recovery, overcharge recovery, site participation, and return recoup.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 What-If Scenario Modeler", layout="wide")
st.title("📊 What-If Scenario Modeler")

st.markdown("Adjust key 340B program assumptions and model the resulting impact on overall savings, "
            "waste recovery, overcharges, and duplicate discount risks.")

# Input sliders for assumptions
st.subheader("⚙️ Scenario Controls")

waste_recovery_rate = st.slider("Waste Recovery Rate (%)", 0, 100, 60)
overcharge_recovery_rate = st.slider("Overcharge Dispute Success Rate (%)", 0, 100, 80)
site_expansion = st.number_input("New 340B-Eligible Sites Added", min_value=0, step=1, value=0)
return_recoup_rate = st.slider("Return Credit Success Rate (%)", 0, 100, 70)

# Mock base values (replace with real backend link later)
base_waste_savings = 50000
base_overcharges = 40000
base_return_losses = 20000
base_sites = 12
avg_site_savings = 15000

# Calculated scenarios
projected_waste = base_waste_savings * (waste_recovery_rate / 100)
projected_overcharges = base_overcharges * (overcharge_recovery_rate / 100)
projected_return = base_return_losses * (return_recoup_rate / 100)
projected_site_savings = site_expansion * avg_site_savings

total_projection = projected_waste + projected_overcharges + projected_return + projected_site_savings
baseline = base_waste_savings + base_overcharges + (base_sites * avg_site_savings)

# Display projections
st.subheader("📈 Scenario Impact Summary")

summary_df = pd.DataFrame({
    "Category": [
        "Recovered Waste Savings",
        "Resolved Overcharges",
        "Recouped Drug Returns",
        "Savings from Site Expansion"
    ],
    "Projected Impact ($)": [
        projected_waste,
        projected_overcharges,
        projected_return,
        projected_site_savings
    ]
})

st.dataframe(summary_df)

delta = total_projection - baseline
delta_percent = (delta / baseline) * 100

st.metric(label="💰 Total Projected Program Savings", value=f"${total_projection:,.2f}",
          delta=f"{delta:+,.2f} ({delta_percent:+.1f}%)")

# Download option
csv = summary_df.to_csv(index=False)
st.download_button("⬇️ Download Scenario Summary", csv, "what_if_scenario_summary.csv", "text/csv")
