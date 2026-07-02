import logging

import gps_data
import vehicle
import battery_pack
import battery_simulator
import plots

logging.basicConfig(
    format="%(asctime)s:%(levelname)s: %(message)s",
    level=logging.INFO,
    filename="app.log",
    encoding="utf-8"
)

def main():
    """Hauptfunktion des Programms."""
    logging.info("E-Bike Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"

    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)
    route_data = vehicle.add_vehicle_data(route_data)

    power_profile = route_data["power_W"].tolist()
    duration_profile = route_data["time_diff_s"].tolist()

    soc_points = [
        0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26,
        0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00
    ]

    lipo_voltage_points = [
        32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81,
        39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42.00
    ]

    nmc_voltage_points = [
        32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.39,
        35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00
    ]

    lipo_battery = battery_pack.BatteryPack(
        capacity_nom_Ah=35.0,
        internal_resistance_mOhm=80.0,
        initial_soc=1.0,
        soc_points=soc_points,
        voltage_points=lipo_voltage_points,
    )

    nmc_battery = battery_pack.BatteryPack(
        capacity_nom_Ah=35.0,
        internal_resistance_mOhm=70.0,
        initial_soc=1.0,
        soc_points=soc_points,
        voltage_points=nmc_voltage_points,
    )

    lipo_simulator = battery_simulator.BatterySimulator(lipo_battery)
    lipo_simulator.simulate_power(power_profile, duration_profile)

    nmc_simulator = battery_simulator.BatterySimulator(nmc_battery)
    nmc_simulator.simulate_power(power_profile, duration_profile)

    route_data["lipo_soc_percent"] = [soc * 100 for soc in lipo_simulator.soc_profile]
    route_data["lipo_voltage_V"] = lipo_simulator.voltage_profile
    route_data["lipo_current_A"] = lipo_simulator.current_profile

    route_data["nmc_soc_percent"] = [soc * 100 for soc in nmc_simulator.soc_profile]
    route_data["nmc_voltage_V"] = nmc_simulator.voltage_profile
    route_data["nmc_current_A"] = nmc_simulator.current_profile

    logging.info("Akku-Simulation abgeschlossen.")
    logging.info(f"End-Ladezustand LiPo: {route_data['lipo_soc_percent'].iloc[-1]:.2f} %")
    logging.info(f"End-Ladezustand NMC: {route_data['nmc_soc_percent'].iloc[-1]:.2f} %")
    logging.info(f"Minimale Spannung LiPo: {route_data['lipo_voltage_V'].min():.2f} V")
    logging.info(f"Minimale Spannung NMC: {route_data['nmc_voltage_V'].min():.2f} V")

    total_distance_km = route_data["total_distance_m"].iloc[-1] / 1000

    total_time_s = (route_data["time"].iloc[-1] - route_data["time"].iloc[0]).total_seconds()
    total_time_h = total_time_s / 3600

    average_speed_km_h = total_distance_km / total_time_h

    elevation_difference = route_data["ele"].diff()

    elevation_gain_m = elevation_difference[elevation_difference > 0].sum()
    elevation_loss_m = -elevation_difference[elevation_difference < 0].sum()

    logging.info("Zusammenfassung der gesamten Route:")
    logging.info(f"Durchschnittsgeschwindigkeit: {average_speed_km_h:.2f} km/h")
    logging.info(f"Benötigte Zeit: {total_time_h:.2f} h")
    logging.info(f"Höhenmeter Anstieg: {elevation_gain_m:.2f} m")
    logging.info(f"Höhenmeter Abstieg: {elevation_loss_m:.2f} m")
    
    plots.create_all_plots(route_data)

    
if __name__ == "__main__":
    main()