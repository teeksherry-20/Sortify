import pandas as pd
import numpy as np
import json
from js import document, alert as js_alert, window, Plotly, console
from io import StringIO

# Extended CSV data with sample records
csv_data = """Year,Month,Date,Location (city),Waste_Type,Waste_Source,Quantity_kg,Carbon_Footprint_kgCO2
2023,1,15,Mumbai,Plastic,household,150,900.0
2023,1,20,Delhi,Organic,commercial,300,60.0
2023,2,10,Pune,Glass,household,100,50.0
2023,2,25,Bengaluru,E-Waste,industrial,500,1250.0
2023,3,5,Chennai,Hazardous,commercial,80,320.0
2023,3,18,Mumbai,Plastic,household,180,1080.0
2023,4,8,Delhi,Organic,municipal,400,80.0
2023,4,22,Pune,Glass,commercial,250,125.0
2023,5,12,Bengaluru,E-Waste,household,120,300.0
2023,5,28,Chennai,Hazardous,industrial,600,2400.0
2023,6,7,Mumbai,Plastic,commercial,320,1920.0
2023,6,19,Delhi,Organic,household,200,40.0
2023,7,3,Pune,Glass,industrial,800,400.0
2023,7,25,Bengaluru,E-Waste,commercial,280,700.0
2023,8,11,Chennai,Hazardous,household,45,180.0
2023,8,29,Mumbai,Plastic,municipal,450,2700.0
2023,9,14,Delhi,Organic,commercial,380,76.0
2023,9,26,Pune,Glass,household,95,47.5
2023,10,9,Bengaluru,E-Waste,institution,350,875.0
2023,10,23,Chennai,Hazardous,commercial,120,480.0
2023,11,6,Mumbai,Plastic,household,210,1260.0
2023,11,20,Delhi,Organic,municipal,520,104.0
2023,12,4,Pune,Glass,commercial,310,155.0
2023,12,18,Bengaluru,E-Waste,household,160,400.0
2024,1,10,Chennai,Hazardous,industrial,750,3000.0
2024,1,24,Mumbai,Plastic,commercial,380,2280.0
2024,2,8,Delhi,Organic,household,280,56.0
2024,2,22,Pune,Glass,institution,420,210.0
2024,3,7,Bengaluru,E-Waste,commercial,390,975.0
2024,3,21,Chennai,Hazardous,household,65,260.0
2024,4,5,Mumbai,Plastic,municipal,510,3060.0
2024,4,19,Delhi,Organic,commercial,440,88.0
2024,5,3,Pune,Glass,household,130,65.0
2024,5,17,Bengaluru,E-Waste,industrial,620,1550.0
2024,6,1,Chennai,Hazardous,commercial,180,720.0
2024,6,15,Mumbai,Plastic,household,240,1440.0
2024,7,9,Delhi,Organic,municipal,590,118.0
2024,7,23,Pune,Glass,commercial,360,180.0
2024,8,6,Bengaluru,E-Waste,household,195,487.5
2024,8,20,Chennai,Hazardous,institution,290,1160.0
2024,9,4,Mumbai,Plastic,commercial,425,2550.0
2024,9,18,Delhi,Organic,household,310,62.0
2024,10,2,Pune,Glass,industrial,890,445.0
2024,10,16,Bengaluru,E-Waste,commercial,410,1025.0
2024,11,1,Chennai,Hazardous,household,75,300.0
2024,11,15,Mumbai,Plastic,municipal,580,3480.0
2024,12,9,Delhi,Organic,commercial,480,96.0
2024,12,23,Pune,Glass,household,155,77.5
2025,1,7,Bengaluru,E-Waste,institution,450,1125.0
2025,1,21,Chennai,Hazardous,commercial,210,840.0"""

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