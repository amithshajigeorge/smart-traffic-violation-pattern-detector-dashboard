import random

# ====================================================================================
# General Data Definations
# ====================================================================================
TRAFFIC_VIOLATION_COLUMNS = [
    'Violation_ID', 'Violation_Type', 'Fine_Amount', 'Location', 'Date', 'Time', 
    'Vehicle_Type', 'Vehicle_Color', 'Vehicle_Model_Year', 'Registration_State', 
    'Driver_Age', 'Driver_Gender', 'License_Type', 'Penalty_Points', 
    'Weather_Condition', 'Road_Condition', 'Officer_ID', 'Issuing_Agency', 
    'License_Validity', 'Number_of_Passengers', 'Helmet_Worn', 'Seatbelt_Worn', 
    'Traffic_Light_Status', 'Speed_Limit', 'Recorded_Speed', 'Alcohol_Level', 
    'Breathalyzer_Result', 'Towed', 'Fine_Paid', 'Payment_Method', 
    'Court_Appearance_Required', 'Previous_Violations', 'Comments'
]

# ====================================================================================
# Dataset Generartor Data Definations
# ====================================================================================

# -------------------- POSSIBLE CATEGORY CHOICES --------------------
violation_types_list = [
    "Overspeeding", "Overspeeding", "Overspeeding", "Overspeeding", 
    "Drunk Driving", 
    "Wrong Lane", 
    "Red Light Violation", "Red Light Violation", 
    "No Parking", "No Parking", 
    "Mobile Phone Usage", "Mobile Phone Usage","Mobile Phone Usage",
    "Overloading", 
    "Illegal U Turn", 
    "Driving Without License", "Driving Without License","Driving Without License",
    # "Hit and Run"
]

vehicle_types_mapping = {
    "Overspeeding": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Scooty"]),
    "Drunk Driving": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw","Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Wrong Lane": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Red Light Violation": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "No Parking": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Hit and Run": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Mobile Phone Usage": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Illegal U Turn": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Driving Without License": random.choice(["Car", "Motorcycle", "Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Electric Scooter", "Tractor", "E-Rickshaw", "Scooty"]),
    "Overloading": random.choice(["Truck", "Bus", "Auto-Rickshaw", "Van", "Pickup", "Tractor", "E-Rickshaw"])
}

# -------------------- VEHICLE SAFETY MAPPING -----------------------

seatbelt_worn_mapping = {
    "Car": random.choice(['Yes', 'No']),
    "Motorcycle": 'NA',
    "Truck": random.choice(['Yes', 'No']),
    "Bus": random.choice(['Yes', 'No']),
    "Auto-Rickshaw": 'NA',
    "Bicycle": 'NA',
    "Van": random.choice(['Yes', 'No']),  
    "Pickup": random.choice(['Yes', 'No']),
    "Electric Scooter": 'NA',
    "Tractor": 'NA',         
    "E-Rickshaw": 'NA',
    "Scooty": 'NA'
}

helmet_worn_mapping = {
    "Car" : "NA",
    "Motorcycle" : random.choice(["Yes", "No"]),
    "Truck" : "NA",
    "Bus" : "NA",
    "Auto-Rickshaw" : "NA",
    "Bicycle" : random.choice(["Yes", "No"]),
    "Van" : "NA",
    "Pickup" : "NA",
    "Electric Scooter" : random.choice(["Yes", "No"]),
    "Tractor" : "NA",
    "E-Rickshaw" : "NA",
    "Scooty" : random.choice(["Yes", "No"])
}

# ------------------------- VEHICLE TYPES ---------------------------
vehicle_types_list = [
    "Car", "Car", "Car", "Car", "Car", 
    "Motorcycle", "Motorcycle", "Motorcycle", "Motorcycle", 
    "Scooty", "Scooty", "Scooty"
    "Truck", "Truck", "Truck", "Truck", "Truck", "Truck",
    "Bus", 
    "Auto-Rickshaw", 
    "Bicycle", 
    "Van", 
    "Pickup", 
    "Electric Scooter", 
    "Tractor", 
    "E-Rickshaw", 
]

# ----------------------------- FINE MAP -----------------------------
fine_mapping = {
    "Overspeeding": random.randint(1000, 4000),
    "Drunk Driving": random.randint(1000, 1500),
    "Wrong Lane": random.randint(500, 5000),
    "Red Light Violation": random.randint(1000, 5000),
    "No Parking": random.randint(500, 1500),
    "Seatbelt Violation": random.randint(1000, 5000),
    "Helmet Violation": random.randint(1000, 5000),
    "Mobile Phone Usage": random.randint(1000, 5000),
    "Overloading": random.randint(1000, 5000),
    "Illegal U Turn": random.randint(500, 1000),
    "Driving Without License": random.randint(1000, 5000),
    # "Hit and Run": random.choice([100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]),
}

# --------------- VEHICLE SAFETY MAPPING -----------
vehicle_colors_list = [
    "White", "Black", "Silver",
    "Blue", "Red", "Grey", "Green", 
    "Yellow", "Brown", "Orange", "Other"
]

# -------------------- DRIVER'S INFORMATIONS --------------------
driver_genders_list = [
    "Male", "Male", "Male", "Female", "Other"
]

no_of_passengers_mapping = {
    # It will based on vehicle type
    "Car": random.randint(0, 4),
    "Motorcycle": random.randint(0, 2),
    "Truck": random.randint(0, 3),
    "Bus": random.randint(0, 50),
    "Auto-Rickshaw": random.randint(0, 3),
    "Bicycle": random.randint(0, 1),
    "Van": random.randint(0, 8),
    "Pickup": random.randint(0, 5),
    "Electric Scooter": random.randint(0, 2),
    "Tractor": random.randint(0, 1),
    "E-Rickshaw": random.randint(0, 4),
    "Scooty": random.randint(0, 2)
}

