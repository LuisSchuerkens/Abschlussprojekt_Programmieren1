import logging

import gps_data
import vehicle
import battery_pack
import battery_simulator
import plots
from pathlib import Path 

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

    lipo_battery = battery_pack.LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
    nmc_battery = battery_pack.NmcBattery(capacity_nom_Ah=35.0, initial_soc=1.0)

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
    
    results_dir = Path(__file__).resolve().parent.parent / "results"
    plots.create_all_plots(route_data, str(results_dir))

    
if __name__ == "__main__":
    main()