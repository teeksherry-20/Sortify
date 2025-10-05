import pandas as pd 
df = pd.read_csv("waste.csv")
# Emission factors in kg CO2 per kg of waste
emission = { 
    "Plastic": 6.0,
    "Organic": 0.2,
    "Glass": 0.5,
    "E-Waste": 2.5,
    "Hazardous": 4.0,
    "Paper": 1.5
}

# Function to calculate carbon footprint
def calculate_carbon(waste_type, quantity): 
    return quantity * emission.get(waste_type, 0)

# CHOICE 1 - Insert Record
def insert_record():
    print("\nInsert New Record")
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

# CHOICE 2 - Update Record
def update_record():
    print("\n--- Update Record ---")
    location = input("Enter Location (city) to search: ")
    waste_type = input("Enter Waste Type to search: ")
    
    # Find matching records
    records = df[(df['Location (city)'] == location) & (df['Waste_Type'] == waste_type)]
    if records.empty:
        print("No matching record found.")
        return
    print("\nMatching Records:")
    print(records)
    
    # Get index of record to update
    index = int(input("Enter the index of the record to update: "))
    column = input("Enter column to update: ")
    
    # Update the specified column
    if column == "Quantity_kg":
        new_quantity = float(input("Enter new quantity (kg): "))

        # Update quantity and recalculate carbon footprint
        df.at[index, column] = new_quantity
        waste_type_value = df.at[index, 'Waste_Type']
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(waste_type_value, new_quantity)
        print(f"Quantity updated! Carbon footprint recalculated: {df.at[index, 'Carbon_Footprint_kgCO2']} kg CO2")

        # If quantity is updated, also update carbon footprint
    elif column == "Waste_Type":
        new_waste_type = input("Enter new Waste Type: ")

        # Update waste type and recalculate carbon footprint
        df.at[index, column] = new_waste_type
        quantity_value = df.at[index, 'Quantity_kg']
        df.at[index, 'Carbon_Footprint_kgCO2'] = calculate_carbon(new_waste_type, quantity_value)
        print(f"Waste type updated! Carbon footprint recalculated: {df.at[index, 'Carbon_Footprint_kgCO2']} kg CO2")

        # If waste type is updated, also update carbon footprint
    else:
        # Update other columns directly
        new_value = input("Enter new value: ")
        df.at[index, column] = new_value
        print("Record updated successfully!")

# CHOICE 3 - Delete Record
def delete_record():
    print("\nDelete Record")
    location = input("Enter Location (city) to search: ")
    waste_type = input("Enter Waste Type to search: ")
    
    # Find matching records
    df.drop(df[(df['Location (city)'] == location) & (df['Waste_Type'] == waste_type)].index, inplace=True)
    print("Record(s) deleted successfully!")

# CHOICE 4 - Search Records
def search_record():
    print("\nSearch Records")
    location = input("Enter Location (city) to search (leave blank for all): ")
    waste_type = input("Enter Waste Type to search (leave blank for all): ")
    
    # Filter records based on input
    result = df
    if location:
        result = result[result['Location (city)'] == location]
    if waste_type:
        result = result[result['Waste_Type'] == waste_type]
    
    print("\nSearch Results:")
    print(result)

# CHOICE 5 - Monthly Waste Trends
def monthly_trends():
    print("\nMonthly Waste Trends")
    trend = df.groupby(['Year', 'Month', 'Waste_Type'])['Quantity_kg'].sum()
    print(trend)

    # Plotting the trends
    import matplotlib.pyplot as plt
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
    print("\n Waste Type Distribution")
    
    distribution = df.groupby('Waste_Type')['Quantity_kg'].sum()
    print(distribution)
    plt.figure(figsize=(8, 8))
    plt.pie(distribution, labels=distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title('Overall Waste Distribution by Type')
    plt.tight_layout()
    plt.show()

# CHOICE 7 - Location-Based Waste Analysis
def location_analysis():
    print("\nLocation-Based Waste Analysis")
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
    print("\nCarbon Footprint Reports")
    monthly = df.groupby(['Year','Month'])['Carbon_Footprint_kgCO2'].sum()
    print("\nMonthly Carbon Footprint:")
    print(monthly)
    monthly.plot(kind='line', marker='o', figsize=(10,5), color='purple', title='Monthly Carbon Footprint')
    plt.xlabel('Year-Month')
    plt.ylabel('CO2 Emissions (kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# CHOICE X - Save & Exit
def save_csv():
    df.to_csv("waste.csv", index=False)
    print("Data saved to waste.csv")

# Main Menu Loop
while True:
    print("Waste Management Menu")
    print("1. Insert Record")
    print("2. Update Record")
    print("3. Delete Record")
    print("4. Search Records")
    print("5. Monthly Waste Trends")
    print("6. Waste Type Distribution Charts")
    print("7. Location-Based Waste Analysis")
    print("8. Carbon Footprint Reports")
    print("X. Save & Exit")
    
    c = input("ENTER CHOICE: ")
    if c == "1":
        insert_record()
    elif c == "2":
        update_record()
    elif c == "3":
        delete_record()
    elif c == "4":
        search_record()
    elif c == "5":
        monthly_trends()
    elif c == "6":
        waste_type_distribution()
    elif c == "7":
        location_analysis()
    elif c == "8":
        carbon_reports()
    elif c == "X":
        save_csv()
    else:
        print("INVALID!") 