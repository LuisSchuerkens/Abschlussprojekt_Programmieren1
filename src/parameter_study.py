import logging
from pathlib import Path

import matplotlib.pyplot as plt

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


def run_mass_study(route_data, rider_masses: list[float]) -> dict:
    """
    Führt die Simulation für verschiedene Fahrermassen durch und
    gibt die SOC-Verläufe als Dictionary zurück.
    """
    results = {}
    for mass in rider_masses:
        data = vehicle.add_vehicle_data(route_data, rider_mass=mass)
        battery = battery_pack.LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        simulator = battery_simulator.BatterySimulator(battery)
        simulator.simulate_power(data["power_W"].tolist(), data["time_diff_s"].tolist())
        results[mass] = simulator.soc_profile

        end_soc = simulator.soc_profile[-1] * 100
        logging.info(f"Parameterstudie Masse {mass:.0f} kg -> End-SOC {end_soc:.2f} %")
        print(f"Fahrermasse {mass:.0f} kg -> End-SOC LiPo: {end_soc:.2f} %")

    return results


def run_cwa_study(route_data, cwa_values: list[float]) -> dict:
    """
    Führt die Simulation für verschiedene Luftwiderstandsbeiwerte durch und
    gibt die SOC-Verläufe als Dictionary zurück.
    """
    results = {}
    for cw_a in cwa_values:
        data = vehicle.add_vehicle_data(route_data, cw_a=cw_a)
        battery = battery_pack.LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        simulator = battery_simulator.BatterySimulator(battery)
        simulator.simulate_power(data["power_W"].tolist(), data["time_diff_s"].tolist())
        results[cw_a] = simulator.soc_profile

        end_soc = simulator.soc_profile[-1] * 100
        logging.info(f"Parameterstudie cW*A {cw_a} -> End-SOC {end_soc:.2f} %")
        print(f"cW*A {cw_a} -> End-SOC LiPo: {end_soc:.2f} %")

    return results


def main():
    logging.info("Parameterstudie gestartet.")

    file_path = "data/final_project_input_data.csv"
    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)
    distance_km = route_data["total_distance_m"] / 1000

    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    mass_results = run_mass_study(route_data, [60.0, 70.0, 85.0])
    plots.plot_mass_study(distance_km, mass_results, str(results_dir / "parameterstudie_masse.png"))

    cwa_results = run_cwa_study(route_data, [0.4, 0.5625, 0.7])
    plots.plot_cwa_study(distance_km, cwa_results, str(results_dir / "parameterstudie_cwa.png"))

    plt.show()

    logging.info("Parameterstudie abgeschlossen.")


if __name__ == "__main__":
    main()