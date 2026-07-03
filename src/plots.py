import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_speed_profile(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt ein Geschwindigkeitsprofil über der Strecke.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    plt.plot(distance_km, route_data["speed_km_h"])
    plt.title("Geschwindigkeit über der Strecke")
    plt.xlabel("Strecke in km")
    plt.ylabel("Geschwindigkeit in km/h")
    plt.grid(True)

    if output_path is not None:
        plt.savefig(output_path)


def plot_power_profile(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt ein Leistungsprofil über der Strecke.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    plt.plot(distance_km, route_data["power_W"])
    plt.title("Leistung über der Strecke")
    plt.xlabel("Strecke in km")
    plt.ylabel("Leistung in W")
    plt.grid(True)

    if output_path is not None:
        plt.savefig(output_path)


def plot_battery_soc(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt einen Vergleich des Ladezustands von LiPo und NMC.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    plt.plot(distance_km, route_data["lipo_soc_percent"], label="LiPo")
    plt.plot(distance_km, route_data["nmc_soc_percent"], label="NMC")
    plt.title("Ladezustand der Akkus über der Strecke")
    plt.xlabel("Strecke in km")
    plt.ylabel("Ladezustand in %")
    plt.grid(True)
    plt.legend()

    if output_path is not None:
        plt.savefig(output_path)


def plot_battery_voltage(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt einen Vergleich der Akkuspannung von LiPo und NMC.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    plt.plot(distance_km, route_data["lipo_voltage_V"], label="LiPo")
    plt.plot(distance_km, route_data["nmc_voltage_V"], label="NMC")
    plt.title("Akkuspannung über der Strecke")
    plt.xlabel("Strecke in km")
    plt.ylabel("Spannung in V")
    plt.grid(True)
    plt.legend()

    if output_path is not None:
        plt.savefig(output_path)


def plot_height_profile(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt ein Höhenprofil über der Strecke.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    plt.plot(distance_km, route_data["ele"])
    plt.title("Höhenprofil der Route")
    plt.xlabel("Strecke in km")
    plt.ylabel("Höhe in m")
    plt.grid(True)

    if output_path is not None:
        plt.savefig(output_path)


def create_all_plots(route_data: pd.DataFrame, output_dir: str = "results") -> None:
    """
    Erstellt alle Diagramme für die E-Bike-Simulation und speichert sie als PNG.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    plot_speed_profile(route_data, str(output_path / "geschwindigkeit.png"))
    plot_power_profile(route_data, str(output_path / "leistung.png"))
    plot_battery_soc(route_data, str(output_path / "akku_soc.png"))
    plot_battery_voltage(route_data, str(output_path / "akku_spannung.png"))
    plot_height_profile(route_data, str(output_path / "hoehenprofil.png"))

    logging.info(f"Plots wurden erstellt und in '{output_dir}' gespeichert.")
    plt.show()
    