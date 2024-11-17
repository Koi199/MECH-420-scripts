# %%
def calculate_tow_power(aircraft_weight_kg, towing_speed_kph, rolling_resistance_coef = 0.17, safety_factor = 1.5):
    """
    Calculate required tow motor power based on aircraft parameters.
    
    Parameters:
    aircraft_weight_kg: float - Total weight of aircraft in kg
    towing_speed_kph: float - Desired towing speed in km/h
    incline_percent: float - Maximum incline grade in percent (default 0%)
    rolling_resistance_coef: float - Rolling resistance coefficient (default 0.02)
    safety_factor: float - Safety margin multiplier (default 1.5)
    
    Returns:
    tuple: (required_power_kw, force_newtons)
    """

    gravity = 9.81

    assert isinstance(aircraft_weight_kg, (int, float)), "aircraft_weight_kg must be numeric"
    assert isinstance(rolling_resistance_coef, (int, float)), "rolling_resistance_coef must be numeric"
    assert isinstance(gravity, (int, float)), "gravity must be numeric"

    # Rolling resistance force
    rolling_force = aircraft_weight_kg * gravity * rolling_resistance_coef
    
    # Total force needed
    total_force = rolling_force * safety_factor
    
    # Power required (in Watts)
    towing_speed_mps = towing_speed_kph / 3.6
    power_watts = total_force * towing_speed_mps
    
    return power_watts, total_force


def get_motor_recommendation(required_power_kw):
    """
    Provide motor size recommendation based on calculated power requirement.
    
    Parameters:
    required_power_kw: float - Required power in kilowatts
    
    Returns:
    str: Motor recommendation description
    """
    if required_power_kw < 20:
        return "Small tow tractor (15-20 kW) suitable for light aircraft"
    elif required_power_kw < 50:
        return "Medium tow tractor (40-50 kW) suitable for regional aircraft"
    elif required_power_kw < 100:
        return "Large tow tractor (75-100 kW) suitable for narrow-body commercial"
    else:
        return f"Heavy-duty tow tractor ({round(required_power_kw * 1.2)} kW) required for wide-body aircraft"

# # Example calculations for different aircraft types
# # (aircraft type, weight, speed)
# examples = [
#     ("Light aircraft (2,000 kg)", 2000, 5),
#     ("Regional aircraft (15,000 kg)", 15000, 5),
#     ("Narrow-body (45,000 kg)", 45000, 4),
#     ("Wide-body (200,000 kg)", 200000, 3)
# ]
    
# print("Aircraft Tow Motor Power Requirements:\n")
# for aircraft_type, weight, speed in examples:
#     power_kw, force_n = calculate_tow_power(weight, speed)
#     recommendation = get_motor_recommendation(power_kw)
        
#     print(f"{aircraft_type}:")
#     print(f"Weight: {weight:,} kg")
#     print(f"Towing speed: {speed} km/h")
#     print(f"Required power: {power_kw:.1f} kW")
#     print(f"Total force: {force_n:.1f} N")
#     print(f"Recommendation: {recommendation}")
#     print()

# %%
def get_rolling_coefficient(surface_type="concrete", wheel_type="dual", condition="dry"):
    """
    Calculate rolling resistance coefficient based on surface type and wheel configuration.
    
    Parameters:
    surface_type: str - Type of surface (concrete, asphalt, gravel, grass)
    wheel_type: str - Type of wheel configuration (single, dual, bogie)
    condition: str - Surface condition (dry, wet, contaminated)
    
    Returns:
    float: Rolling resistance coefficient
    """
    # Base coefficients for different surfaces (dry conditions)
    base_coefficients = {
        "concrete": {
            "single": 0.015,
            "dual": 0.013,
            "bogie": 0.012
        },
        "asphalt": {
            "single": 0.017,
            "dual": 0.015,
            "bogie": 0.014
        },
        "gravel": {
            "single": 0.045,
            "dual": 0.040,
            "bogie": 0.038
        },
        "grass": {
            "single": 0.080,
            "dual": 0.075,
            "bogie": 0.070
        }
    }
    
    # Condition multipliers
    condition_multipliers = {
        "dry": 1.0,
        "wet": 1.3,
        "contaminated": 1.5  # snow, slush, or other contamination
    }
    
    # Get base coefficient
    base_coef = base_coefficients.get(surface_type, {}).get(wheel_type, 0.02)
    
    # Apply condition multiplier
    return base_coef * condition_multipliers.get(condition, 1.0)

