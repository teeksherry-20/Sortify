import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_file = "C:\\Users\\teeks\\OneDrive\\Desktop\\waste.csv"
df = pd.read_csv(csv_file)

# Standardize waste type names
waste_type_mapping = {
    'plastic': 'Plastic',
    'organic': 'Organic',
    'glass': 'Glass',
    'e-waste': 'E-Waste',
    'hazardous waste': 'Hazardous',
    'hazardous': 'Hazardous',
    'paper': 'Paper'
}

df['Waste_Type'] = df['Waste_Type'].str.lower().map(waste_type_mapping).fillna(df['Waste_Type'])

# Emission factors in kg CO2 per kg of waste
emission = { 
    "Plastic": 6.0,
    "Organic": 0.2,
    "Glass": 0.5,
    "E-Waste": 2.5,
    "Hazardous": 4.0,
    "Paper": 1.5
}

# Targets dictionary
targets = {
    'monthly_waste': None,
    'monthly_carbon': None,
    'yearly_waste': None,
    'yearly_carbon': None
}

def calculate_carbon(waste_type, quantity): 
    return quantity * emission.get(waste_type, 0)

def validate_date(year, month, date):
    year_int = int(year)
    month_int = int(month)
    date_int = int(date)
    
    if month_int < 1 or month_int > 12:
        print("❌ Invalid month. Please enter 1-12.")
        return False
    if date_int < 1 or date_int > 31:
        print("❌ Invalid date. Please enter 1-31.")
        return False
    if year_int < 1900 or year_int > 2100:
        print("❌ Invalid year.")
        return False
    return True

def validate_quantity(quantity_str):
    if quantity_str == '':
        return None
    qty = float(quantity_str)
    if qty < 0:
        print("❌ Quantity cannot be negative.")
        return None
    return qty

# 🔐 Login System
print("🌍♻️ WASTE MANAGEMENT SYSTEM LOGIN 🌍♻️")
print("👥 User Roles:")    
print("1️ Admin (username: admin, password: admin123)")
print("2️ Waste Collector (username: waste collector, password: collector123)")
print("3️ Municipal Officer (username: municipal officer, password: officer123)")
print("4️ Household/Institution (username: household/institution, password: user123)")
print("")

username = input("👤 Enter username: ")
password = input("🔑 Enter password: ")

# 📝 CHOICE 1 - Insert Record
def insert_record(df, emission):
    print("")
    print("✨📝 INSERT NEW WASTE RECORD 📝✨")
    
    while True:
        year = input("📅 Enter Year (YYYY): ")
        month = input("📅 Enter Month (MM): ")
        date = input("📅 Enter Date (DD): ")
        
        if validate_date(year, month, date):
            break
    
    location = input("📍 Enter Location (city): ")
    
    print("")
    print("🗑️ Available Waste Types:")
    waste_types = list(emission.keys())
    for idx, wt in enumerate(waste_types, start=1):
        print(f"  {idx}. {wt}")
    waste_type = input("🗑️ Enter Waste Type: ")
    
    print("")
    print("🏭 Waste Sources: Household, Commercial, Industrial, Institution, Municipal")
    waste_source = input("🏭 Enter Waste Source: ")
    
    quantity = None
    while quantity is None:
        qty_input = input("⚖️ Enter Quantity (kg): ")
        quantity = validate_quantity(qty_input)
    
    carbon = calculate_carbon(waste_type, quantity)
    
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
    
    df_new = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    
    print("")
    print("✅ Record inserted successfully!")
    print(f"🌱 Carbon Footprint: {carbon:.2f} kg CO2")
    
    return df_new  # ✅ return updated DataFrame

# 🔄 CHOICE 2 - Update Record
def update_record():
    print("🔄 UPDATE WASTE RECORD")
       
    location = input("📍 Enter Location (city) to search: ")
    waste_type = input("🗑️ Enter Waste Type to search: ")
    
    records = df[(df['Location (city)'].str.contains(location, case=False, na=False)) & 
                 (df['Waste_Type'].str.contains(waste_type, case=False, na=False))]
    
    if records.empty:
        print("❌ No matching records found.")
        return
    
    print("")
    print("🔍 Matching Records:")
    print(records[['Year', 'Month', 'Date', 'Location (city)', 'Waste_Type', 'Quantity_kg', 'Carbon_Footprint_kgCO2']])
    
    index_input = input("🔢 Enter the index of the record to update: ")
    index = int(index_input)
    if index not in df.index:
        print("❌ Invalid index.")
        return
    
    print("")
    print("📋 Columns: Year, Month, Date, Location (city), Waste_Type, Waste_Source, Quantity_kg")
    column = input("✏️ Enter column to update: ")
    
    if column not in df.columns:
        print("❌ Invalid column name.")
        return
    
    if column == "Quantity_kg":
        new_quantity = None
        while new_quantity is None:
            qty_input = input("⚖️ Enter new quantity (kg): ")
            new_quantity = validate_quantity(qty_input)
        
        df.at[index, column] = new_quantity
        waste_type_value = df.at[index, 'Waste_Type']
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(waste_type_value, new_quantity)
        print(f"✅ Quantity updated! 🌱 Carbon footprint recalculated: {df.at[index, 'Carbon_Footprint_kgCO2']:.2f} kg CO2")
    
    elif column == "Waste_Type":
        print("")
        print("🗑️ Available Waste Types:")
        waste_types = list(emission.keys())
        for idx in range(len(waste_types)):
            print(f"  {idx + 1}. {waste_types[idx]}")
        new_waste_type = input("🗑️ Enter new Waste Type: ")
        df.at[index, column] = new_waste_type
        quantity_value = df.at[index, 'Quantity_kg']
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(new_waste_type, quantity_value)
        print(f"✅ Waste type updated! 🌱 Carbon footprint recalculated: {df.at[index, 'Carbon_Footprint_kgCO2']:.2f} kg CO2")
    
    else:
        new_value = input(f"✏️ Enter new value for {column}: ")
        df.at[index, column] = new_value
        print("✅ Record updated successfully!")

