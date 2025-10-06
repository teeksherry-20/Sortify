import pandas as pd
import numpy as np
import json
from js import document, alert as js_alert, window, Plotly, console
from io import StringIO

# Extended CSV data with sample records
csv_data = """Year,Month,Date,Location (city),Waste_Type,Waste_Source,Quantity_kg,Carbon_Footprint_kgCO2
2020,1,13,Pune,Glass,household,120,24.0
2020,1,8,Mumbai,Hazardous,household,15,37.5
2020,2,4,Pune,Plastic,commercial,300,1830.0
2020,2,14,Mumbai,E-Waste,commercial,150,135.0
2020,3,1,Bengaluru,Glass,institution,450,90.0
2020,3,31,Bengaluru,Organic,commercial,500,50.0
2020,4,18,Chennai,Hazardous,institution,80,200.0
2020,4,15,Chennai,Plastic,municipal,200,1220.0
2020,5,21,Hyderabad,Glass,industrial,1500,300.0
2020,5,31,Hyderabad,E-Waste,municipal,100,90.0
2020,6,16,Delhi,Hazardous,industrial,5000,12500.0
2020,6,22,Delhi,Organic,municipal,400,40.0
2020,7,6,Ahmedabad,Glass,household,200,40.0
2020,7,12,Ahmedabad,Glass,commercial,1000,200.0
2020,8,9,Ahmedabad,Hazardous,industrial,3000,7500.0
2020,8,30,Ahmedabad,Hazardous,commercial,1000,2500.0
2020,9,23,Ahmedabad,Hazardous,municipal,1500,3750.0
2020,9,30,Kolkata,Glass,municipal,2000,400.0
2020,10,20,Kolkata,Hazardous,institution,120,300.0
2020,10,22,Kolkata,Hazardous,industrial,5500,13750.0
2020,11,7,Kolkata,Hazardous,commercial,1200,3000.0
2020,11,16,Kolkata,Hazardous,municipal,2000,5000.0
2020,12,13,Pune,Glass,commercial,1200,240.0
2020,12,21,Pune,Hazardous,industrial,5000,12500.0
2020,12,28,Pune,Hazardous,commercial,1200,3000.0
2021,1,1,Pune,Hazardous,municipal,2000,5000.0
2021,1,13,Mumbai,Glass,municipal,2500,500.0
2021,1,8,Mumbai,Hazardous,industrial,6000,15000.0
2021,2,4,Mumbai,Hazardous,commercial,1500,3750.0
2021,2,14,Mumbai,Hazardous,municipal,2500,6250.0
2021,3,1,Pune,Glass,household,110,22.0
2021,3,31,Mumbai,Hazardous,household,25,62.5
2021,4,18,Pune,Plastic,commercial,280,1708.0
2021,4,15,Mumbai,E-Waste,commercial,140,126.0
2021,5,21,Bengaluru,Glass,institution,430,86.0
2021,5,31,Bengaluru,Organic,commercial,490,49.0
2021,6,16,Chennai,Hazardous,institution,75,187.5
2021,6,22,Chennai,Plastic,municipal,210,1281.0
2021,7,6,Pune,Organic,household,320,32.0
2021,7,12,Mumbai,Glass,industrial,1500,300.0
2021,8,9,Bengaluru,Hazardous,household,45,112.5
2021,8,30,Chennai,E-Waste,institution,160,144.0
2021,9,23,Pune,Plastic,institution,310,1891.0
2021,9,30,Mumbai,Organic,household,200,20.0
2021,10,20,Bengaluru,Glass,municipal,420,84.0
2021,10,22,Chennai,Hazardous,commercial,85,212.5
2021,11,7,Pune,E-Waste,industrial,1200,1080.0
2021,11,16,Mumbai,Plastic,institution,230,1403.0
2021,11,13,Bengaluru,Organic,municipal,510,51.0
2021,12,21,Chennai,Glass,household,180,36.0
2021,12,28,Pune,Hazardous,commercial,40,100.0
2022,1,13,Mumbai,Glass,institution,155,31.0
2022,1,8,Bengaluru,Plastic,household,270,1647.0
2022,2,4,Chennai,Organic,commercial,480,48.0
2022,2,14,Pune,Glass,municipal,130,26.0
2022,3,1,Pune,Plastic,industrial,2900,17690.0
2022,3,31,Mumbai,Organic,institution,210,21.0
2022,4,18,Bengaluru,Glass,commercial,400,80.0
2022,4,15,Chennai,E-Waste,commercial,160,144.0
2022,5,21,Delhi,Hazardous,household,50,125.0
2022,5,31,Hyderabad,Organic,municipal,470,47.0
2022,6,16,Kolkata,Plastic,institution,230,1403.0
2022,6,22,Pune,Glass,household,120,24.0
2022,7,6,Mumbai,Hazardous,commercial,35,87.5
2022,7,12,Bengaluru,E-Waste,household,170,153.0
2022,8,9,Chennai,Plastic,industrial,2000,12200.0
2022,8,30,Pune,Organic,institution,310,31.0
2022,9,23,Mumbai,Glass,household,150,30.0
2022,9,30,Bengaluru,Hazardous,commercial,45,112.5
2022,10,20,Chennai,E-Waste,institution,180,162.0
2022,10,22,Pune,Plastic,municipal,300,1830.0
2022,11,7,Mumbai,Organic,household,220,22.0
2022,11,16,Bengaluru,Glass,institution,410,82.0
2022,11,13,Chennai,Hazardous,commercial,80,200.0
2022,12,21,Delhi,E-Waste,household,140,126.0
2022,12,28,Hyderabad,Plastic,commercial,250,1525.0
2023,1,13,Kolkata,Organic,industrial,4900,490.0
2023,1,8,Pune,Glass,household,125,25.0
2023,2,4,Mumbai,Hazardous,institution,30,75.0
2023,2,14,Pune,Plastic,household,300,1830.0
2023,3,1,Mumbai,Organic,commercial,230,23.0
2023,3,31,Bengaluru,Glass,industrial,4200,840.0
2023,4,18,Chennai,E-Waste,commercial,170,153.0
2023,4,15,Delhi,Hazardous,household,55,137.5
2023,5,21,Hyderabad,Organic,municipal,480,48.0
2023,5,31,Kolkata,Plastic,institution,240,1464.0
2023,6,16,Pune,Glass,household,130,26.0
2023,6,22,Mumbai,Hazardous,commercial,40,100.0
2023,7,6,Bengaluru,E-Waste,household,180,162.0
2023,7,12,Chennai,Plastic,municipal,210,1281.0
2023,8,9,Pune,Organic,institution,320,32.0
2023,8,30,Mumbai,Glass,household,155,31.0
2023,9,23,Bengaluru,Hazardous,commercial,50,125.0
2023,9,30,Chennai,E-Waste,institution,190,171.0
2023,10,20,Pune,Plastic,municipal,310,1891.0
2023,10,22,Mumbai,Organic,household,240,24.0
2023,11,7,Bengaluru,Glass,institution,430,86.0
2023,11,16,Chennai,Hazardous,commercial,85,212.5
2023,11,13,Delhi,E-Waste,household,150,135.0
2023,12,21,Hyderabad,Plastic,commercial,260,1586.0
2023,12,28,Kolkata,Organic,municipal,500,50.0
2024,1,13,Pune,Glass,household,140,28.0
2024,1,8,Mumbai,Hazardous,institution,35,87.5
2024,2,4,Pune,Plastic,household,310,1891.0
2024,2,14,Mumbai,Organic,commercial,250,25.0
2024,3,1,Bengaluru,Glass,institution,440,88.0
2024,3,31,Chennai,E-Waste,industrial,1800,1620.0
2024,4,18,Delhi,Hazardous,household,60,150.0
2024,4,15,Hyderabad,Organic,municipal,490,49.0
2024,5,21,Kolkata,Plastic,institution,250,1525.0
2024,5,31,Pune,Glass,household,135,27.0
2024,6,16,Mumbai,Hazardous,commercial,45,112.5
2024,6,22,Bengaluru,E-Waste,household,190,171.0
2024,7,6,Chennai,Plastic,municipal,220,1342.0
2024,7,12,Pune,Organic,institution,330,33.0
2024,8,9,Mumbai,Glass,household,160,32.0
2024,8,30,Bengaluru,Hazardous,commercial,55,137.5
2024,9,23,Chennai,E-Waste,institution,200,180.0
2024,9,30,Pune,Plastic,municipal,320,1952.0
2024,10,20,Mumbai,Organic,household,250,25.0
2024,10,22,Bengaluru,Glass,institution,450,90.0
2024,11,7,Chennai,Hazardous,commercial,90,225.0
2024,11,16,Delhi,E-Waste,household,160,144.0
2024,11,13,Hyderabad,Plastic,industrial,2700,16470.0
2024,12,21,Kolkata,Organic,municipal,510,51.0
2024,12,28,Pune,Glass,household,145,29.0
2025,1,13,Mumbai,Hazardous,institution,40,100.0
2025,1,8,Pune,Plastic,household,330,2013.0
2025,2,4,Mumbai,Organic,commercial,260,26.0
2025,2,14,Bengaluru,Glass,institution,460,92.0
2025,3,1,Chennai,E-Waste,commercial,190,171.0
2025,3,31,Delhi,Hazardous,household,65,162.5
2025,4,18,Hyderabad,Organic,municipal,500,50.0
2025,4,15,Kolkata,Plastic,industrial,2600,15860.0
2025,5,21,Pune,Glass,household,140,28.0
2025,5,31,Mumbai,Hazardous,commercial,50,125.0
2025,6,16,Bengaluru,E-Waste,household,200,180.0
2025,6,22,Chennai,Plastic,municipal,230,1403.0
2025,7,6,Pune,Organic,institution,340,34.0
2025,7,12,Mumbai,Glass,household,165,33.0
2025,8,9,Bengaluru,Hazardous,commercial,60,150.0
2025,8,30,Chennai,E-Waste,institution,210,189.0
2025,9,23,Pune,Plastic,municipal,330,2013.0
2025,9,30,Mumbai,Organic,household,260,26.0
2025,10,20,Bengaluru,Glass,institution,470,94.0
2025,10,22,Chennai,Hazardous,commercial,95,237.5
2025,11,7,Delhi,E-Waste,household,170,153.0
2025,11,16,Hyderabad,Plastic,industrial,2800,17080.0
2025,11,13,Kolkata,Organic,municipal,520,52.0
2025,12,21,Pune,Glass,household,150,30.0
2025,12,28,Mumbai,Hazardous,institution,45,112.5"""

