import random
from datetime import datetime, timedelta
from faker import Faker


from core.data_variables import vehicle_colors_list, driver_genders_list, states_list, violation_types_list, weather_conditions_list, road_conditions_list, license_types_list, issuing_agencies_list, license_validity_list, breathalyzer_results_list, comments_list

from core.data_variables import vehicle_types_mapping, helmet_worn_mapping, seatbelt_worn_mapping, no_of_passengers_mapping, fine_mapping, alcohol_levels_mapping,towing_mapping, court_mapping, payment_methods_mapping


# ---------------------------------------
# FAKE DATA GENERATOR SETUP
# ---------------------------------------
fake = Faker("en_IN")

# SINGLE RECORD GENERATOR
def generate_record(idx, date: datetime.date):
    violation_id = f"VLT{idx:06d}"
    violation_type = random.choice(violation_types_list)
    fine_amount = fine_mapping.get(violation_type, random.randint(100, 10000))
    location = random.choice(states_list)
    date = date.strftime("%Y-%m-%d")
    time = fake.time()

    vehicle_type = vehicle_types_mapping.get(violation_type, 'NA')
    vehicle_color = random.choice(vehicle_colors_list)

    vehicle_model_year = random.randint(1990, int(datetime.strptime(date, "%Y-%m-%d").date().year))

    registration_state = random.choice(states_list)

    helmet_worn = helmet_worn_mapping.get(vehicle_type, "NA")
    seatbelt_worn = seatbelt_worn_mapping.get(vehicle_type, "NA")

    driver_age = random.randint(18, 80)
    driver_gender = random.choice(driver_genders_list)

    number_of_passengers = no_of_passengers_mapping.get(vehicle_type, random.randint(0, 50))

    penalty_points = random.randint(0, 8)
    weather_condition = random.choice(weather_conditions_list)
    road_condition = random.choice(road_conditions_list)

    officer_id = f"OFF{random.randint(1000, 9999)}"
    license_type = random.choice(license_types_list)
    issuing_agency = random.choice(issuing_agencies_list)
    license_validity = random.choice(license_validity_list)
    
    traffic_light_status = random.choice(["Red", "Green", "Yellow"])
    
    speed_limit = random.randint(20, 120)
    recorded_speed = random.randint(0, 200)
    
    breathalyzer_result = random.choice(breathalyzer_results_list)
    alcohol_level = alcohol_levels_mapping.get(breathalyzer_result, 0.00)

    towed = towing_mapping.get(violation_type, "No")
    # -------------------------
    # Fine logic
    fine_paid = "NA"
    six_year_rule_date = datetime.today().date().replace(year=datetime.today().year - 6)
    if datetime.strptime(date, "%Y-%m-%d").date() < six_year_rule_date:
        fine_paid = "Yes"
    else:
        fine_paid = random.choice(["Yes", "No"])
    # --------------------------
    payment_method = payment_methods_mapping.get(fine_paid, "NA")

    court_appearance_required = court_mapping.get(violation_type, "No")
    previous_violations = random.randint(0, 20)
    comments = random.choice(comments_list)

    record = {
        "Violation_ID": violation_id,
        "Violation_Type": violation_type,
        "Fine_Amount": fine_amount,
        "Location": location,
        "Date": date,
        "Time": time,
        "Vehicle_Type": vehicle_type,
        "Vehicle_Color": vehicle_color,
        "Vehicle_Model_Year": vehicle_model_year,
        "Registration_State": registration_state,
        "Helmet_Worn": helmet_worn,
        "Seatbelt_Worn": seatbelt_worn,   
        "Driver_Age": driver_age,
        "Driver_Gender": driver_gender,
        "Number_of_Passengers": number_of_passengers,
        "Penalty_Points": penalty_points,
        "Weather_Condition": weather_condition,
        "Road_Condition": road_condition,
        "Officer_ID": officer_id,
        "License_Type": license_type,
        "Issuing_Agency": issuing_agency,
        "License_Validity": license_validity,
        "Traffic_Light_Status": traffic_light_status,
        "Speed_Limit": speed_limit,
        "Recorded_Speed": recorded_speed,
        "Alcohol_Level": alcohol_level,
        "Breathalyzer_Result": breathalyzer_result,
        "Towed": towed,
        "Fine_Paid": fine_paid,
        "Payment_Method": payment_method,
        "Court_Appearance_Required": court_appearance_required,
        "Previous_Violations": previous_violations,
        "Comments": comments
    }
    
    return record


# DATASET GENERATOR — DAY BY DAY
def generate_dataset_by_days(start_date=("2015-01-01"), end_date=(datetime.now().date().strftime("%Y-%m-%d")), min_records_per_day=5, max_records_per_day=15):
    
    current_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    violation_counter = 1
    records = []
    while current_date <= end_date:
        daily_count = random.randint(min_records_per_day, max_records_per_day)
        for _ in range(daily_count):
            records.append(generate_record(violation_counter, current_date))
            violation_counter += 1
        current_date += timedelta(days=1)
    return records