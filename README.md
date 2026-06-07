# System Capacity & Care Load Analytics for Unaccompanied Children

**U.S. Department of Health and Human Services | UAC Program Analytics**  
**Reporting Period:** January 2023 – December 2025  
**Data Points:** 720 daily observations

---

## Project Overview

This project delivers a comprehensive data-driven analytics framework for monitoring the HHS Unaccompanied Alien Children (UAC) Program — a federally mandated initiative in which children apprehended by U.S. Customs and Border Protection (CBP) are transferred to HHS for medical screening, sheltering, and sponsor placement.

The analysis translates raw daily operational counts into structured capacity metrics, trend analyses, and actionable KPIs to support evidence-based decision-making for government stakeholders and program administrators.

---

## Problem Statement

Although daily operational data is collected across the UAC care pipeline, HHS lacked a centralized analytical framework to continuously assess:

- Total care system load across CBP and HHS
- Balance between inflow (transfers) and outflow (discharges)
- Capacity stress and relief periods
- Sustainability of care delivery over time

---

## Deliverables

| File | Description |
|------|-------------|
| `UAC_Research_Paper.pdf` / `.docx` | Full research paper with EDA, methodology, KPIs, insights & recommendations |
| `UAC_Executive_Summary.pdf` / `.docx` | Concise government-facing brief for policymakers and administrators |
| `HHS_Unaccompanied_Alien_Children_Program__1_.csv` | Source dataset (720 daily records, Jan 2023 – Dec 2025) |

---

## Key Findings

| Finding | Detail |
|---------|--------|
| **Peak system load** | 11,516 children in HHS care on December 20, 2023 |
| **Total discharged to sponsors** | 124,853 children across all 3 years |
| **Discharge offset ratio** | 1.85x — system placed more children than it received in HHS transfers |
| **2025 load reduction** | −83% from peak — lowest care census in the dataset |
| **Care load volatility** | 46.7% coefficient of variation — requires adaptive infrastructure |
| **Peak throughput year** | 2024: 52,552 transfers in, 51,689 discharges out |

---

## Key Performance Indicators

- **Total Children Under Care** — System-wide responsibility (avg 6,061/day)
- **Net Intake Pressure** — Inflow vs. outflow imbalance (transfers − discharges)
- **Care Load Volatility Index** — Coefficient of variation of HHS daily census
- **Backlog Accumulation Rate** — Sustained positive net intake over time
- **Discharge Offset Ratio** — System's ability to relieve care load (1.85x overall)

---

## Dataset Description

| Column | Description |
|--------|-------------|
| `Date` | Reporting date |
| `Children apprehended and placed in CBP custody` | Daily CBP intake volume |
| `Children in CBP custody` | Active CBP care load (daily census) |
| `Children transferred out of CBP custody` | Flow from CBP into HHS system |
| `Children in HHS Care` | Active HHS care load (daily census) |
| `Children discharged from HHS Care` | Successful sponsor placements |

---

## Methodology

1. **Data Ingestion & Structuring** — Loaded 720-day time-series, datetime conversion, chronological ordering
2. **Data Quality & Validation** — Missing date detection, logical constraint checks, anomaly flagging
3. **Derived Capacity Metrics** — Total system load, net daily intake, care load growth rate, backlog indicator
4. **Trend & Temporal Analysis** — Daily, weekly, monthly, and quarterly aggregations; year-over-year comparison
5. **Pressure & Stress Identification** — 7-day and 14-day rolling averages; sustained high-load window detection

---

## Three-Year Summary

| Year | Apprehended | Transferred to HHS | Discharged | Avg HHS Census |
|------|-------------|-------------------|------------|----------------|
| 2023 | 27,056 | 36,124 | 66,244 | 8,646 |
| 2024 | 37,166 | 52,552 | 51,689 | 7,043 |
| 2025 (partial) | 3,115 | 3,965 | 6,920 | 2,543 |

---

## Strategic Recommendations

**For Program Administrators**
- Deploy real-time analytics dashboard for daily care load monitoring
- Implement tiered surge protocols at HHS census thresholds of 7,000 / 9,000 / 11,000
- Reduce sponsor placement processing time as the primary lever for decreasing standing load

**For Resource & Budget Planning**
- Size baselines to the 75th percentile of historical load (~8,000–9,000 children)
- Establish contingency shelter contracts activatable within 72 hours of threshold breach
- Track discharge offset ratio quarterly; values below 0.85 trigger formal capacity review

**For Policy & Oversight**
- Integrate CBP border encounter forecasts into HHS planning (2–4 week lead time)
- Publish quarterly public-facing care load reports for transparency
- Commission retrospective review of Aug–Dec 2023 surge for lessons learned

---

## Tools & Technologies

- **Python** (pandas) — Data ingestion, cleaning, aggregation, KPI computation
- **JavaScript / Chart.js** — Interactive analytics dashboard
- **docx (Node.js)** — Professional document generation
- **LibreOffice** — PDF conversion
- **Data Source:** HHS Office of Refugee Resettlement — UAC Program operational data

---

## Context

This project was completed as part of the Unified Mentor program in collaboration with the U.S. Department of Health and Human Services. It delivers a policy-aligned healthcare analytics framework that empowers stakeholders to understand, evaluate, and improve the delivery of federally mandated child care services.

---

*U.S. Department of Health and Human Services | Office of Refugee Resettlement | UAC Program Analytics Division*
