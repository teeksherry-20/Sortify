import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
df = pd.read_csv("C:\\Users\\teeks\\OneDrive\\Desktop\\waste.csv")

# Emission factors in kg CO2 per kg of waste
emission = { 
    "Plastic": 6.0,
    "Organic": 0.2,
    "Glass": 0.5,
    "E-Waste": 2.5,
    "Hazardous": 4.0,
    "Paper": 1.5
}

# Global targets dictionary
targets = {
    'monthly_waste': None,
    'monthly_carbon': None,
    'yearly_waste': None,
    'yearly_carbon': None
}

# Input username and password
print("=== WASTE MANAGEMENT SYSTEM LOGIN ===")
print("User Roles:")    
print("1. Admin (username: admin, password: admin123)")
print("2. Waste Collector (username: waste collector, password: collector123)")
print("3. Municipal Officer (username: municipal officer, password: officer123)")
print("4. Household/Institution (username: household/institution, password: user123)")

username= input("Enter username: ")
password= input("Enter password: ")
# CHOICE 1 - Insert Record
def insert_record():
    print("Insert New Record")
    year = input("Enter Year (YYYY): ")
    month = input("Enter Month (MM): ")
    date = input("Enter Date (DD): ")
    location = input("Enter Location (city): ")
    waste_type = input("Enter Waste Type: ")
    waste_source = input("Enter Waste Source: ")
    quantity = float(input("Enter Quantity (kg): "))
    carbon = calculate_carbon(waste_type, quantity)
    
    # Append new record to DataFrame
    new_record = {
        'Year': year,
        'Month': month,
        'Date': date,
        'Location (city)': location,
        'Waste_Type': waste_type,
        'Waste_Source': waste_source,
        'Quantity_kg': quantity,
        'Carbon_Footprint_kgCO2': carbon
    }
    df.loc[len(df)] = new_record
    print("Record inserted successfully!")

# Function to calculate carbon footprint
def calculate_carbon(waste_type, quantity): 
    return quantity * emission.get(waste_type, 0)

# CHOICE 2 - Update Record
def update_record():
    print("Update Record")
    location = input("Enter Location (city) to search: ")
    waste_type = input("Enter Waste Type to search: ")
    
    # Find matching records
    records = df[(df['Location (city)'] == location) & (df['Waste_Type'] == waste_type)]
    if records.empty:
        print("No matching record found.")
        return
    print("Matching Records:")
    print(records)
    
    # Get index of record to update
    index = int(input("Enter the index of the record to update: "))
    column = input("Enter column to update: ")
    
    # Update the specified column
    if column == "Quantity_kg":
        new_quantity = float(input("Enter new quantity (kg): "))
        df.at[index, column] = new_quantity
        waste_type_value = df.at[index, 'Waste_Type']

        # Update quantity and recalculate carbon footprint
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(waste_type_value, new_quantity)
        print("Quantity updated! Carbon footprint recalculated: {} kg CO2".format(df.at[index, 'Carbon_Footprint_kgCO2']))

    # update waste type and recalculate carbon footprint   
    elif column == "Waste_Type":
        new_waste_type = input("Enter new Waste Type: ")
        df.at[index, column] = new_waste_type
        quantity_value = df.at[index, 'Quantity_kg']

        # Update waste type and recalculate carbon footprint
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(new_waste_type, quantity_value)
        print("Waste type updated! Carbon footprint recalculated: {} kg CO2".format(df.at[index, 'Carbon_Footprint_kgCO2']))

    # For other columns, just update the value
    else:
        new_value = input("Enter new value: ")
        df.at[index, column] = new_value
        print("Record updated successfully!")

# CHOICE 3 - Delete Record
def delete_record():
    print("YOU CHOSE: DELETE RECORD")
    location = input("Enter Location (city) to search: ")
    waste_type = input("Enter Waste Type to search: ")
    
    # Find matching records
    df.drop(df[(df['Location (city)'] == location) & (df['Waste_Type'] == waste_type)].index, inplace=True)
    print("Record(s) deleted successfully!")

# CHOICE 4 - Search Records
def search_record():
    print("YOU CHOSE: SEARCH RECORDS")
    location = input("Enter Location (city) to search (leave blank for all): ")
    waste_type = input("Enter Waste Type to search (leave blank for all): ")
    
    # Filter records based on input
    result = df
    if location:
        result = result[result['Location (city)'] == location]
    if waste_type:
        result = result[result['Waste_Type'] == waste_type]
    
    print("Search Results:")
    print(result)

