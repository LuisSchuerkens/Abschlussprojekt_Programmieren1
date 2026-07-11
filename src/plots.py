import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import folium
import geocoding


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


def plot_height_profile_with_slope(route_data: pd.DataFrame, output_path: str = None) -> None:
    """
    Erstellt ein Höhenprofil, bei dem die Punkte nach Steigung eingefärbt sind.
    Rot bedeutet bergauf, blau bedeutet bergab.
    """
    distance_km = route_data["total_distance_m"] / 1000

    plt.figure()
    scatter = plt.scatter(
        distance_km,
        route_data["ele"],
        c=route_data["slope_percent"],
        cmap="coolwarm",
        vmin=-10,
        vmax=10,
        s=4,
    )
    plt.colorbar(scatter, label="Steigung in %")
    plt.title("Höhenprofil mit Steigung")
    plt.xlabel("Strecke in km")
    plt.ylabel("Höhe in m")
    plt.grid(True)

    if output_path is not None:
        plt.savefig(output_path)

def create_route_map(route_data: pd.DataFrame, output_path: str) -> None:
    """
    Erstellt eine interaktive Karte der Route mit folium.
    Die markanten Punkte werden über Reverse Geocoding beschriftet.
    Die Karte wird als HTML-Datei gespeichert und kann im Browser geöffnet werden.
    """
    coordinates = list(zip(route_data["lat"], route_data["lon"]))

    center_lat = route_data["lat"].mean()
    center_lon = route_data["lon"].mean()

    route_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    folium.PolyLine(coordinates, color="blue", weight=3).add_to(route_map)

    highest_index = route_data["ele"].idxmax()

    start_location = geocoding.reverse_geocode(route_data["lat"].iloc[0], route_data["lon"].iloc[0])
    end_location = geocoding.reverse_geocode(route_data["lat"].iloc[-1], route_data["lon"].iloc[-1])
    highest_location = geocoding.reverse_geocode(
        route_data["lat"].iloc[highest_index], route_data["lon"].iloc[highest_index]
    )

    start_name = start_location.split(",")[0]
    end_name = end_location.split(",")[0]
    highest_name = highest_location.split(",")[0]

    folium.Marker(
        coordinates[0],
        popup=f"Start / Ziel (Rundkurs): {start_name}",
        icon=folium.Icon(color="green"),
    ).add_to(route_map)

    folium.Marker(
        coordinates[highest_index],
        popup=f"Hoechster Punkt: {highest_name}",
        icon=folium.Icon(color="orange"),
    ).add_to(route_map)

    route_map.save(output_path)
    logging.info(f"Routenkarte wurde gespeichert: {output_path}")
    logging.info(f"Routenkarte wurde gespeichert: {output_path}")


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
    plot_height_profile_with_slope(route_data, str(output_path / "hoehenprofil_steigung.png"))
    create_route_map(route_data, str(output_path / "route_karte.html"))

    logging.info(f"Plots wurden erstellt und in '{output_dir}' gespeichert.")
    plt.show()

def plot_mass_study(distance_km, results: dict, output_path: str = None) -> None:
    """
    Vergleicht die SOC-Verläufe für verschiedene Fahrermassen.
    results ist ein Dictionary: Fahrermasse -> SOC-Verlauf
    """
    plt.figure()
    for mass, soc_profile in results.items():
        soc_percent = [soc * 100 for soc in soc_profile]
        plt.plot(distance_km, soc_percent, label=f"{mass:.0f} kg")
    plt.title("Ladezustand bei verschiedenen Fahrermassen (LiPo)")
    plt.xlabel("Strecke in km")
    plt.ylabel("Ladezustand in %")
    plt.grid(True)
    plt.legend(title="Fahrermasse")

    if output_path is not None:
        plt.savefig(output_path)
    
def plot_cwa_study(distance_km, results: dict, output_path: str = None) -> None:
    """
    Vergleicht die SOC-Verläufe für verschiedene Luftwiderstandsbeiwerte.
    results ist ein Dictionary: cW*A-Wert -> SOC-Verlauf
    """
    plt.figure()
    for cw_a, soc_profile in results.items():
        soc_percent = [soc * 100 for soc in soc_profile]
        plt.plot(distance_km, soc_percent, label=f"cW*A = {cw_a}")
    plt.title("Ladezustand bei verschiedenen Luftwiderstandsbeiwerten (LiPo)")
    plt.xlabel("Strecke in km")
    plt.ylabel("Ladezustand in %")
    plt.grid(True)
    plt.legend(title="cW*A")

    if output_path is not None:
        plt.savefig(output_path)