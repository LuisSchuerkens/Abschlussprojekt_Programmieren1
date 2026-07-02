import matplotlib.pyplot as plt
import pandas as pd


def plot_speed_profile(route_data: pd.DataFrame) -> None:
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


def plot_power_profile(route_data: pd.DataFrame) -> None:
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


def plot_battery_soc(route_data: pd.DataFrame) -> None:
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


def plot_battery_voltage(route_data: pd.DataFrame) -> None:
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

def plot_height_profile(route_data: pd.DataFrame) -> None:
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

def create_all_plots(route_data: pd.DataFrame) -> None:
    """
    Erstellt alle Diagramme für die E-Bike-Simulation.
    """
    plot_speed_profile(route_data)
    plot_power_profile(route_data)
    plot_battery_soc(route_data)
    plot_battery_voltage(route_data)
    plot_height_profile(route_data)


    print("Plots wurden erstellt.")
    plt.show()