# CHOICE 5 - Monthly Waste Trends
def monthly_trends():
    print("YOU CHOSE: MONTHLY WASTE TRENDS")
    trend = df.groupby(['Year', 'Month', 'Waste_Type'])['Quantity_kg'].sum()
    print(trend)

    # Plotting the trends
    trend.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.xlabel('Year-Month')
    plt.ylabel('Quantity (kg)')
    plt.title('Monthly Waste Trends (Stacked by Waste Type)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title='Waste Type')
    plt.show()

# CHOICE 6 - Waste Type Distribution
def waste_type_distribution():
    print("YOU CHOSE: WASTE TYPE DISTRIBUTION")
    
    distribution = df.groupby('Waste_Type')['Quantity_kg'].sum()
    print(distribution)
    plt.figure(figsize=(8, 8))
    plt.pie(distribution, labels=distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title('Overall Waste Distribution by Type')
    plt.tight_layout()
    plt.show()

# CHOICE 7 - Location-Based Waste Analysis
def location_analysis():
    print("YOU CHOSE: LOCATION-BASED WASTE ANALYSIS")
    loc_trend = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values(ascending=False)
    print(loc_trend)
    loc_trend.plot(kind='bar', figsize=(10,6), color='skyblue')
    plt.xlabel('Location')
    plt.ylabel('Total Waste (kg)')
    plt.title('Total Waste by Location')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# CHOICE 8 - Carbon Footprint Reports
def carbon_reports():
    print("YOU CHOSE: CARBON FOOTPRINT REPORTS")
    monthly = df.groupby(['Year','Month'])['Carbon_Footprint_kgCO2'].sum()
    print("\nMonthly Carbon Footprint:")
    print(monthly)
    monthly.plot(kind='line', marker='o', figsize=(10,5), color='purple', title='Monthly Carbon Footprint')
    plt.xlabel('Year-Month')
    plt.ylabel('CO2 Emissions (kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# CHOICE 9 - Interactive Search and Filter
def interactive_search_filter():
    print("YOU CHOSE: INTERACTIVE SEARCH & FILTER")
    result = df.copy()
    
    # Apply filters
    print("\nApply Filters (press Enter to skip):")
    year = input("Filter by Year (YYYY): ")
    if year:
        result = result[result['Year'] == year]
    
    month = input("Filter by Month (MM): ")
    if month:
        result = result[result['Month'] == month]
    
    location = input("Filter by Location: ")
    if location:
        result = result[result['Location (city)'].str.contains(location, case=False, na=False)]
    
    waste_type = input("Filter by Waste Type: ")
    if waste_type:
        result = result[result['Waste_Type'].str.contains(waste_type, case=False, na=False)]
    
    waste_source = input("Filter by Waste Source: ")
    if waste_source:
        result = result[result['Waste_Source'].str.contains(waste_source, case=False, na=False)]
    
    # Quantity range filter
    min_qty = input("Minimum Quantity (kg): ")
    if min_qty:
        result = result[result['Quantity_kg'] >= float(min_qty)]
    
    max_qty = input("Maximum Quantity (kg): ")
    if max_qty:
        result = result[result['Quantity_kg'] <= float(max_qty)]
    
    # Sort options
    print("\nSORT OPTIONS:")
    print("1. Sort by Quantity (Ascending)")
    print("2. Sort by Quantity (Descending)")
    print("3. Sort by Carbon Footprint (Ascending)")
    print("4. Sort by Carbon Footprint (Descending)")
    print("5. Sort by Date (Ascending)")
    print("6. Sort by Date (Descending)")
    
    sort_choice = input("Choose sort option (or press Enter to skip): ")
    
    if sort_choice == "1":
        result = result.sort_values('Quantity_kg', ascending=True)
    elif sort_choice == "2":
        result = result.sort_values('Quantity_kg', ascending=False)
    elif sort_choice == "3":
        result = result.sort_values('Carbon_Footprint_kgCO2', ascending=True)
    elif sort_choice == "4":
        result = result.sort_values('Carbon_Footprint_kgCO2', ascending=False)
    elif sort_choice == "5":
        result = result.sort_values(['Year', 'Month', 'Date'], ascending=True)
    elif sort_choice == "6":
        result = result.sort_values(['Year', 'Month', 'Date'], ascending=False)
    
    print("FILTERED RESULT ({} records) ===".format(len(result)))
    print(result)
    
    # Export option
    export = input("EXPORT RESULTS TO CSV? (y/n): ")
    if export.lower() == 'y':
        filename = input("Enter filename (without .csv): ")
        result.to_csv("{}.csv".format(filename), index=False)
        print("Results exported to {}.csv".format(filename))

# 10 - Aggregated Statistics
def aggregated_statistics():
    print("YOU CHOSE: AGGREGATED STATISTICS")
    
    print("\nOVERALL STATISTICS")
    print("Total Records: {}".format(len(df)))
    print("Total Waste Generated: {:.2f} kg".format(df['Quantity_kg'].sum()))
    print("Total Carbon Footprint: {:.2f} kg CO2".format(df['Carbon_Footprint_kgCO2'].sum()))
    print("Average Waste per Record: {:.2f} kg".format(df['Quantity_kg'].mean()))
    print("Average Carbon per Record: {:.2f} kg CO2".format(df['Carbon_Footprint_kgCO2'].mean()))
    
    print("\nSTATISTICS BY WASTE TYPE")
    by_type = df.groupby('Waste_Type').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_type)
    
    print("\nSTATISTICS BY LOCATION")
    by_location = df.groupby('Location (city)').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_location)
    
    print("\nSTATISTICS BY WASTE SOURCE")
    by_source = df.groupby('Waste_Source').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_source)
    
    print("\nSTATISTICS BY YEAR & MONTH")
    monthly_avg = df.groupby(['Year', 'Month']).agg({
        'Quantity_kg': 'sum',
        'Carbon_Footprint_kgCO2': 'sum'
    }).round(2)
    print(monthly_avg)
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Waste by Type
    by_type_sum = df.groupby('Waste_Type')['Quantity_kg'].sum()
    by_type_sum.plot(kind='bar', ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title('Total Waste by Type')
    axes[0, 0].set_ylabel('Quantity (kg)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Plot 2: Carbon by Type
    carbon_by_type = df.groupby('Waste_Type')['Carbon_Footprint_kgCO2'].sum()
    carbon_by_type.plot(kind='bar', ax=axes[0, 1], color='coral')
    axes[0, 1].set_title('Total Carbon Footprint by Type')
    axes[0, 1].set_ylabel('CO2 (kg)')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Plot 3: Waste by Location
    by_location_sum = df.groupby('Location (city)')['Quantity_kg'].sum().head(10)
    by_location_sum.plot(kind='barh', ax=axes[1, 0], color='lightgreen')
    axes[1, 0].set_title('Top 10 Locations by Waste')
    axes[1, 0].set_xlabel('Quantity (kg)')
    
    # Plot 4: Waste by Source
    by_source_sum = df.groupby('Waste_Source')['Quantity_kg'].sum()
    by_source_sum.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%')
    axes[1, 1].set_title('Waste Distribution by Source')
    axes[1, 1].set_ylabel('')
    
    plt.tight_layout()
    plt.show()

# CHOICE 11 - Monthly & Yearly Carbon Emissions
def carbon_emissions_analysis():
    print("YOU CHOSE: CARBON EMISSIONS ANALYSIS")
    
    # Monthly emissions
    print("\nMONTHLY CARBON EMISSIONS")
    monthly_carbon = df.groupby(['Year', 'Month'])['Carbon_Footprint_kgCO2'].sum().reset_index()
    monthly_carbon['Year-Month'] = monthly_carbon['Year'] + '-' + monthly_carbon['Month']
    print(monthly_carbon)
    
    # Yearly emissions
    print("\nYEARLY CARBON EMISSIONS")
    yearly_carbon = df.groupby('Year')['Carbon_Footprint_kgCO2'].sum().reset_index()
    print(yearly_carbon)
    
    # Statistics
    print("\nEMISSION STATISTICS")
    print("Highest Monthly Emission: {:.2f} kg CO2".format(monthly_carbon['Carbon_Footprint_kgCO2'].max()))
    print("Lowest Monthly Emission: {:.2f} kg CO2".format(monthly_carbon['Carbon_Footprint_kgCO2'].min()))
    print("Average Monthly Emission: {:.2f} kg CO2".format(monthly_carbon['Carbon_Footprint_kgCO2'].mean()))
    
    if len(yearly_carbon) > 1:
        yearly_change = ((yearly_carbon['Carbon_Footprint_kgCO2'].iloc[-1] - 
                         yearly_carbon['Carbon_Footprint_kgCO2'].iloc[0]) / 
                        yearly_carbon['Carbon_Footprint_kgCO2'].iloc[0] * 100)
        print("Year-over-Year Change: {:.2f}%".format(yearly_change))
    
    # Visualizations
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Monthly trend
    axes[0].plot(range(len(monthly_carbon)), monthly_carbon['Carbon_Footprint_kgCO2'], 
                 marker='o', color='darkred', linewidth=2)
    axes[0].set_title('Monthly Carbon Emissions Trend')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('CO2 Emissions (kg)')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xticks(range(len(monthly_carbon)))
    axes[0].set_xticklabels(monthly_carbon['Year-Month'], rotation=45, ha='right')
    
    # Yearly comparison
    axes[1].bar(yearly_carbon['Year'], yearly_carbon['Carbon_Footprint_kgCO2'], 
                color='darkgreen', alpha=0.7)
    axes[1].set_title('Yearly Carbon Emissions Comparison')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('CO2 Emissions (kg)')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

#CHOICE 12 - Outlier Detection
def outlier_detection(): 
    print("YOU CHOSE: OUTLIER DETECTION")
    
    # Calculate IQR for quantity
    Q1_qty = df['Quantity_kg'].quantile(0.25)
    Q3_qty = df['Quantity_kg'].quantile(0.75)
    IQR_qty = Q3_qty - Q1_qty
    lower_bound_qty = Q1_qty - 1.5 * IQR_qty
    upper_bound_qty = Q3_qty + 1.5 * IQR_qty
    
    # Calculate IQR for carbon
    Q1_carbon = df['Carbon_Footprint_kgCO2'].quantile(0.25)
    Q3_carbon = df['Carbon_Footprint_kgCO2'].quantile(0.75)
    IQR_carbon = Q3_carbon - Q1_carbon
    lower_bound_carbon = Q1_carbon - 1.5 * IQR_carbon
    upper_bound_carbon = Q3_carbon + 1.5 * IQR_carbon
    
    # Find outliers
    qty_outliers = df[(df['Quantity_kg'] < lower_bound_qty) | (df['Quantity_kg'] > upper_bound_qty)]
    carbon_outliers = df[(df['Carbon_Footprint_kgCO2'] < lower_bound_carbon) | 
                         (df['Carbon_Footprint_kgCO2'] > upper_bound_carbon)]
    
    print("\nQUANTITY OUTLIERS")
    print("Normal Range: {:.2f} - {:.2f} kg".format(lower_bound_qty, upper_bound_qty))
    print("Number of Outliers: {}".format(len(qty_outliers)))
    if not qty_outliers.empty:
        print("\nOUTLIER RECORDS:")
        print(qty_outliers[['Year', 'Month', 'Location (city)', 'Waste_Type', 
                            'Quantity_kg', 'Carbon_Footprint_kgCO2']])
    
    print("\nCARBON FOOTPRINT OUTLIERS:")
    print("Normal Range: {:.2f} - {:.2f} kg CO2".format(lower_bound_carbon, upper_bound_carbon))
    print("Number of Outliers: {}".format(len(carbon_outliers)))
    if not carbon_outliers.empty:
        print("\nOUTLIER RECORDS:")
        print(carbon_outliers[['Year', 'Month', 'Location (city)', 'Waste_Type', 
                               'Quantity_kg', 'Carbon_Footprint_kgCO2']])
    
    # Statistical analysis by waste type
    print("\nOUTLIER ANALYSIS BY WASTE TYPE")
    for waste_type in df['Waste_Type'].unique():
        type_data = df[df['Waste_Type'] == waste_type]['Quantity_kg']
        if len(type_data) > 3:
            Q1 = type_data.quantile(0.25)
            Q3 = type_data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            type_outliers = df[(df['Waste_Type'] == waste_type) & 
                               ((df['Quantity_kg'] < lower) | (df['Quantity_kg'] > upper))]
            if len(type_outliers) > 0:
                print("\n{}: {} outlier(s)".format(waste_type, len(type_outliers)))
                print("  Normal range: {:.2f} - {:.2f} kg".format(lower, upper))
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Histogram for quantity by waste type
    for waste_type in df['Waste_Type'].unique():
        type_data = df[df['Waste_Type'] == waste_type]['Quantity_kg']
        axes[0, 0].hist(type_data, alpha=0.5, label=waste_type, bins=15)
    axes[0, 0].set_title('Quantity Distribution by Waste Type')
    axes[0, 0].set_xlabel('Quantity (kg)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Histogram for carbon by waste type
    for waste_type in df['Waste_Type'].unique():
        type_data = df[df['Waste_Type'] == waste_type]['Carbon_Footprint_kgCO2']
        axes[0, 1].hist(type_data, alpha=0.5, label=waste_type, bins=15)
    axes[0, 1].set_title('Carbon Footprint Distribution by Waste Type')
    axes[0, 1].set_xlabel('CO2 (kg)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Bar chart for outlier counts by waste type
    outlier_counts = []
    waste_types = []
    for waste_type in df['Waste_Type'].unique():
        type_data = df[df['Waste_Type'] == waste_type]['Quantity_kg']
        if len(type_data) > 3:
            Q1 = type_data.quantile(0.25)
            Q3 = type_data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            type_outliers = df[(df['Waste_Type'] == waste_type) & 
                               ((df['Quantity_kg'] < lower) | (df['Quantity_kg'] > upper))]
            outlier_counts.append(len(type_outliers))
            waste_types.append(waste_type)
    
    axes[1, 0].bar(waste_types, outlier_counts, color='orange', alpha=0.7)
    axes[1, 0].set_title('Number of Outliers by Waste Type')
    axes[1, 0].set_xlabel('Waste Type')
    axes[1, 0].set_ylabel('Number of Outliers')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Histogram with outlier boundaries
    axes[1, 1].hist(df['Quantity_kg'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[1, 1].axvline(lower_bound_qty, color='red', linestyle='--', label=f'Lower Bound: {lower_bound_qty:.2f}')
    axes[1, 1].axvline(upper_bound_qty, color='red', linestyle='--', label=f'Upper Bound: {upper_bound_qty:.2f}')
    axes[1, 1].set_title('Quantity Distribution with Outlier Boundaries')
    axes[1, 1].set_xlabel('Quantity (kg)')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()
    
    # Option to flag or remove outliers
    action = input("Actions: (V)iew outlier details, (F)lag outliers, (R)emove outliers, or (E)xit: ")
    if action.upper() == 'V':
        print("All Outliers:")
        all_outliers = pd.concat([qty_outliers, carbon_outliers]).drop_duplicates()
        print(all_outliers)
    elif action.upper() == 'F':
        print("Note: Implement flagging by adding a column to the DataFrame")
    elif action.upper() == 'R':
        confirm = input("Are you sure you want to remove all outliers? (yes/no): ")
        if confirm.lower() == 'yes':
            all_outliers = pd.concat([qty_outliers, carbon_outliers]).drop_duplicates()
            df.drop(all_outliers.index, inplace=True)
            print("Removed {} outlier records.".format(len(all_outliers)))

#CHOICE 13 - Trend Forecasting (Linear Regression)
def trend_forecasting():
    print("\nYOU CHOSE: TREND FORECASTING")
    data = df.groupby(['Year', 'Month'])['Quantity_kg'].sum().reset_index()
    data['Time'] = np.arange(len(data))
    X = data['Time']
    y = data['Quantity_kg']
    
    # Simple linear regression using NumPy
    a, b = np.polyfit(X, y, 1)
    
    # Predictions
    data['Predicted'] = a * X + b
    
    # Forecast next 6 months
    future_time = np.arange(len(data), len(data) + 6)
    future_pred = a * future_time + b
    future = pd.DataFrame({'Time': future_time, 'Predicted': future_pred})
    
    print("\nForecast for Next 6 Months (approx.):")
    print(future[['Predicted']])
    plt.figure(figsize=(10, 6))
    plt.plot(data['Time'], y, label='Actual Quantity', color='steelblue', linewidth=2)
    plt.plot(future['Time'], future['Predicted'], label='Forecast (Next 6 Months)', color='tomato', linestyle='--', linewidth=2)
    
    plt.title('Waste Generation Over Time', fontsize=14)
    plt.xlabel('Time (Months)', fontsize=12)
    plt.ylabel('Quantity (kg)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

#CHOICE 14 - Historical Comparison (Yearly & Monthly % Change)
def historical_comparison():
    print("\nYOU CHOSE: HISTORICAL COMPARISON")
    yearly = df.groupby('Year')['Quantity_kg'].sum().pct_change()*100
    monthly = df.groupby(['Year','Month'])['Quantity_kg'].sum().pct_change()*100
    print("\nYearly % Change:")
    print(yearly)
    print("\nMonthly % Change:")
    print(monthly)

# CHOICE 15 - Top Contributors (Least Waste)
def top_contributors():
    print("\nYOU CHOSE: TOP CONTRIBUTORS (LEAST WASTE)")
    least_waste = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values().head(5)
    print("\nTop 5 Locations Generating Least Waste:")
    print(least_waste)
    
    # Least hazardous waste by commercial/institutional sources
    subset = df[(df['Waste_Type'] == 'Hazardous') & (df['Waste_Source'].isin(['Commercial Establishment','Institution']))]
    if not subset.empty:
        least_hazard = subset.groupby('Waste_Source')['Quantity_kg'].sum().sort_values().head(5)
        print("\nInstitutions/Commercial Sources Producing Least Hazardous Waste:")
        print(least_hazard)

# CHOICE 16 - Save & Exit
def save_csv():
    df.to_csv("waste.csv", index=False)
    print("Data saved to waste.csv")

# MENU OPTIONS
if username == "admin" and password == "admin123":
    # Example menu loop for admin
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Insert Record")           
        print("2. Update Record")
        print("3. Delete Record")
        print("4. Search Records")
        print("5. Monthly Waste Trends")
        print("6. Waste Type Distribution")
        print("7. Location-Based Waste Analysis")
        print("8. Carbon Footprint Reports")
        print("9. Interactive Search & Filter")
        print("10. Aggregated Statistics")
        print("11. Monthly & Yearly Carbon Emissions")
        print("12. Outlier Detection")
        print("13. Trend Forecasting (Linear Regression)")
        print("14. Historical Comparison (Yearly & Monthly % Change)")
        print("15. Top Contributors (Least Waste)")
        print("16. Save & Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            insert_record()
        elif choice == "2":
            update_record()
        elif choice == "3":
            delete_record()
        elif choice == "4":
            search_record()
        elif choice == "5":
            monthly_trends()
        elif choice == "6":
            waste_type_distribution()
        elif choice == "7":
            location_analysis()
        elif choice == "8":
            carbon_reports()
        elif choice == "9":
            interactive_search_filter()
        elif choice == "10":
            aggregated_statistics()
        elif choice == "11":
            carbon_emissions_analysis()
        elif choice == "12":
            outlier_detection()
        elif choice == "13":
            trend_forecasting()
        elif choice == "14":
            historical_comparison()
        elif choice == "15":
            top_contributors()
        elif choice == "16":
            save_csv()
            break
        else:
            print("Invalid choice. Please try again.")

elif username == "waste collector" and password == "collector123":
    while True:
        print("\n--- WASTE COLLECTOR MENU ---")
        print("1. Insert Record")           
        print("2. Update Record")
        print("3. Delete Record")
        print("4. Search Records")
        print("5. Monthly Waste Trends")
        print("6. Waste Type Distribution")
        print("7. Location-Based Waste Analysis")
        print("8. Carbon Footprint Reports")
        print("X. Save & Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            insert_record()
        elif choice == "2":
            update_record()
        elif choice == "3":
            delete_record()
        elif choice == "4":
            search_record()
        elif choice == "5":
            monthly_trends()
        elif choice == "6":
            waste_type_distribution()
        elif choice == "7":
            location_analysis()
        elif choice == "8":
            carbon_reports()
        elif choice.upper() == "X":
            save_csv()
            break
        else:
            print("Invalid choice. Please try again.")

elif username == "municipal officer" and password == "officer123":
    while True:
        print("\n--- MUNICIPAL OFFICER MENU ---")
        print("1. Search Records")
        print("2. Monthly Waste Trends")
        print("3. Waste Type Distribution")
        print("4. Location-Based Waste Analysis")
        print("5. Carbon Footprint Reports")
        print("X. Save & Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            search_record()
        elif choice == "2":
            monthly_trends()
        elif choice == "3":
            waste_type_distribution()
        elif choice == "4":
            location_analysis()
        elif choice == "5":
            carbon_reports()
        elif choice.upper() == "X":
            save_csv()
            break
        else:
            print("Invalid choice. Please try again.")

elif username == "household/institution" and password == "user123":
    while True:
        print("\n--- HOUSEHOLD/INSTITUTION MENU ---")
        print("1. Search Records")
        print("2. Monthly Waste Trends")
        print("3. Waste Type Distribution")
        print("4. Location-Based Waste Analysis")
        print("5. Carbon Footprint Reports")
        print("X. Save & Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            search_record()
        elif choice == "2":
            monthly_trends()
        elif choice == "3":
            waste_type_distribution()
        elif choice == "4":
            location_analysis()
        elif choice == "5":
            carbon_reports()
        elif choice.upper() == "X":
            save_csv()
            break
        else:
            print("Invalid choice. Please try again.")

else:
    print("Invalid username or password.")