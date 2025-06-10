# Power BI Dashboard Setup Instructions

## Step 1: Import Data
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Import these files in order:
   - `powerbi/dashboard_main_data.csv` (Main table)
   - `powerbi/performance_summary.csv` (KPIs)
   - `powerbi/daily_performance.csv` (Time series)
   - `powerbi/segment_details.csv` (Segments)
   - `powerbi/campaign_comparison.csv` (Campaigns)

## Step 2: Create Relationships
1. Go to "Model" view
2. Create relationships between tables:
   - Link tables by `segment_name`
   - Link daily_performance to main data by `segment_name`
   - Create date table for time intelligence

## Step 3: Create Key Measures (DAX)

-- Overall CTR Improvement
CTR_Improvement =
DIVIDE(
CALCULATE(AVERAGE([ctr]), [test_group] = "B") -
CALCULATE(AVERAGE([ctr]), [test_group] = "A"),
CALCULATE(AVERAGE([ctr]), [test_group] = "A")
) * 100

-- Total Customers
Total_Customers = DISTINCTCOUNT([customer_id])

-- Campaign ROI
Campaign_ROI =
DIVIDE([Total_Revenue] - [Total_Costs], [Total_Costs]) * 100

-- Conversion Rate
Conversion_Rate = DIVIDE([Total_Conversions], [Total_Clicks])




## Step 4: Dashboard Pages

### Page 1: Executive Summary
- **Card Visuals:**
  - Total customers analyzed (12,000)
  - Customer segments (4)
  - CTR improvement (23%)
  - Total ROI

- **Key Charts:**
  - Donut: Segment distribution
  - Bar: CTR by segment and test group
  - Line: Monthly performance trend

### Page 2: Customer Segmentation
- **Visualizations:**
  - Scatter plot: Frequency vs Monetary (colored by segment)
  - Heatmap: Segment characteristics
  - Table: Detailed segment metrics
  - Histogram: Age distribution by segment

### Page 3: A/B Testing Results
- **Charts:**
  - Clustered column: CTR comparison
  - Funnel: Email → Click → Conversion
  - Waterfall: Revenue breakdown
  - Matrix: Performance by segment and campaign

### Page 4: ROI Analysis
- **Visualizations:**
  - Gauge: ROI by campaign type
  - Bar: Revenue by segment
  - Line: Daily performance trends
  - KPI cards: Cost metrics

## Step 5: Interactive Features
1. **Slicers:** Date range, segment, campaign type
2. **Cross-filtering:** Enable between all visuals
3. **Drill-through:** From summary to detailed customer lists
4. **Bookmarks:** Create navigation between insights

## Step 6: Formatting
- **Color scheme:** Use consistent brand colors
- **Fonts:** Professional, readable fonts
- **Layout:** Clean, organized dashboard structure
- **Mobile:** Optimize for mobile viewing

## Key Insights to Highlight
✅ **50K+ transactions analyzed**
✅ **4 distinct customer segments identified**
✅ **23% CTR improvement achieved**
✅ **Targeted campaigns significantly outperformed generic**
✅ **Champions segment shows highest ROI**