# 🗑️ CHOICE 3 - Delete Record
def delete_record():
    print("")
    print("🗑️🚨 DELETE WASTE RECORD 🚨🗑️")
    
    location = input("📍 Enter Location (city) to search: ")
    waste_type = input("🗑️ Enter Waste Type to search: ")
    
    to_delete = df[(df['Location (city)'].str.contains(location, case=False, na=False)) & 
                   (df['Waste_Type'].str.contains(waste_type, case=False, na=False))]
    
    if to_delete.empty:
        print("❌ No matching records found.")
        return
    
    print(f"")
    print(f"🔍 Found {len(to_delete)} matching record(s):")
    print(to_delete)
    
    confirm = input("⚠️ Are you sure you want to delete these records? (yes/no): ").lower()
    if confirm == 'yes':
        df.drop(to_delete.index, inplace=True)
        print(f"✅ {len(to_delete)} record(s) deleted successfully! ✅️ ")
    else:
        print("🚫 Deletion cancelled.")

# 🔍 CHOICE 4 - Search Records
def search_record():
    print("")
    print("🔎 SEARCH WASTE RECORDS 🔎")
    
    result = df.copy()
    
    location = input("📍 Filter by Location (press Enter to skip): ")
    if location:
        result = result[result['Location (city)'].str.contains(location, case=False, na=False)]
    
    waste_type = input("🗑️ Filter by Waste Type (press Enter to skip): ")
    if waste_type:
        result = result[result['Waste_Type'].str.contains(waste_type, case=False, na=False)]
    
    if result.empty:
        print("")
        print("❌ No records found matching your criteria.")
    else:
        print(f"")
        print(f"✅ Found {len(result)} record(s): 🎉")
        print(result)
        
        export = input("💾 Export results to CSV? (y/n): ").lower()
        if export == 'y':
            filename = input("📁 Enter filename (without .csv): ")
            result.to_csv(f"{filename}.csv", index=False)
            print(f"✅ Results exported to {filename}.csv 🎊")

