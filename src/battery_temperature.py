import logging
from pathlib import Path

import matplotlib.pyplot as plt

import gps_data
import vehicle
import battery_pack


class ThermalBattery(battery_pack.LipoBattery):
    """
    LiPo-Akku mit einfachem Temperaturmodell.
    Die Temperatur steigt durch die ohmschen Verluste (I^2 * R) und
    sinkt durch Kuehlung Richtung Umgebungstemperatur.
    """

    def __init__(self, capacity_nom_Ah, initial_soc=1.0, ambient_temperature=25.0):
        super().__init__(capacity_nom_Ah, initial_soc)
        self.temperature = ambient_temperature
        self.ambient_temperature = ambient_temperature
        self.heat_capacity = 1200.0
        self.cooling_coefficient = 0.8
        self.reference_resistance = self.R_int

    def update_temperature(self, current, duration):
        heat_generated = current ** 2 * self.R_int * duration
        heat_lost = self.cooling_coefficient * (self.temperature - self.ambient_temperature) * duration
        self.temperature += (heat_generated - heat_lost) / self.heat_capacity


def simulate_temperature(file_path, ambient_temperature=28.0):
    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)
    route_data = vehicle.add_vehicle_data(route_data)

    battery = ThermalBattery(35.0, initial_soc=1.0, ambient_temperature=ambient_temperature)
    temperatures = []

    for power, duration in zip(route_data["power_W"], route_data["time_diff_s"]):
        voltage = battery.open_circuit_voltage()
        current = power / voltage if voltage > 0 else 0.0
        battery.apply_current(current, duration)
        battery.update_temperature(current, duration)
        temperatures.append(battery.temperature)

    distance_km = route_data["total_distance_m"] / 1000
    return distance_km, temperatures


def main():
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s: %(message)s",
        level=logging.INFO,
        filename="app.log",
        encoding="utf-8",
    )
    logging.info("Akkutemperatur-Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"
    distance_km, temperatures = simulate_temperature(file_path)

    logging.info(f"Maximale Akkutemperatur: {max(temperatures):.1f} C")
    print(f"Start: {temperatures[0]:.1f} C, Maximum: {max(temperatures):.1f} C, Ende: {temperatures[-1]:.1f} C")

    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    plt.figure()
    plt.plot(distance_km, temperatures)
    plt.title("Akkutemperatur ueber der Strecke")
    plt.xlabel("Strecke in km")
    plt.ylabel("Temperatur in Grad C")
    plt.grid(True)
    plt.savefig(str(results_dir / "akku_temperatur.png"))
    plt.show()

    logging.info("Akkutemperatur-Simulation abgeschlossen.")


if __name__ == "__main__":
    main()