def calculate_total_rolling_resistance(aircraft_weight_kg, surface_type="concrete", 
                                    wheel_type="dual", condition="dry"):
    """
    Calculate total rolling resistance force for an aircraft.
    
    Parameters:
    aircraft_weight_kg: float - Aircraft weight in kg
    surface_type: str - Type of surface
    wheel_type: str - Type of wheel configuration
    condition: str - Surface condition
    
    Returns:
    tuple: (force_newtons, coefficient)
    """
    coefficient = get_rolling_coefficient(surface_type, wheel_type, condition)
    gravity = 9.81  # m/s²
    force = aircraft_weight_kg * gravity * coefficient
    return force, coefficient

print("Aircraft Rolling Resistance Coefficients and Forces\n")
    
# # Test conditions
# surfaces = ["concrete", "asphalt", "gravel", "grass"]
# wheel_types = ["single", "dual", "bogie"]
# conditions = ["dry", "wet", "contaminated"]
    
# # Example aircraft weight (50,000 kg - typical narrow-body)
# aircraft_weight = 50000
    
# print(f"Aircraft weight: {aircraft_weight:,} kg\n")
# print("Rolling Resistance Coefficients:")
# print("-" * 60)
# print(f"{'Surface':<12} {'Wheel Type':<10} {'Condition':<12} {'Coefficient':<10} {'Force (N)':<10}")
# print("-" * 60)
   
# for surface in surfaces:
#     for wheel in wheel_types:
#         for condition in conditions:
#             force, coef = calculate_total_rolling_resistance(
#                 aircraft_weight, surface, wheel, condition
#             )
#             print(f"{surface:<12} {wheel:<10} {condition:<12} {coef:.4f} {force:,.0f}")
#     print("-" * 60)

# %%
def calculate_battery_requirements(motor_power_kw, runtime_hours, 
                                voltage=80, depth_of_discharge=0.8,
                                motor_efficiency=0.85, inverter_efficiency=0.95,
                                battery_type="lithium"):
    """
    Calculate battery requirements for an electric motor.
    
    Parameters:
    motor_power_kw: float - Motor power rating in kilowatts
    runtime_hours: float - Required runtime in hours
    voltage: float - System voltage (default 80V)
    depth_of_discharge: float - Maximum allowable DOD (default 0.8 or 80%)
    motor_efficiency: float - Motor efficiency (default 0.85 or 85%)
    inverter_efficiency: float - Inverter efficiency (default 0.95 or 95%)
    battery_type: str - Battery chemistry type
    
    Returns:
    dict: Battery specifications and requirements
    """
    # Battery chemistry specifications
    battery_specs = {
        "lithium": {
            "energy_density_wh_kg": 150,  # Wh/kg
            "cycles": 2000,
            "cost_per_kwh": 300,  # USD
            "efficiency": 0.95
        },
        "lead_acid": {
            "energy_density_wh_kg": 40,
            "cycles": 500,
            "cost_per_kwh": 150,
            "efficiency": 0.85
        },
        "nimh": {
            "energy_density_wh_kg": 80,
            "cycles": 1000,
            "cost_per_kwh": 400,
            "efficiency": 0.90
        }
    }
    
    # Get battery specifications
    bat_specs = battery_specs.get(battery_type, battery_specs["lithium"])
    battery_efficiency = bat_specs["energy_density_wh_kg"]
    
    # Calculate total system efficiency
    system_efficiency = motor_efficiency * inverter_efficiency * bat_specs["efficiency"]
    
    # Calculate energy requirements
    daily_energy_kwh = (motor_power_kw * runtime_hours) / system_efficiency
    
    # Account for depth of discharge
    battery_capacity_kwh = daily_energy_kwh / depth_of_discharge
    
    # Calculate amp-hours
    amp_hours = (battery_capacity_kwh * 1000) / voltage
    
    # Calculate weight and volume
    battery_weight_kg = (battery_capacity_kwh * 1000) / bat_specs["energy_density_wh_kg"]
    
    # Calculate estimated cost
    estimated_cost = battery_capacity_kwh * bat_specs["cost_per_kwh"]
    
    # Calculate peak current requirements
    peak_current_amps = (motor_power_kw * 1000) / (voltage * motor_efficiency)
    
    return {
        "battery_capacity_kwh": round(battery_capacity_kwh, 2),
        "amp_hours": round(amp_hours, 2),
        "battery_weight_kg": round(battery_weight_kg, 2),
        "peak_current_amps": round(peak_current_amps, 2),
        "estimated_cost_usd": round(estimated_cost, 2),
        "expected_cycles": bat_specs["cycles"],
        "daily_energy_kwh": round(daily_energy_kwh, 2),
        "system_efficiency": round(system_efficiency * 100, 1)
    }

