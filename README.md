# 📊 InsightX: Customer Behavior & Campaign Intelligence

## Project Overview

An **end-to-end marketing analytics platform** using **Python, SQL, ML, and Power BI** to evaluate campaign performance, segment customers and optimize ROI. 

**Analyzed 55K+ transactions**, performed **RFM analysis**, **K-Means clustering (4 segments)**, **A/B testing (+23% CTR)** and built **interactive Power BI dashboards** demonstrating **9000%+ ROI impact**.

---

## 🎯 Key Achievements

- **55K+ transaction analysis** using Python (pandas) + SQL
- **4 customer segments** identified via K-Means clustering
- **RFM analysis** for customer lifetime value modeling
- **23% CTR improvement** through segment-specific A/B testing
- **9000%+ ROI** demonstrated via campaign optimization
- **Interactive Power BI dashboards** with KPIs and drill-downs

---

## 🛠️ Technologies Used

Python: pandas, NumPy, scikit-learn, matplotlib, seaborn
SQL: SQLite, CTEs, window functions, aggregations
Power BI: DAX, slicers, dynamic measures, drill-through

---

## 📁 Project Structure

InsightX-Marketing-Analytics/
├── data/
│ ├── raw/ # 55K+ synthetic transactions
│ ├── processed/ # Cleaned + feature engineered
│ └── results/ # RFM scores, segments, KPIs
├── sql/ # Advanced queries & CTEs
├── notebooks/ # EDA + analysis
├── powerbi/ # Dashboard .pbix files
├── 01_data_generation.py
├── 02_rfm_analysis.py
├── 03_sql_pipeline.py
├── 04_kmeans_clustering.py
├── 05_segment_strategies.py
├── 06_ab_testing.py
├── 07_roi_analysis.py
├── 08_powerbi_export.py
└── README.md

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy scikit-learn matplotlib seaborn sqlite3 openpyxl

Run Complete Pipeline

python 01_data_generation.py    # Generate 55K transactions
python 02_rfm_analysis.py       # RFM scoring
python 03_sql_pipeline.py       # SQL feature engineering
python 04_kmeans_clustering.py  # 4-segment clustering
python 05_segment_strategies.py # Marketing recommendations
python 06_ab_testing.py         # A/B test simulation (+23% CTR)
python 07_roi_analysis.py       # 9000%+ ROI calculation
python 08_powerbi_export.py     # Dashboard-ready CSVs

📊 Key Results & Insights

| Segment   | Characteristics     | Strategy           | CTR Impact |
| --------- | ------------------- | ------------------ | ---------- |
| Champions | High R/F/M          | VIP offers         | +35%       |
| Loyal     | Consistent spenders | Loyalty program    | +18%       |
| At Risk   | Declining RFM       | Win-back campaigns | +22%       |
| Potential | High F/M, low R     | Nurture campaigns  | +28%       |

📈 Business Impact:

CTR: +23% across segments
ROI: 9000%+ (simulated)
Campaign Cost Reduction: 42%


📱 Interactive Dashboards

Power BI Features:

Customer segment heatmaps
A/B test performance comparison
Dynamic ROI calculator
Segment-specific KPIs
Drill-through segment analysis

🔬 Methodology

Files: powerbi/insightx_dashboard.pbix

1. Synthetic Data Generation (55K transactions)
2. RFM Analysis (Recency/Frequency/Monetary)
3. SQL Pipeline (Feature engineering)
4. K-Means Clustering (4 segments, silhouette=0.72)
5. Segment Strategy Design
6. A/B Testing (Statistical significance p<0.01)
7. ROI Modeling & KPI Dashboarding

📋 File Reference

| File                    | Purpose                    |
| ----------------------- | -------------------------- |
| 01_data_generation.py   | 55K+ transaction dataset   |
| 02_rfm_analysis.py      | RFM scoring & percentiles  |
| 04_kmeans_clustering.py | Optimal 4-cluster solution |
| 06_ab_testing.py        | T-test validated +23% CTR  |
| campaign_metrics.csv    | Dashboard source data      |
| customer_segments.csv   | Final segment assignments  |

👤 Author

Shreyansh Dubey
🌐 Portfolio: https://shreyanshdubey09.github.io
💼 LinkedIn: https://linkedin.com/in/shreyanshdubey09
🐙 GitHub: https://github.com/ShreyanshDubey09
✉️ Email: sdubey0009999@gmail.com

InsightX transforms raw transaction data into actionable marketing intelligence, demonstrating production-ready data science skills for enterprise environments.
