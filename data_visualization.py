import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Create the output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Load the CSV files into DataFrames
iss_df = pd.read_csv('data_source/MCDB_clean_iss_2024-05-17_09_42_05.csv')
ret_df = pd.read_csv('data_source/MCDB_clean_ret_2024-05-17_09_42_05.csv')

# Clean 'Vintage' column
def clean_vintage(v):
    try:
        return int(float(v))
    except ValueError:
        return None

iss_df['Vintage'] = iss_df['Vintage'].apply(clean_vintage)
ret_df['Vintage'] = ret_df['Vintage'].apply(clean_vintage)

# Drop rows with invalid 'Vintage'
iss_df.dropna(subset=['Vintage'], inplace=True)
ret_df.dropna(subset=['Vintage'], inplace=True)

# Add 'Month' and 'Year' columns for visualizations
iss_df['Month'] = pd.to_datetime(iss_df['Vintage'], format='%Y').dt.strftime('%B')
ret_df['Month'] = pd.to_datetime(ret_df['Vintage'], format='%Y').dt.strftime('%B')
ret_df['Year'] = ret_df['Vintage'].astype(int)

# Ensure 'Tons Delivered' is numeric
ret_df['Tons Delivered'] = pd.to_numeric(ret_df['Tons Delivered'], errors='coerce')

# Visualization 1: Tons Delivered per Month by Year (Stacked Bar Chart)
fig1 = px.bar(ret_df, x='Month', y='Tons Delivered', color='Year', title='Tons Delivered per Month by Year')
fig1.write_html('output/tons_delivered_per_month_by_year.html')

# Visualization 2: Monthly Deliveries by Year (Line Chart)
fig2 = px.line(ret_df, x='Month', y='Tons Delivered', color='Year', title='Monthly Deliveries by Year')
fig2.write_html('output/monthly_deliveries_by_year.html')

# Visualization 3: Total Deliveries (Single Value Display)
total_deliveries = ret_df['Tons Delivered'].sum()
fig3 = go.Figure()
fig3.add_trace(go.Indicator(
    mode="number",
    value=total_deliveries,
    title={"text": "Total Deliveries"}
))
fig3.write_html('output/total_deliveries.html')

# Visualization 4: Deliveries by Registry (Bar Chart)
client_df = ret_df.groupby('Registry')['Tons Delivered'].sum().reset_index()
fig4 = px.bar(client_df, x='Registry', y='Tons Delivered', title='Deliveries by Registry')
fig4.write_html('output/deliveries_by_registry.html')

# Visualization 5: Annual Deliveries by Vintage (Stacked Area Chart)
fig5 = px.area(ret_df, x='Year', y='Tons Delivered', color='Year', title='Annual Deliveries by Vintage')
fig5.write_html('output/annual_deliveries_by_vintage.html')

# Visualization 6: Availability by Developer (Bar Chart)
developer_df = iss_df.groupby('Developer')['Available'].sum().reset_index()
fig6 = px.bar(developer_df, x='Developer', y='Available', title='Availability by Developer')
fig6.write_html('output/availability_by_developer.html')

# Visualization 7: Activities Distribution (Pie Chart)
activity_df = ret_df.groupby('Activity')['Tons Delivered'].sum().reset_index()
fig7 = px.pie(activity_df, names='Activity', values='Tons Delivered', title='Activities Distribution')
fig7.write_html('output/activities_distribution.html')

print("Visualizations saved as HTML files in the 'output' folder.")