def print_battery_comparison(motor_power_kw, runtime_hours):
    """
    Print comparison of different battery types for given requirements.
    
    Parameters:
    motor_power_kw: float - Motor power rating in kilowatts
    runtime_hours: float - Required runtime in hours
    """
    battery_types = ["lithium", "lead_acid", "nimh"]
    
    print(f"\nBattery Comparison for {motor_power_kw}kW Motor, {runtime_hours}h Runtime")
    print("-" * 80)
    print(f"{'Parameter':<20} {'Lithium':<20} {'Lead Acid':<20} {'NiMH':<20}")
    print("-" * 80)
    
    results = {}
    for bat_type in battery_types:
        results[bat_type] = calculate_battery_requirements(
            motor_power_kw, runtime_hours, battery_type=bat_type
        )
    
    params = [
        ("Capacity (kWh)", "battery_capacity_kwh"),
        ("Amp Hours", "amp_hours"),
        ("Weight (kg)", "battery_weight_kg"),
        ("Peak Current (A)", "peak_current_amps"),
        ("Cost (USD)", "estimated_cost_usd"),
        ("Lifecycle (cycles)", "expected_cycles"),
        ("Efficiency (%)", "system_efficiency")
    ]
    
    for param_name, param_key in params:
        print(f"{param_name:<20}", end="")
        for bat_type in battery_types:
            value = results[bat_type][param_key]
            print(f"{value:,.1f}".ljust(20), end="")
        print()


    # # Example cases for different tow motor sizes
    # test_cases = [
    #     ("Small Aircraft Tug", 20, 4),
    #     ("Medium Aircraft Tug", 50, 6),
    #     ("Large Aircraft Tug", 100, 8)
    # ]
    
    # for case_name, power, runtime in test_cases:
    #     print(f"\n{case_name} ({power}kW)")
    #     print_battery_comparison(power, runtime)


# %%
import math

def calculate_tugs_required(tug_uptime, charging_time, trip_time, total_trips_per_year):
    """
    Calculate the number of airplane tugs needed.
    
    Parameters:
    - tug_uptime (float): The operational time of a tug per charge in hours.
    - charging_time (float): The time it takes to recharge the tug in hours.
    - trip_time (float): The time for a single trip (runway to taxiway) in minutes.
    - total_trips_per_year (int): The total number of trips needed per year.
    
    Returns:
    - int: The number of tugs required.
    """
    # Convert tug uptime to minutes
    tug_uptime_minutes = tug_uptime * 60
    
    # Calculate the number of trips a tug can complete per charge
    trips_per_charge = tug_uptime_minutes // trip_time
    
    # Calculate the number of charges per day a tug can have
    charge_cycle_time = tug_uptime + charging_time  # total time for one charge cycle in hours
    charges_per_day = 24 / charge_cycle_time
    
    # Calculate the total trips a tug can handle in one day
    trips_per_day = trips_per_charge * charges_per_day
    
    # Calculate the total trips a tug can handle per year
    trips_per_year_per_tug = trips_per_day * 365
    
    # Calculate the number of tugs required
    tugs_required = math.ceil(total_trips_per_year / trips_per_year_per_tug)
    
    return tugs_required

# # Example usage:
# tug_uptime = 6  # hours
# charging_time = 2  # hours
# trip_time = 20  # minutes
# total_trips_per_year = 600000  # total trips needed per year

# tugs_needed = calculate_tugs_required(tug_uptime, charging_time, trip_time, total_trips_per_year)
# print(f"Number of tugs required: {tugs_needed}")


# %% [markdown]
# # Final calculations and putting it all together

# %%
aircraft_weight = 50000 # kg
aircraft_speed = 3.0 # kph

rolling_force, rolling_coefficient = calculate_total_rolling_resistance(aircraft_weight_kg=aircraft_weight, surface_type="concrete", wheel_type="dual", condition="dry")
power, tow_force = calculate_tow_power(aircraft_weight_kg=aircraft_weight, towing_speed_kph=aircraft_speed, rolling_resistance_coef=rolling_coefficient, safety_factor=1.5)

print(f"\nRolling Force: {rolling_force} N")
print(f"\nRolling Coefficient: {rolling_coefficient}")
print(f"\nTow Power: {power:.2f} W")
print(f"\nTow Force: {tow_force:.2f} N")

print_battery_comparison(motor_power_kw=30, runtime_hours=6)

# Number of Tugs needed
"""
    Calculate the number of airplane tugs needed.
    
    Parameters:
    - tug_uptime (float): The operational time of a tug per charge in hours.
    - charging_time (float): The time it takes to recharge the tug in hours.
    - trip_time (float): The time for a single trip (runway to taxiway) in minutes.
    - total_trips_per_year (int): The total number of trips needed per year.
    
    Returns:
    - int: The number of tugs required.
    """
Number_of_tugs = calculate_tugs_required(tug_uptime = 6, charging_time = 2, trip_time = 30, total_trips_per_year = 300000)

print(f"\nNumber of Tugs needed: {Number_of_tugs}")


