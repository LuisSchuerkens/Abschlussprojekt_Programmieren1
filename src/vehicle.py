import logging

import pandas as pd

def calculate_air_density(elevation, temperature_celsius):
    """
    Berechnet die Luftdichte aus Höhe und Temperatur.
    Der Luftdruck wird mit der barometrischen Höhenformel bestimmt,
    die Dichte über die ideale Gasgleichung.
    """
    pressure_sea_level = 101325.0
    specific_gas_constant = 287.05

    temperature_kelvin = temperature_celsius + 273.15
    pressure = pressure_sea_level * (1 - 0.0065 * elevation / 288.15) ** 5.255

    return pressure / (specific_gas_constant * temperature_kelvin)

def add_vehicle_data(gps_data: pd.DataFrame, rider_mass: float = 70.0) -> pd.DataFrame:
    """
    Berechnet Fahrzeugkraft, Leistung, Drehmoment und Motorstrom.

    Parameters
    ----------
    gps_data : pd.DataFrame
        GPS-Daten mit Geschwindigkeit, Beschleunigung und Steigung.

    Returns
    -------
    pd.DataFrame
        GPS-Daten mit zusätzlichen Fahrzeugdaten.
    """
    gps_data = gps_data.copy()

    bike_mass = 10.0
    total_mass = rider_mass + bike_mass

    gravity = 9.81
    air_density = calculate_air_density(gps_data["ele"], gps_data["temperature"])
    cw_a = 0.5625

    wheel_diameter_inch = 27.0
    inch_to_meter = 0.0254
    wheel_radius = wheel_diameter_inch * inch_to_meter / 2

    motor_constant = 1.5

    speed = gps_data["speed_m_s"]
    acceleration = gps_data["acceleration_m_s2"]
    slope = gps_data["slope"]

    air_force = 0.5 * air_density * cw_a * speed ** 2
    slope_force = total_mass * gravity * slope
    acceleration_force = total_mass * acceleration

    total_force = air_force + slope_force + acceleration_force

    # Für die minimal Anforderungen (ohne Erweiterung) setzen wir minimale Antriebskraft auf 0.
    total_force = total_force.clip(lower=0)

    power = total_force * speed
    torque = total_force * wheel_radius
    motor_current = torque / motor_constant

    gps_data["air_force_N"] = air_force
    gps_data["slope_force_N"] = slope_force
    gps_data["acceleration_force_N"] = acceleration_force
    gps_data["total_force_N"] = total_force
    gps_data["power_W"] = power
    gps_data["torque_Nm"] = torque
    gps_data["motor_current_A"] = motor_current

    logging.info("Fahrzeugdaten wurden berechnet.")
    logging.info(f"Maximale Leistung: {gps_data['power_W'].max():.2f} W")
    logging.info(f"Maximaler Motorstrom: {gps_data['motor_current_A'].max():.2f} A")

    return gps_data