license_types_list = [
    "Learner", 
    "Permanent", "Permanent", "Permanent","Permanent", 
    "Commercial", "Commercial",
]
issuing_agencies_list = [
    "City Traffic Police", "Highway Patrol", "RTO Enforcement", "Special Task Force"
]
license_validity_list = [
    "Valid", "Valid", "Valid", "Valid", "Valid", 
    "Expired", "Expired", "Expired", 
    "Suspended", 
    "Cancelled"
]

# -------------------- DRIVER'S CONDITIONS ------------------------
breathalyzer_results_list = [
    "Positive", 
    "Negative", "Negative", "Negative", "Negative", 
    "Not Applied", "Not Applied", "Not Applied", "Not Applied", "Not Applied"
]

alcohol_levels_mapping = {    
    "Positive": round(random.uniform(0.08, 0.40), 2), # Legal limit is often 0.08% in many places
    "Negative": round(random.uniform(0.00, 0.07), 2),
    "Not Applied": 0.00
}

# -------------------- Environament CONDITIONS --------------------
weather_conditions_list = [
    "Clear", "Clear", "Clear", "Clear", "Clear", 
    "Rainy", "Rainy", "Rainy", 
    "Windy", "Windy", "Windy",
    "Foggy", "Foggy", 
    "Snowy", 
]
road_conditions_list = ["Dry", "Wet", "Under Construction", "Gravel", "Potholes"]

# -------------------- Locations --------------------
# Increased occurrence of some states to raise their selection probability.
# Adjust the repetition counts in the list below to tune probabilities.
states_list = [
    # High-probability (duplicated) states
    "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh",
    "Maharashtra", "Maharashtra", "Maharashtra", "Maharashtra", "Maharashtra", 
    "West Bengal", "West Bengal", "West Bengal", "West Bengal", 
    "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", 
    "Karnataka", "Karnataka", "Karnataka", "Karnataka", 
    "Delhi", "Delhi", "Delhi", "Delhi", "Delhi",
    "Bihar", "Bihar", "Bihar", "Bihar", 
    
    # Medium-probability (duplicated a bit)
    "Andhra Pradesh", "Andhra Pradesh", "Andhra Pradesh", 
    "Telangana", "Telangana", "Telangana",     
    "Gujarat", "Gujarat", "Gujarat", 
    "Rajasthan", "Rajasthan", "Rajasthan", 
    "Madhya Pradesh", "Madhya Pradesh", "Madhya Pradesh", 
        

    # Single occurrence (low/normal probability)
    "Arunachal Pradesh", "Assam", "Chhattisgarh", "Goa", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Kerala", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Sikkim", "Tripura",
    "Uttarakhand", "Andaman & Nicobar", "Chandigarh", "Dadra & Nagar Haveli",
    "Daman & Diu", "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]


# ========================= Date Filteration =========================
payment_methods_mapping  = {
    'Yes' : random.choice([
        'Cash', 'Cash', 'Cash', 'Cash'
        'UPI', 'UPI', 'UPI',
        'Online',
        'Card', 
    ]),
    'No' : 'Pending'
}


# -------------------------- ACTION TAKEN --------------------------
towing_mapping = {
    # High Possibilities
    "No Parking": random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "No"]), # 70% -> Yes, 30% -> No
    "Hit and Run": random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "No"]), # 70% -> Yes, 30% -> No
    "Drunk Driving": random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "No"]), # 70% -> Yes, 30% -> No
    "Overloading": random.choice(["Yes", "No"]), # 50% -> Yes, 50% -> No
    "Driving Without License": random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "No", "No"]), # 60% -> Yes, 40% -> No

    # Low Possibilities
    "Wrong Lane": "No",
    "Red Light Violation": "No",
    "Helmet Violation": "No",
    "Seatbelt Violation": "No",
    "Mobile Phone Usage": "No",
    "Illegal U Turn": "No",
}

court_mapping = {
    # --- SERIOUS OFFENSES (Mandatory Court/Magistrate) ---
    "Hit and Run": "Yes",             # Criminal offense (IPC), strictly court.
    "Drunk Driving": "Yes",           # Mandatory court appearance for sentencing/fine.
    "Driving Without License": "Yes", # Often sent to court due to high fine amount (Sec 181).
    
    # --- STANDARD TRAFFIC VIOLATIONS (Compounding/Spot Fines) ---
    "Overspeeding": "No",             # usually settled via Camera/Online Challan.
    "Red Light Violation": "No",      # usually settled via Camera/Online Challan.
    "Wrong Lane": "No",               # Spot fine.
    "No Parking": "No",               # Pay towing charge + fine to release vehicle.
    "Seatbelt Violation": "No",       # Spot fine.
    "Helmet Violation": "No",         # Spot fine.
    "Mobile Phone Usage": "No",       # Spot fine (though license seizure is possible).
    "Illegal U Turn": "No",           # Spot fine.
    "Overloading": "No"               # Usually settled with RTO/Police fine, unless commercial/extreme.
}

comments_list = [
    "First Violation", "First Violation", "First Violation", "First Violation", "First Violation", 
    "Warning Issued", "Warning Issued", "Warning Issued", "Warning Issued", 
    "Repeat Offender", "Repeat Offender",
    "Fine Paid On Spot", 
]