# Load data
df = pd.read_csv(StringIO(csv_data))

current_user = None
emission_factors = {
    "Plastic": 6.0,
    "Organic": 0.2,
    "Glass": 0.5,
    "E-Waste": 2.5,
    "Hazardous": 4.0,
    "Paper": 1.5
}

def show_dashboard():
    """Display main dashboard with statistics and recent records"""
    content = document.getElementById("content-section")
    
    total_waste = df['Quantity_kg'].sum()
    total_carbon = df['Carbon_Footprint_kgCO2'].sum()
    avg_waste = df['Quantity_kg'].mean()
    record_count = len(df)
    
    # Get top location and waste type
    top_location = df.groupby('Location (city)')['Quantity_kg'].sum().idxmax()
    top_waste_type = df.groupby('Waste_Type')['Quantity_kg'].sum().idxmax()
    
    html = f"""
    <h2 style="margin-bottom: 20px;">Dashboard Overview</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <h3>{record_count}</h3>
            <p>Total Records</p>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>{total_waste:,.0f}</h3>
            <p>Total Waste (kg)</p>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3>{total_carbon:,.0f}</h3>
            <p>Carbon Footprint (kg CO2)</p>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h3>{avg_waste:,.1f}</h3>
            <p>Avg Waste/Record (kg)</p>
        </div>
    </div>
    
    <div class="stats-grid" style="margin-top: 20px;">
        <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <h3>{top_location}</h3>
            <p>Top Location</p>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
            <h3>{top_waste_type}</h3>
            <p>Most Common Waste</p>
        </div>
    </div>
    
    <h3 style="margin-top: 30px; margin-bottom: 15px;">Recent Records</h3>
    <div style="overflow-x: auto;">
    <table class="data-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Location</th>
                <th>Waste Type</th>
                <th>Source</th>
                <th>Quantity (kg)</th>
                <th>Carbon (kg CO2)</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for _, row in df.tail(15).iterrows():
        html += f"""
            <tr>
                <td>{row['Year']}-{str(row['Month']).zfill(2)}-{str(row['Date']).zfill(2)}</td>
                <td>{row['Location (city)']}</td>
                <td>{row['Waste_Type']}</td>
                <td>{row['Waste_Source']}</td>
                <td>{row['Quantity_kg']:.1f}</td>
                <td>{row['Carbon_Footprint_kgCO2']:.1f}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    </div>
    """
    
    content.innerHTML = html

def show_waste_distribution():
    """Display waste type distribution with pie and bar charts"""
    content = document.getElementById("content-section")
    
    dist = df.groupby('Waste_Type')['Quantity_kg'].sum().sort_values(ascending=False)
    
    html = """
    <h2>Waste Type Distribution</h2>
    <div id="pie-chart" class="chart-container"></div>
    <div id="bar-chart" class="chart-container"></div>
    """
    
    content.innerHTML = html
    
    # Create pie chart
    pie_data = [{
        'values': dist.values.tolist(),
        'labels': dist.index.tolist(),
        'type': 'pie',
        'hole': 0.4,
        'marker': {'colors': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#43e97b', '#38f9d7']}
    }]
    
    pie_layout = {
        'title': 'Waste Distribution by Type',
        'showlegend': True,
        'height': 400
    }
    
    Plotly.newPlot('pie-chart', pie_data, pie_layout)
    
    # Create bar chart
    bar_data = [{
        'x': dist.index.tolist(),
        'y': dist.values.tolist(),
        'type': 'bar',
        'marker': {'color': '#667eea'}
    }]
    
    bar_layout = {
        'title': 'Total Waste by Type (kg)',
        'xaxis': {'title': 'Waste Type'},
        'yaxis': {'title': 'Quantity (kg)'},
        'height': 400
    }
    
    Plotly.newPlot('bar-chart', bar_data, bar_layout)

def show_carbon_reports():
    """Display carbon footprint analysis with trend charts"""
    content = document.getElementById("content-section")
    
    monthly = df.groupby(['Year', 'Month'])['Carbon_Footprint_kgCO2'].sum().reset_index()
    monthly['Date'] = monthly['Year'].astype(str) + '-' + monthly['Month'].astype(str).str.zfill(2)
    
    by_type = df.groupby('Waste_Type')['Carbon_Footprint_kgCO2'].sum().sort_values(ascending=False)
    
    html = """
    <h2>Carbon Footprint Analysis</h2>
    <div class="alert alert-info">
        Carbon footprint measured in kg CO2 emissions per waste type
    </div>
    <div id="carbon-trend" class="chart-container"></div>
    <div id="carbon-by-type" class="chart-container"></div>
    """
    
    content.innerHTML = html
    
    # Trend line
    trend_data = [{
        'x': monthly['Date'].tolist(),
        'y': monthly['Carbon_Footprint_kgCO2'].tolist(),
        'type': 'scatter',
        'mode': 'lines+markers',
        'marker': {'color': '#f5576c', 'size': 8},
        'line': {'width': 3}
    }]
    
    trend_layout = {
        'title': 'Monthly Carbon Emissions Trend',
        'xaxis': {'title': 'Month'},
        'yaxis': {'title': 'CO2 Emissions (kg)'},
        'height': 400
    }
    
    Plotly.newPlot('carbon-trend', trend_data, trend_layout)
    
    # By type
    type_data = [{
        'x': by_type.index.tolist(),
        'y': by_type.values.tolist(),
        'type': 'bar',
        'marker': {'color': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#43e97b', '#38f9d7']}
    }]
    
    type_layout = {
        'title': 'Total Carbon Footprint by Waste Type',
        'xaxis': {'title': 'Waste Type'},
        'yaxis': {'title': 'CO2 Emissions (kg)'},
        'height': 400
    }
    
    Plotly.newPlot('carbon-by-type', type_data, type_layout)

def show_location_analysis():
    """Display location-based waste analysis"""
    content = document.getElementById("content-section")
    
    by_location = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values(ascending=False)
    
    html = """
    <h2>Location-Based Analysis</h2>
    <div id="location-chart" class="chart-container"></div>
    """
    
    content.innerHTML = html
    
    chart_data = [{
        'x': by_location.values.tolist(),
        'y': by_location.index.tolist(),
        'type': 'bar',
        'orientation': 'h',
        'marker': {'color': '#43e97b'}
    }]
    
    layout = {
        'title': 'Total Waste by Location',
        'xaxis': {'title': 'Quantity (kg)'},
        'yaxis': {'title': 'Location'},
        'height': 500
    }
    
    Plotly.newPlot('location-chart', chart_data, layout)

def show_trend_forecast():
    """Display trend forecast with linear regression"""
    content = document.getElementById("content-section")
    
    monthly_data = df.groupby(['Year', 'Month'])['Quantity_kg'].sum().reset_index()
    monthly_data['Time'] = range(len(monthly_data))
    monthly_data['Date'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str).str.zfill(2)
    
    # Simple linear regression
    X = monthly_data['Time'].values
    y = monthly_data['Quantity_kg'].values
    coeffs = np.polyfit(X, y, 1)
    trend_line = coeffs[0] * X + coeffs[1]
    
    # Forecast next 6 months
    future_X = np.arange(len(monthly_data), len(monthly_data) + 6)
    forecast = coeffs[0] * future_X + coeffs[1]
    
    html = """
    <h2>Waste Generation Forecast</h2>
    <div class="alert alert-info">
        Linear regression forecast for next 6 months based on historical trends
    </div>
    <div id="forecast-chart" class="chart-container"></div>
    """
    
    content.innerHTML = html
    
    trace1 = {
        'x': monthly_data['Date'].tolist(),
        'y': y.tolist(),
        'name': 'Actual',
        'type': 'scatter',
        'mode': 'lines+markers',
        'marker': {'color': '#667eea', 'size': 8}
    }
    
    trace2 = {
        'x': monthly_data['Date'].tolist(),
        'y': trend_line.tolist(),
        'name': 'Trend',
        'type': 'scatter',
        'mode': 'lines',
        'line': {'dash': 'dash', 'color': '#f5576c'}
    }
    
    future_dates = ['Future-' + str(i+1) for i in range(6)]
    trace3 = {
        'x': future_dates,
        'y': forecast.tolist(),
        'name': 'Forecast',
        'type': 'scatter',
        'mode': 'lines+markers',
        'marker': {'color': '#43e97b', 'size': 8}
    }
    
    layout = {
        'title': 'Waste Generation Trend & Forecast',
        'xaxis': {'title': 'Time Period'},
        'yaxis': {'title': 'Quantity (kg)'},
        'height': 500
    }
    
    Plotly.newPlot('forecast-chart', [trace1, trace2, trace3], layout)

def export_csv():
    """Export data as CSV"""
    csv_string = df.to_csv(index=False)
    js_alert("CSV export: In a full implementation, this would download a file. Data is ready in the console.")
    console.log(csv_string)

def export_summary():
    """Export summary report"""
    summary = f"""
SORTIFY Waste Management Summary Report
========================================

Total Records: {len(df)}
Total Waste: {df['Quantity_kg'].sum():.2f} kg
Total Carbon: {df['Carbon_Footprint_kgCO2'].sum():.2f} kg CO2

Top Locations:
{df.groupby('Location (city)')['Quantity_kg'].sum().sort_values(ascending=False).head(3).to_string()}

Waste Type Distribution:
{df.groupby('Waste_Type')['Quantity_kg'].sum().to_string()}
"""
    js_alert("Summary generated. Check console for full report.")
    console.log(summary)

# Expose functions to JavaScript
window.show_dashboard = show_dashboard
window.show_waste_distribution = show_waste_distribution
window.show_carbon_reports = show_carbon_reports
window.show_location_analysis = show_location_analysis
window.show_trend_forecast = show_trend_forecast
window.export_csv = export_csv
window.export_summary = export_summary