# 📊 CHOICE 5 - Monthly Waste Trends
def monthly_trends(df):
    print("")
    print("📊📈 MONTHLY WASTE TRENDS 📈📊")

    # Make sure Quantity_kg is numeric
    df['Quantity_kg'] = df['Quantity_kg'].astype(float)

    # Group and display the trend
    trend = df.groupby(['Year', 'Month', 'Waste_Type'])['Quantity_kg'].sum()
    print(trend)
    trend_pivot = df.groupby(['Year', 'Month', 'Waste_Type'])['Quantity_kg'].sum().unstack(fill_value=0)

    # Plot
    trend_pivot.plot(kind='bar', stacked=True, figsize=(14, 7), colormap='viridis')
    plt.xlabel('Year-Month')
    plt.ylabel('Quantity (kg)')
    plt.title('Monthly Waste Trends (Stacked by Waste Type)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Waste Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

# 🥧 CHOICE 6 - Waste Type Distribution
def waste_type_distribution():
    print("")
    print("📊 WASTE TYPE DISTRIBUTION 📊")
    
    distribution = df.groupby('Waste_Type')['Quantity_kg'].sum()
    print(distribution)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = plt.cm.Set3(range(len(distribution)))
    ax1.pie(distribution, labels=distribution.index, autopct='%1.1f%%', startangle=140, colors=colors)
    ax1.set_title(' Waste Distribution by Type (Percentage) ', fontsize=14, fontweight='bold')
    
    distribution.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Waste Distribution by Type (Quantity)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Quantity (kg) ', fontsize=12)
    ax2.set_xlabel('Waste Type ', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 🌍 CHOICE 7 - Location-Based Waste Analysis
def location_analysis():
    print("")
    print("🗺️ LOCATION-BASED WASTE ANALYSIS 🗺️")
    
    loc_trend = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values(ascending=False)
    print(loc_trend)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    loc_trend.plot(kind='bar', ax=ax1, color='steelblue', alpha=0.8)
    ax1.set_xlabel('Location', fontsize=12)
    ax1.set_ylabel('Total Waste (kg) ', fontsize=12)
    ax1.set_title(' Total Waste by Location ', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    loc_trend.plot(kind='barh', ax=ax2, color='coral', alpha=0.8)
    ax2.set_xlabel('Total Waste (kg) ', fontsize=12)
    ax2.set_ylabel('Location ', fontsize=12)
    ax2.set_title('Total Waste by Location (Horizontal) ', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 🌱 CHOICE 8 - Carbon Footprint Reports
def carbon_reports():
    print("")
    print("🌱🌿 CARBON FOOTPRINT REPORTS 🌿🌱")
    
    monthly = df.groupby(['Year','Month'])['Carbon_Footprint_kgCO2'].sum()
    print("")
    print("📅 Monthly Carbon Footprint:")
    print(monthly)
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    monthly.plot(kind='line', marker='o', ax=axes[0], color='purple', linewidth=2, markersize=6)
    axes[0].set_title('Monthly Carbon Footprint Trend', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Year-Month', fontsize=12)
    axes[0].set_ylabel('CO2 Emissions (kg)', fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3)
    
    carbon_by_type = df.groupby('Waste_Type')['Carbon_Footprint_kgCO2'].sum().sort_values(ascending=False)
    carbon_by_type.plot(kind='bar', ax=axes[1], color='darkred', alpha=0.7)
    axes[1].set_title('Total Carbon Footprint by Waste Type', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Waste Type', fontsize=12)
    axes[1].set_ylabel('CO2 Emissions (kg)', fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 🔎 CHOICE 9 - Interactive Search and Filter
def interactive_search_filter():
    print("")
    print("🔍 INTERACTIVE SEARCH & FILTER 🔍")
    
    result = df.copy()
    
    print("")
    print("🎯 Apply Filters (press Enter to skip):")
    year = input("📅 Filter by Year (YYYY): ")
    if year:
        result = result[result['Year'] == year]
    
    month = input("📅 Filter by Month (MM): ")
    if month:
        result = result[result['Month'] == month.zfill(2)]
    
    location = input("📍 Filter by Location: ")
    if location:
        result = result[result['Location (city)'].str.contains(location, case=False, na=False)]
    
    waste_type = input("🗑️ Filter by Waste Type: ")
    if waste_type:
        result = result[result['Waste_Type'].str.contains(waste_type, case=False, na=False)]
    
    waste_source = input("🏭 Filter by Waste Source: ")
    if waste_source:
        result = result[result['Waste_Source'].str.contains(waste_source, case=False, na=False)]
    
    min_qty = input("⚖️ Minimum Quantity (kg): ")
    if min_qty:
        result = result[result['Quantity_kg'] >= float(min_qty)]
    
    max_qty = input("⚖️ Maximum Quantity (kg): ")
    if max_qty:
        result = result[result['Quantity_kg'] <= float(max_qty)]
    
    print("")
    print("📑 SORT OPTIONS:")
    print("1 Sort by Quantity (Ascending) ⬆️")
    print("2 Sort by Quantity (Descending) ⬇️")
    print("3 Sort by Carbon Footprint (Ascending) ⬆️")
    print("4 Sort by Carbon Footprint (Descending) ⬇️")
    print("5 Sort by Date (Ascending) ⬆️")
    print("6 Sort by Date (Descending) ⬇️")
    
    sort_choice = input("🎯 Choose sort option (or press Enter to skip): ")
    
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
    
    print("")
    print(f"📋✨ FILTERED RESULTS ({len(result)} records) ✨📋")
    print(result)
    
    export = input("💾 EXPORT RESULTS TO CSV? (y/n): ").lower()
    if export == 'y':
        filename = input("📁 Enter filename (without .csv): ")
        result.to_csv(f"{filename}.csv", index=False)
        print(f"✅ Results exported to {filename}.csv 🎉")

# 📊 CHOICE 10 - Aggregated Statistics
def aggregated_statistics():
    print("")
    print("📊📈 AGGREGATED STATISTICS 📈📊")
    
    print("")
    print("📊 OVERALL STATISTICS 📊")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(f"📁 Total Records: {len(df):,}")
    print(f"🗑️ Total Waste Generated: {df['Quantity_kg'].sum():,.2f} kg")
    print(f"🌱 Total Carbon Footprint: {df['Carbon_Footprint_kgCO2'].sum():,.2f} kg CO2")
    print(f"⚖️ Average Waste per Record: {df['Quantity_kg'].mean():,.2f} kg")
    print(f"💨 Average Carbon per Record: {df['Carbon_Footprint_kgCO2'].mean():,.2f} kg CO2")
    
    print("")
    print("📈 STATISTICS BY WASTE TYPE 🗑️")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    by_type = df.groupby('Waste_Type').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_type)
    
    print("")
    print("🌍 STATISTICS BY LOCATION 📍")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    by_location = df.groupby('Location (city)').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_location)
    
    print("")
    print("🏭 STATISTICS BY WASTE SOURCE 🏢")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    by_source = df.groupby('Waste_Source').agg({
        'Quantity_kg': ['sum', 'mean', 'count'],
        'Carbon_Footprint_kgCO2': ['sum', 'mean']
    }).round(2)
    print(by_source)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    by_type_sum = df.groupby('Waste_Type')['Quantity_kg'].sum()
    by_type_sum.plot(kind='bar', ax=axes[0, 0], color='steelblue', alpha=0.8)
    axes[0, 0].set_title(' Total Waste by Type ', fontsize=13, fontweight='bold')
    axes[0, 0].set_ylabel('Quantity (kg) ', fontsize=11)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    carbon_by_type = df.groupby('Waste_Type')['Carbon_Footprint_kgCO2'].sum()
    carbon_by_type.plot(kind='bar', ax=axes[0, 1], color='coral', alpha=0.8)
    axes[0, 1].set_title('Total Carbon Footprint by Type ', fontsize=13, fontweight='bold')
    axes[0, 1].set_ylabel('CO2 (kg) ', fontsize=11)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    by_location_sum = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values(ascending=True).tail(10)
    by_location_sum.plot(kind='barh', ax=axes[1, 0], color='lightgreen', alpha=0.8)
    axes[1, 0].set_title(' Top 10 Locations by Waste ', fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel('Quantity (kg) ', fontsize=11)
    axes[1, 0].grid(axis='x', alpha=0.3)
    
    by_source_sum = df.groupby('Waste_Source')['Quantity_kg'].sum()
    colors = plt.cm.Pastel1(range(len(by_source_sum)))
    by_source_sum.plot(kind='pie', ax=axes[1, 1], autopct='%1.1f%%', colors=colors)
    axes[1, 1].set_title(' Waste Distribution by Source ', fontsize=13, fontweight='bold')
    axes[1, 1].set_ylabel('')
    
    plt.tight_layout()
    plt.show()

# 🌱 CHOICE 11 - Monthly & Yearly Carbon Emissions
def carbon_emissions_analysis():
    print("")
    print("🌱💨 CARBON EMISSIONS ANALYSIS 💨🌱")
    
    df['Carbon_Footprint_kgCO2'] = df['Carbon_Footprint_kgCO2'].astype(float)
    df['Year'] = df['Year'].astype(str)
    df['Month'] = df['Month'].astype(str)

    # Create Year-Month column
    monthly_carbon = df.groupby(['Year', 'Month'])['Carbon_Footprint_kgCO2'].sum().reset_index()
    monthly_carbon['Year-Month'] = monthly_carbon['Year'] + '-' + monthly_carbon['Month']

    print("")
    print("📅 MONTHLY CARBON EMISSIONS 📊")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(monthly_carbon[['Year-Month', 'Carbon_Footprint_kgCO2']])
    
    yearly_carbon = df.groupby('Year')['Carbon_Footprint_kgCO2'].sum().reset_index()
    print("")
    print("📆 YEARLY CARBON EMISSIONS 📊")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(yearly_carbon)
    
    print("")
    print("📊 EMISSION STATISTICS 💨")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(f"📈 Highest Monthly Emission: {monthly_carbon['Carbon_Footprint_kgCO2'].max():,.2f} kg CO2")
    print(f"📉 Lowest Monthly Emission: {monthly_carbon['Carbon_Footprint_kgCO2'].min():,.2f} kg CO2")
    print(f"📊 Average Monthly Emission: {monthly_carbon['Carbon_Footprint_kgCO2'].mean():,.2f} kg CO2")
    
    if len(yearly_carbon) > 1:
        yearly_change = ((yearly_carbon['Carbon_Footprint_kgCO2'].iloc[-1] - 
                         yearly_carbon['Carbon_Footprint_kgCO2'].iloc[0]) / 
                        yearly_carbon['Carbon_Footprint_kgCO2'].iloc[0] * 100)
        print(f"📈 Year-over-Year Change: {yearly_change:+.2f}%")
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    axes[0].plot(range(len(monthly_carbon)), monthly_carbon['Carbon_Footprint_kgCO2'], 
                 marker='o', color='darkred', linewidth=2, markersize=6)
    axes[0].set_title(' Monthly Carbon Emissions Trend ', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Month ', fontsize=12)
    axes[0].set_ylabel('CO2 Emissions (kg) ', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xticks(range(len(monthly_carbon)))
    axes[0].set_xticklabels(monthly_carbon['Year-Month'], rotation=45, ha='right')
    
    axes[1].bar(yearly_carbon['Year'], yearly_carbon['Carbon_Footprint_kgCO2'], 
                color='darkgreen', alpha=0.7, edgecolor='black')
    axes[1].set_title(' Yearly Carbon Emissions Comparison ', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Year ', fontsize=12)
    axes[1].set_ylabel('CO2 Emissions (kg) ', fontsize=12)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

# ⚠️ CHOICE 12 - Outlier Detection
def outlier_detection(df):
    print("")
    print("🔍⚠️ OUTLIER DETECTION ⚠️🔍")

    # IQR-based bounds
    Q1_qty = df['Quantity_kg'].quantile(0.25)
    Q3_qty = df['Quantity_kg'].quantile(0.75)
    IQR_qty = Q3_qty - Q1_qty
    lower_bound_qty = Q1_qty - 1.5 * IQR_qty
    upper_bound_qty = Q3_qty + 1.5 * IQR_qty

    qty_outliers = df[(df['Quantity_kg'] < lower_bound_qty) | (df['Quantity_kg'] > upper_bound_qty)]

    # Print summary
    print(f"\n⚖️ Quantity Normal Range: {lower_bound_qty:.2f} - {upper_bound_qty:.2f} kg")
    print(f"🔢 Number of Outliers: {len(qty_outliers)}")
    if not qty_outliers.empty:
        print("📋 Outlier Records:")
        print(qty_outliers[['Year', 'Month', 'Location (city)', 'Waste_Type', 'Quantity_kg', 'Carbon_Footprint_kgCO2']])

    # Single histogram
    plt.figure(figsize=(12,6))
    plt.hist(df['Quantity_kg'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(lower_bound_qty, color='red', linestyle='--', linewidth=2, label=f'⚠️ Lower: {lower_bound_qty:.0f}')
    plt.axvline(upper_bound_qty, color='red', linestyle='--', linewidth=2, label=f'⚠️ Upper: {upper_bound_qty:.0f}')
    plt.title('⚖️ Quantity Distribution with Outlier Boundaries', fontsize=14, fontweight='bold')
    plt.xlabel('Quantity (kg) ⚖️')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# 🔮 CHOICE 13 - Trend Forecasting
def trend_forecasting():
    print("")
    print("🔮📈 TREND FORECASTING (LINEAR REGRESSION) 📈🔮")
    
    data = df.groupby(['Year', 'Month'])['Quantity_kg'].sum().reset_index()
    data['Time'] = np.arange(len(data))
    X = data['Time']
    y = data['Quantity_kg']
    
    a, b = np.polyfit(X, y, 1)
    data['Predicted'] = a * X + b
    
    future_time = np.arange(len(data), len(data) + 6)
    future_pred = a * future_time + b
    future = pd.DataFrame({'Time': future_time, 'Predicted': future_pred})
    
    print("")
    print("🔮 FORECAST FOR NEXT 6 MONTHS 📅")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    for i in range(len(future)):
        print(f"📅 Month {i + 1}: {future['Predicted'].iloc[i]:,.2f} kg")
    
    trend_direction = '📈 Increasing' if a > 0 else '📉 Decreasing'
    print(f"")
    print(f"📊 Trend: {trend_direction} ({abs(a):.2f} kg/month)")
    
    plt.figure(figsize=(14, 7))
    plt.plot(data['Time'], y, label='Actual Quantity', color='steelblue', linewidth=2.5, marker='o', markersize=5)
    plt.plot(data['Time'], data['Predicted'], label='Fitted Trend', color='orange', linewidth=2, linestyle='--')
    plt.plot(future['Time'], future['Predicted'], label='Forecast (Next 6 Months)', color='red', linestyle='--', linewidth=2.5, marker='s')
    
    plt.title('Waste Generation Forecast', fontsize=16, fontweight='bold')
    plt.xlabel('Time (Months)', fontsize=13)
    plt.ylabel('Quantity (kg) ', fontsize=13)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# 📊 CHOICE 14 - Historical Comparison
def historical_comparison():
    print("")
    print("📈 HISTORICAL COMPARISON 📈")
    
    yearly = df.groupby('Year')['Quantity_kg'].sum().pct_change()*100
    monthly = df.groupby(['Year','Month'])['Quantity_kg'].sum().pct_change()*100
    
    print("")
    print("📊 YEARLY PERCENTAGE CHANGE 📈")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(yearly)
    
    print("")
    print("📅 MONTHLY PERCENTAGE CHANGE (Last 12 Months) 📊")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(monthly.tail(12))

# 🏆 CHOICE 15 - Top Contributors
def top_contributors():
    print("")
    print("🌟🏆 TOP CONTRIBUTORS (LEAST WASTE) 🏆🌟")
    
    least_waste = df.groupby('Location (city)')['Quantity_kg'].sum().sort_values().head(5)
    print("")
    print("🏆 TOP 5 LOCATIONS GENERATING LEAST WASTE 🌟")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    print(least_waste)
    
    subset = df[(df['Waste_Type'] == 'Hazardous') & 
                (df['Waste_Source'].str.contains('Commercial|Institution', case=False, na=False))]
    if not subset.empty:
        least_hazard = subset.groupby('Waste_Source')['Quantity_kg'].sum().sort_values().head(5)
        print("")
        print("🏭 INSTITUTIONS/COMMERCIAL WITH LEAST HAZARDOUS WASTE ⚠️")
        print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
        print(least_hazard)

# 🎯 CHOICE 16 - Set Waste Reduction Targets
def set_targets():
    print("")
    print("🎯 SET WASTE REDUCTION TARGETS 🎯")
    
    print("")
    print("📊 CURRENT STATISTICS 📊")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    current_monthly = df.groupby(['Year', 'Month'])['Quantity_kg'].sum().mean()
    current_yearly = df.groupby('Year')['Quantity_kg'].sum().mean()
    current_monthly_carbon = df.groupby(['Year', 'Month'])['Carbon_Footprint_kgCO2'].sum().mean()
    current_yearly_carbon = df.groupby('Year')['Carbon_Footprint_kgCO2'].sum().mean()
    
    print(f"⚖️ Current Avg Monthly Waste: {current_monthly:,.2f} kg")
    print(f"⚖️ Current Avg Yearly Waste: {current_yearly:,.2f} kg")
    print(f"💨 Current Avg Monthly Carbon: {current_monthly_carbon:,.2f} kg CO2")
    print(f"💨 Current Avg Yearly Carbon: {current_yearly_carbon:,.2f} kg CO2")
    
    print("")
    print("🎯 SET YOUR TARGETS 🎯")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    
    target_monthly_input = input(f"🎯 Target Monthly Waste (kg) [{current_monthly*0.9:.0f}]: ")
    targets['monthly_waste'] = float(target_monthly_input or current_monthly*0.9)
    
    target_yearly_input = input(f"🎯 Target Yearly Waste (kg) [{current_yearly*0.9:.0f}]: ")
    targets['yearly_waste'] = float(target_yearly_input or current_yearly*0.9)
    
    target_monthly_carbon_input = input(f"🎯 Target Monthly Carbon (kg CO2) [{current_monthly_carbon*0.9:.0f}]: ")
    targets['monthly_carbon'] = float(target_monthly_carbon_input or current_monthly_carbon*0.9)
    
    target_yearly_carbon_input = input(f"🎯 Target Yearly Carbon (kg CO2) [{current_yearly_carbon*0.9:.0f}]: ")
    targets['yearly_carbon'] = float(target_yearly_carbon_input or current_yearly_carbon*0.9)
    
    print("")
    print("✅ Targets set successfully! 🎉")
    print("")
    print("🎯 YOUR TARGETS:")
    print(f"  📅 Monthly Waste: {targets['monthly_waste']:,.2f} kg")
    print(f"  📆 Yearly Waste: {targets['yearly_waste']:,.2f} kg")
    print(f"  📅 Monthly Carbon: {targets['monthly_carbon']:,.2f} kg CO2")
    print(f"  📆 Yearly Carbon: {targets['yearly_carbon']:,.2f} kg CO2")

# 📊 CHOICE 17 - Compare Against Targets
def compare_targets():
    print("")
    print("📊🎯 TARGET COMPARISON REPORT 🎯📊")
    
    if not any(targets.values()):
        print("")
        print("⚠️ No targets have been set yet.")
        print("⚠️ Please set targets first (Option 16).")
        return
    
    current_monthly = df.groupby(['Year', 'Month'])['Quantity_kg'].sum().mean()
    current_yearly = df.groupby('Year')['Quantity_kg'].sum().mean()
    current_monthly_carbon = df.groupby(['Year', 'Month'])['Carbon_Footprint_kgCO2'].sum().mean()
    current_yearly_carbon = df.groupby('Year')['Carbon_Footprint_kgCO2'].sum().mean()
    
    print("")
    print("📊 PERFORMANCE VS TARGETS 🎯")
    print("⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤")
    
    if targets['monthly_waste']:
        diff = current_monthly - targets['monthly_waste']
        status = "✅ Meeting Target 🎉" if current_monthly <= targets['monthly_waste'] else "❌ Above Target ⚠️"
        print(f"")
        print(f"📅 Monthly Waste:")
        print(f"  📊 Current: {current_monthly:,.2f} kg")
        print(f"  🎯 Target: {targets['monthly_waste']:,.2f} kg")
        print(f"  📈 Difference: {diff:+,.2f} kg ({(diff/targets['monthly_waste']*100):+.1f}%)")
        print(f"  {status}")
    
    if targets['yearly_waste']:
        diff = current_yearly - targets['yearly_waste']
        status = "✅ Meeting Target 🎉" if current_yearly <= targets['yearly_waste'] else "❌ Above Target ⚠️"
        print(f"")
        print(f"📆 Yearly Waste:")
        print(f"  📊 Current: {current_yearly:,.2f} kg")
        print(f"  🎯 Target: {targets['yearly_waste']:,.2f} kg")
        print(f"  📈 Difference: {diff:+,.2f} kg ({(diff/targets['yearly_waste']*100):+.1f}%)")
        print(f"  {status}")
    
    if targets['monthly_carbon']:
        diff = current_monthly_carbon - targets['monthly_carbon']
        status = "✅ Meeting Target 🎉" if current_monthly_carbon <= targets['monthly_carbon'] else "❌ Above Target ⚠️"
        print(f"")
        print(f"📅 Monthly Carbon:")
        print(f"  💨 Current: {current_monthly_carbon:,.2f} kg CO2")
        print(f"  🎯 Target: {targets['monthly_carbon']:,.2f} kg CO2")
        print(f"  📈 Difference: {diff:+,.2f} kg CO2 ({(diff/targets['monthly_carbon']*100):+.1f}%)")
        print(f"  {status}")
    
    if targets['yearly_carbon']:
        diff = current_yearly_carbon - targets['yearly_carbon']
        status = "✅ Meeting Target 🎉" if current_yearly_carbon <= targets['yearly_carbon'] else "❌ Above Target ⚠️"
        print(f"")
        print(f"📆 Yearly Carbon:")
        print(f"  💨 Current: {current_yearly_carbon:,.2f} kg CO2")
        print(f"  🎯 Target: {targets['yearly_carbon']:,.2f} kg CO2")
        print(f"  📈 Difference: {diff:+,.2f} kg CO2 ({(diff/targets['yearly_carbon']*100):+.1f}%)")
        print(f"  {status}")
    
    if any(targets.values()):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        if targets['monthly_waste']:
            categories = ['Current', 'Target']
            values = [current_monthly, targets['monthly_waste']]
            colors = ['red' if current_monthly > targets['monthly_waste'] else 'green', 'blue']
            axes[0, 0].bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
            axes[0, 0].set_title(' Monthly Waste: Current vs Target ', fontweight='bold')
            axes[0, 0].set_ylabel('Quantity (kg) ')
            axes[0, 0].grid(axis='y', alpha=0.3)
        
        if targets['yearly_waste']:
            categories = ['Current', 'Target']
            values = [current_yearly, targets['yearly_waste']]
            colors = ['red' if current_yearly > targets['yearly_waste'] else 'green', 'blue']
            axes[0, 1].bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
            axes[0, 1].set_title(' Yearly Waste: Current vs Target ', fontweight='bold')
            axes[0, 1].set_ylabel('Quantity (kg) ')
            axes[0, 1].grid(axis='y', alpha=0.3)
        
        if targets['monthly_carbon']:
            categories = ['Current', 'Target']
            values = [current_monthly_carbon, targets['monthly_carbon']]
            colors = ['red' if current_monthly_carbon > targets['monthly_carbon'] else 'green', 'blue']
            axes[1, 0].bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
            axes[1, 0].set_title(' Monthly Carbon: Current vs Target ', fontweight='bold')
            axes[1, 0].set_ylabel('CO2 (kg) ')
            axes[1, 0].grid(axis='y', alpha=0.3)
        
        if targets['yearly_carbon']:
            categories = ['Current', 'Target']
            values = [current_yearly_carbon, targets['yearly_carbon']]
            colors = ['red' if current_yearly_carbon > targets['yearly_carbon'] else 'green', 'blue']
            axes[1, 1].bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
            axes[1, 1].set_title(' Yearly Carbon: Current vs Target ', fontweight='bold')
            axes[1, 1].set_ylabel('CO2 (kg) ')
            axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# 💾 CHOICE 18 - Save & Exit
def save_csv():
    df.to_csv(csv_file, index=False)
    print("")
    print("✅ Data saved successfully to waste.csv 🎉")

# 🎮 MENU OPTIONS
if username == "admin" and password == "admin123":
    while True:
        print("")
        print("👑 ADMIN MENU 👑")
        print("1 Insert New Record 📝")
        print("2 Update Existing Record 🔄")
        print("3 Delete Record 🗑️")   
        print("4 Search Records 🔍")
        print("5 Waste Trend Analysis 📊")
        print("6 Waste Type Distribution 🥧")
        print("7 Location-Based Waste Analysis 🌍")
        print("8 Carbon Footprint Reports 🌱")
        print("9 Interactive Search & Filter 🔎")
        print("10 Aggregated Statistics 📈")
        print("11 Monthly & Yearly Carbon Emissions 💨")
        print("12 Outlier Detection ⚠️")
        print("13 Trend Forecasting 🔮")
        print("14 Historical Comparison 📊")
        print("15 Top Contributors 🏆")
        print("16 Set Waste Reduction Targets 🎯")
        print("17 Compare Against Targets 📊")
        print("18 Save & Exit 💾")
        choice = input("🎯 Choose an option (1-18): ")
        if choice == "1":
            df = insert_record(df, emission)
        elif choice == "2":
            update_record()
        elif choice == "3":
            delete_record()
        elif choice == "4":
            search_record()
        elif choice == "5":
            monthly_trends(df)
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
            outlier_detection(df)
        elif choice == "13":
            trend_forecasting()
        elif choice == "14":
            historical_comparison()
        elif choice == "15":
            top_contributors()
        elif choice == "16":
            set_targets()
        elif choice == "17":
            compare_targets()
        elif choice == "18":
            save_csv()
            print("👋 Exiting SORTIFY... Goodbye! 🌍")
            break
        else:
            print("❌ Invalid option. Please choose a number between 1 and 18. 🔢")

elif username == "household/institution" and password == "user123":
    while True:
        print("")
        print("🏠 USER MENU 🏠")
        print("1 Waste Trend Analysis 📊")
        print("2 Waste Type Distribution 🥧")
        print("3 Carbon Footprint Reports 🌱")
        print("4 Interactive Search & Filter 🔎")
        print("5 Aggregated Statistics 📈")
        print("6 Monthly & Yearly Carbon Emissions 💨")
        print("7 Top Contributors 🏆")
        print("8 Set Waste Reduction Targets 🎯")
        print("9 Compare Against Targets 📊")
        print("10 Save & Exit 💾")
        choice = input("🎯 Choose an option (1-10): ")
        if choice == "1":
            monthly_trends(df)
        elif choice == "2":
            waste_type_distribution()
        elif choice == "3":
            carbon_reports()
        elif choice == "4":
            interactive_search_filter()
        elif choice == "5":
            aggregated_statistics()
        elif choice == "6":
            carbon_emissions_analysis()
        elif choice == "7":
            top_contributors()
        elif choice == "8":
            set_targets()
        elif choice == "9":
            compare_targets()
        elif choice == "10":
            save_csv()
            print("👋 Exiting SORTIFY... Goodbye! 🌍")
            break
        else:
            print("❌ Invalid option. Please choose a number between 1 and 10. 🔢")

elif username == "municipal officer" and password == "officer123":
    while True:
        print("")
        print("🏛️ MUNICIPAL OFFICER MENU 🏛️")
        print("1 Waste Trend Analysis 📊")
        print("2 Waste Type Distribution 🥧")
        print("3 Location-Based Waste Analysis 🌍")
        print("4 Carbon Footprint Reports 🌱")
        print("5 Interactive Search & Filter 🔎")
        print("6 Aggregated Statistics 📈")
        print("7 Monthly & Yearly Carbon Emissions 💨")
        print("8 Outlier Detection ⚠️")
        print("9 Trend Forecasting 🔮")
        print("10 Historical Comparison 📊")
        print("11 Top Contributors 🏆")
        print("12 Set Waste Reduction Targets 🎯")
        print("13 Compare Against Targets 📊")
        print("14 Save & Exit 💾")
        choice = input("🎯 Choose an option (1-14): ")
        if choice == "1":
            monthly_trends(df)
        elif choice == "2":
            waste_type_distribution()
        elif choice == "3":
            location_analysis()
        elif choice == "4":
            carbon_reports()
        elif choice == "5":
            interactive_search_filter()
        elif choice == "6":
            aggregated_statistics()
        elif choice == "7":
            carbon_emissions_analysis()
        elif choice == "8":
            outlier_detection(df)
        elif choice == "9":
            trend_forecasting()
        elif choice == "10":
            historical_comparison()
        elif choice == "11":
            top_contributors()
        elif choice == "12":
            set_targets()
        elif choice == "13":
            compare_targets()
        elif choice == "14":
            save_csv()
            print("👋 Exiting SORTIFY... Goodbye! 🌍")
            break
        else:
            print("❌ Invalid option. Please choose a number between 1 and 14. 🔢")

elif username == "waste collector" and password == "collector123":
    while True:
        print("")
        print("🚛 WASTE COLLECTOR MENU 🚛")
        print("1 Insert New Record 📝")
        print("2 Update Existing Record 🔄")
        print("3 Delete Record 🗑️")   
        print("4 Search Records 🔍")
        print("5 Waste Trend Analysis 📊")
        print("6 Waste Type Distribution 🥧")
        print("7 Location-Based Waste Analysis 🌍")
        print("8 Carbon Footprint Reports 🌱")
        print("9 Interactive Search & Filter 🔎")
        print("10 Save & Exit 💾")
        choice = input("🎯 Choose an option (1-10): ")
        if choice == "1":
            insert_record(df, emission)
        elif choice == "2":
            update_record()
        elif choice == "3":
            delete_record()
        elif choice == "4":
            search_record()
        elif choice == "5":
            monthly_trends(df)
        elif choice == "6":
            waste_type_distribution()
        elif choice == "7":
            location_analysis()
        elif choice == "8":
            carbon_reports()
        elif choice == "9":
            interactive_search_filter()
        elif choice == "10":
            save_csv()
            print("👋 Exiting SOTIFY... Goodbye! 🌍")
            break
        else:
            print("❌ Invalid option. Please choose a number between 1 and 10. 🔢")

else: 
    print("❌ Invalid credentials. Access denied. 🚫")
