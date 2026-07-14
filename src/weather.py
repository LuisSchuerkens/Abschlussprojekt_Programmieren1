import json
import logging
import urllib.parse
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import battery_pack
import battery_simulator
import gps_data


def fetch_wind(latitude: float, longitude: float, date: str) -> tuple[float | None, float | None]:
    """
    Holt die mittlere Windgeschwindigkeit und Windrichtung fuer den Fahrttag
    von der Open-Meteo-Archiv-API.

    Parameters
    ----------
    latitude : float
        Breitengrad der Route.
    longitude : float
        Laengengrad der Route.
    date : str
        Datum im Format YYYY-MM-DD.

    Returns
    -------
    tuple[float | None, float | None]
        Windgeschwindigkeit in m/s und Windrichtung in Grad.
        Falls keine Daten geladen werden koennen: (None, None).
    """
    parameters = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "hourly": "wind_speed_10m,wind_direction_10m",
    })

    url = f"https://archive-api.open-meteo.com/v1/archive?{parameters}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode())

        speeds = [
            speed
            for speed in data["hourly"]["wind_speed_10m"]
            if speed is not None
        ]

        directions = [
            direction
            for direction in data["hourly"]["wind_direction_10m"]
            if direction is not None
        ]

        average_speed_kmh = sum(speeds) / len(speeds)
        average_direction = sum(directions) / len(directions)

        return average_speed_kmh / 3.6, average_direction

    except Exception as error:
        logging.warning(f"Wetterdaten konnten nicht geladen werden: {error}")
        return None, None


def simulate_with_wind(
    route_data: pd.DataFrame,
    wind_speed_ms: float,
    wind_from_deg: float,
) -> float:
    """
    Rechnet die Fahrt mit einer Windkomponente entlang der Fahrtrichtung nach
    und gibt den End-Ladezustand in Prozent zurueck.

    Parameters
    ----------
    route_data : pd.DataFrame
        Routendaten mit Bewegungsdaten.
    wind_speed_ms : float
        Windgeschwindigkeit in m/s.
    wind_from_deg : float
        Windrichtung in Grad.

    Returns
    -------
    float
        End-Ladezustand des LiPo-Akkus in Prozent.
    """
    total_mass = 80.0
    gravity = 9.81

    temperature_kelvin = route_data["temperature"] + 273.15
    pressure = 101325.0 * (1 - 0.0065 * route_data["ele"] / 288.15) ** 5.255
    air_density = pressure / (287.05 * temperature_kelvin)

    angle = np.radians(wind_from_deg - route_data["bearing"])
    headwind = wind_speed_ms * np.cos(angle)
    effective_speed = (route_data["speed_m_s"] + headwind).clip(lower=0)

    air_force = 0.5 * air_density * 0.5625 * effective_speed ** 2
    slope_force = total_mass * gravity * route_data["slope"]
    rolling_force = 0.008 * total_mass * gravity * np.cos(np.arctan(route_data["slope"]))
    acceleration_force = total_mass * route_data["acceleration_m_s2"]

    total_force = air_force + slope_force + acceleration_force + rolling_force
    total_force = total_force.clip(lower=0)

    power = total_force * route_data["speed_m_s"]

    battery = battery_pack.LipoBattery(35.0, initial_soc=1.0)
    simulator = battery_simulator.BatterySimulator(battery)

    simulator.simulate_power(power.tolist(), route_data["time_diff_s"].tolist())

    return simulator.soc_profile[-1] * 100


def main() -> None:
    """
    Hauptfunktion fuer die Wetterdaten- und Wind-Simulation.
    """
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s: %(message)s",
        level=logging.INFO,
        filename="app.log",
        encoding="utf-8",
    )

    logging.info("Wetterdaten-Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"

    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)

    date = str(route_data["time"].iloc[0].date())
    latitude = route_data["lat"].mean()
    longitude = route_data["lon"].mean()

    wind_speed, wind_direction = fetch_wind(latitude, longitude, date)

    if wind_speed is None or wind_direction is None:
        print("Keine Wetterdaten verfuegbar (kein Internet?). Abbruch ohne Fehler.")
        logging.info("Keine Wetterdaten verfuegbar.")
        return

    print(f"Wind am {date}: {wind_speed * 3.6:.1f} km/h aus {wind_direction:.0f} Grad")
    logging.info(f"Wind: {wind_speed * 3.6:.1f} km/h aus {wind_direction:.0f} Grad")

    soc_no_wind = simulate_with_wind(route_data, 0.0, 0.0)
    soc_with_wind = simulate_with_wind(route_data, wind_speed, wind_direction)

    print(f"End-SOC ohne Wind: {soc_no_wind:.2f} %")
    print(f"End-SOC mit Wind: {soc_with_wind:.2f} %")

    logging.info(
        f"End-SOC ohne Wind: {soc_no_wind:.2f} %, "
        f"mit Wind: {soc_with_wind:.2f} %"
    )

    results_dir = Path(__file__).resolve().parent.parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.bar(["ohne Wind", "mit Wind"], [soc_no_wind, soc_with_wind])
    plt.title("Einfluss des Windes auf den End-Ladezustand")
    plt.ylabel("End-Ladezustand in %")
    plt.grid(True, axis="y")
    plt.savefig(str(results_dir / "wind_einfluss.png"))
    plt.show()

    logging.info("Wetterdaten-Simulation abgeschlossen.")


if __name__ == "__main__":
    main()