import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from datetime import datetime, timedelta
# from streamlit_autorefresh import st_autorefresh

# st_autorefresh(interval=60 * 1000, key="data_refresh")
# Chnage
# --- PAGE SETTINGS ---
st.set_page_config(page_title="Weekly Productivity Dashboard", page_icon="📈", layout="wide")

# --- STYLE ---
def color_productivity(val):
    color = 'green' if val >= 70 else 'orange' if val >= 40 else 'red'
    return f'color: {color}'

# --- TITLE ---
st.title("📈 Weekly Employee Productivity Dashboard")
st.markdown("---")

# --- DATE RANGE FILTER ---
date_range = st.date_input("📅 Select start and end date", value=(datetime.today() - timedelta(days=7), datetime.today()))

# Ensure valid selection
if isinstance(date_range, tuple) and len(date_range) == 2:
    week_start, week_end = date_range
    st.write(f"📆 Showing data from `{week_start.strftime('%Y-%m-%d')}` to `{week_end.strftime('%Y-%m-%d')}`")
else:
    st.error("❗ Please select both a start and end date.")
    st.stop()
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123asd!@#",
#     database="employee_monitoring"
# )
# --- DATABASE CONNECTION ---
conn = mysql.connector.connect(
    host="fdb1030.awardspace.net",
    user="4625513_employeemonitoring",
    password="123asd!@#",
    database="4625513_employeemonitoring"
)

cursor = conn.cursor()

# Fetching data within the selected date range
cursor.execute("""
    SELECT 
    DAYNAME(timestamp_start) AS day_name,
    label,
    SUM(total_time_seconds) AS total_time
    FROM action_logs
    WHERE DATE(timestamp_start) BETWEEN %s AND %s
    AND DAYOFWEEK(timestamp_start) != 1  -- 1 = Sunday in MySQL
    GROUP BY day_name, label
    ORDER BY FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');
""", (week_start, week_end))
data = cursor.fetchall()

cursor.close()
conn.close()

# --- DATA PROCESSING ---
severity_levels = {
    'Arriving': 'Normal', 'Closing_Door': 'Normal', 'Conversation': 'Normal', 'Drinking_Water': 'Normal', 
    'Eating': 'Normal', 'Greeting': 'Normal', 'Person_Writing_on_paper': 'Normal', 'Sitting_Down': 'Normal', 
    'Standing': 'Normal', 'Working': 'Normal', 'opening_door': 'Normal', 'standing_up_employee': 'Normal',
    'Idle': 'Bad', 'Leaving': 'Bad', 'Sleeping': 'Bad', 'Sneezing': 'Bad', 'falling_down': 'Worst', 'using_phone': 'Worst'
}

df = pd.DataFrame(data, columns=["Day", "Label", "Total_Time_Seconds"])

productive_time, bad_time, worst_time = {}, {}, {}

for _, row in df.iterrows():
    day, label, total_time = row['Day'], row['Label'], row['Total_Time_Seconds']
    severity = severity_levels.get(label, 'Normal')
    if severity == 'Normal':
        productive_time[day] = productive_time.get(day, 0) + total_time
    elif severity == 'Bad':
        bad_time[day] = bad_time.get(day, 0) + total_time
    elif severity == 'Worst':
        worst_time[day] = worst_time.get(day, 0) + total_time

# Prepare Final Data
all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

final_data = []

for day in all_days:
    prod_time = productive_time.get(day, 0)
    bad_time_val = bad_time.get(day, 0)
    worst_time_val = worst_time.get(day, 0)
    total_time = prod_time + bad_time_val + worst_time_val
    productivity_percent = (prod_time / total_time * 100) if total_time > 0 else 0
    final_data.append({
        'Day': day,
        'Productive Time (s)': prod_time,
        'Bad Time (s)': bad_time_val,
        'Worst Time (s)': worst_time_val,
        'Total Time (s)': total_time,
        'Productivity %': productivity_percent
    })

final_df = pd.DataFrame(final_data)

# --- METRICS SECTION ---
st.subheader("✨ Weekly Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Average Productivity %", value=f"{final_df['Productivity %'].mean():.2f}%")
with col2:
    st.metric(label="Total Productive Time (s)", value=f"{final_df['Productive Time (s)'].sum():,.0f} sec")
with col3:
    st.metric(label="Total Wasted Time (s)", value=f"{(final_df['Bad Time (s)'].sum() + final_df['Worst Time (s)'].sum()):,.0f} sec")

st.markdown("---")

# --- DATAFRAME ---
st.subheader("📋 Detailed Day-wise Data")
st.dataframe(
    final_df.style.applymap(color_productivity, subset=['Productivity %']).format({
        'Productive Time (s)': "{:,.0f}",
        'Bad Time (s)': "{:,.0f}",
        'Worst Time (s)': "{:,.0f}",
        'Total Time (s)': "{:,.0f}",
        'Productivity %': "{:.2f}%"
    }),
    use_container_width=True
)
st.markdown("---")

# --- CHARTS ---
st.subheader("📈 Productivity Trend")
fig_prod = px.line(
    final_df,
    x="Day",
    y="Productivity %",
    markers=True,
    line_shape='spline',
    title="Productivity % Over Days",
    labels={"Productivity %": "Productivity (%)"},
)
fig_prod.update_traces(line_color='green')
st.plotly_chart(fig_prod, use_container_width=True)

# Stacked Bar Chart
st.subheader("🧱 Productive vs Bad vs Worst Time")
fig_time = go.Figure(data=[
    go.Bar(name='Productive Time', x=final_df['Day'], y=final_df['Productive Time (s)'], marker_color='green'),
    go.Bar(name='Bad Time', x=final_df['Day'], y=final_df['Bad Time (s)'], marker_color='orange'),
    go.Bar(name='Worst Time', x=final_df['Day'], y=final_df['Worst Time (s)'], marker_color='red')
])
fig_time.update_layout(barmode='stack', xaxis_title="Day", yaxis_title="Seconds", title="Productive vs Bad vs Worst Time")
st.plotly_chart(fig_time, use_container_width=True)

# Wasted Time Trend
st.subheader("📉 Wasted Time Trend")
final_df['Wasted Time (s)'] = final_df['Bad Time (s)'] + final_df['Worst Time (s)']

fig_waste = px.line(
    final_df,
    x="Day",
    y="Wasted Time (s)",
    markers=True,
    line_shape='spline',
    title="Wasted Time Trend",
)
waste_color = 'green' if final_df['Wasted Time (s)'].iloc[-1] < final_df['Wasted Time (s)'].iloc[0] else 'red'
fig_waste.update_traces(line_color=waste_color)
st.plotly_chart(fig_waste, use_container_width=True)

st.markdown("---")
st.caption("Designed with ❤️ by M.Daniyal Tariq")
