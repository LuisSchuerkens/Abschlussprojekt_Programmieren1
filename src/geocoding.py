import logging
import json
import time
import urllib.request
import urllib.parse

import gps_data


def reverse_geocode(latitude: float, longitude: float) -> str:
    """
    Wandelt GPS-Koordinaten über die Nominatim-API in einen Ortsnamen um.
    Gibt bei einem Fehler (z.B. kein Internet) "unbekannt" zurück.
    """
    parameters = urllib.parse.urlencode({
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 14,
    })
    url = f"https://nominatim.openstreetmap.org/reverse?{parameters}"
    request = urllib.request.Request(url, headers={"User-Agent": "ebike-simulation-student-project"})

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())
        return data.get("display_name", "unbekannt")
    except Exception as error:
        logging.warning(f"Reverse Geocoding fehlgeschlagen: {error}")
        return "unbekannt"


def describe_route(file_path: str) -> None:
    """
    Bestimmt die Ortsnamen für markante Punkte der Route und schreibt sie ins Log.
    """
    route_data = gps_data.load_gps_data(file_path)

    start_index = 0
    end_index = len(route_data) - 1
    highest_index = route_data["ele"].idxmax()
    lowest_index = route_data["ele"].idxmin()

    points = {
        "Start": start_index,
        "Ziel": end_index,
        "Hoechster Punkt": highest_index,
        "Tiefster Punkt": lowest_index,
    }

    for name, index in points.items():
        latitude = route_data["lat"].iloc[index]
        longitude = route_data["lon"].iloc[index]

        location = reverse_geocode(latitude, longitude)
        logging.info(f"{name}: {location}")
        print(f"{name}: {location}")

        time.sleep(1)


def main():
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s: %(message)s",
        level=logging.INFO,
        filename="app.log",
        encoding="utf-8",
    )
    logging.info("Reverse Geocoding gestartet.")

    file_path = "data/final_project_input_data.csv"
    describe_route(file_path)

    logging.info("Reverse Geocoding abgeschlossen.")


if __name__ == "__main__":
    main()