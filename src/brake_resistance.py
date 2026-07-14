import logging
from pathlib import Path

import matplotlib.pyplot as plt

import gps_data
import vehicle
import battery_pack

def simulate_brake_resistance(file_path: str, max_charge_current: float=10.0):
    """
    Simuliert die Rekuperation mit begrenztem Ladestrom und berechnet die rekuperierte und dissipierte Energie.
    """
    
    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)
    route_data = vehicle.add_vehicle_data(route_data)

    battery = battery_pack.LipoBattery(35.0, initial_soc=1.0)

    recuperated_energy = 0.0
    dissipated_energy = 0.0

    for raw_power, duration in zip(route_data["power_raw_W"], route_data["time_diff_s"]):
        voltage = battery.open_circuit_voltage()

        if raw_power < 0:
            recuperation_power = -raw_power
            max_charge_power = max_charge_current * voltage

            if recuperation_power > max_charge_power:
                battery.apply_current(-max_charge_current, duration)
                recuperated_energy += max_charge_power * duration
                dissipated_energy += (recuperation_power - max_charge_power) * duration
            else:
                battery.apply_current(raw_power / voltage, duration)
                recuperated_energy += recuperation_power * duration
        else:
            current = raw_power / voltage if voltage > 0 else 0.0
            battery.apply_current(current, duration)

    return recuperated_energy, dissipated_energy


def main():
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s: %(message)s",
        level=logging.INFO,
        filename="app.log",
        encoding="utf-8",
    )

    logging.info("Bremswiderstand-Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"
    recuperated, dissipated = simulate_brake_resistance(file_path)

    logging.info(f"Rekuperierte Energie: {recuperated / 1000:.0f} kJ")
    logging.info(f"Im Bremswiderstand dissipiert: {dissipated / 1000:.0f} kJ")

    print(f"Rekuperiert: {recuperated / 1000:.0f} kJ")
    print(f"Bremswiderstand: {dissipated / 1000:.0f} kJ")

    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.bar(
        ["Rekuperiert", "Bremswiderstand"],
        [recuperated / 1000, dissipated / 1000],
    )
    plt.title("Energiebilanz der Rekuperation")
    plt.ylabel("Energie in kJ")
    plt.grid(True, axis="y")
    plt.savefig(str(results_dir / "bremswiderstand.png"))
    plt.show()

    logging.info("Bremswiderstand-Simulation abgeschlossen.")


if __name__ == "__main__":
    main()