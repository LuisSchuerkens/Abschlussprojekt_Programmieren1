from pathlib import Path
import math
import pandas as pd

def load_gps_data(file_path: str) -> pd.DataFrame:
    """
    Lädt GPS-Daten aus einer CSV-Datei und bereitet sie für die Simulation vor.

    Parameters
    ----------
    file_path : str
        Pfad zur CSV-Datei.

    Returns
    -------
    pd.DataFrame
        Vorbereitete GPS-Daten.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden: {file_path}")

    gps_data = pd.read_csv(path, sep=";")

    # Spaltennamen bereinigen, falls Leerzeichen oder Sonderzeichen enthalten sind
    gps_data.columns = gps_data.columns.str.strip()
    gps_data.columns = gps_data.columns.str.replace("\ufeff", "")

    print("Erkannte Spalten:")
    print(gps_data.columns.tolist())

    required_columns = ["lat", "lon", "ele", "time", "temperature"]

    for column in required_columns:
        if column not in gps_data.columns:
            raise ValueError(f"Die Spalte '{column}' fehlt in der CSV-Datei.")

    gps_data["time"] = pd.to_datetime(gps_data["time"])

    numeric_columns = ["lat", "lon", "ele", "temperature"]

    for column in numeric_columns:
        gps_data[column] = pd.to_numeric(gps_data[column], errors="coerce")

    if gps_data[required_columns].isnull().values.any():
        raise ValueError("Die GPS-Daten enthalten leere oder ungültige Werte.")

    gps_data = gps_data.sort_values("time")
    gps_data = gps_data.reset_index(drop=True)

    print("GPS-Daten wurden erfolgreich geladen.")
    print(f"Anzahl der Datenpunkte: {len(gps_data)}")
    print(f"Startzeit: {gps_data['time'].iloc[0]}")
    print(f"Endzeit: {gps_data['time'].iloc[-1]}")

    return gps_data


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Berechnet die Entfernung zwischen zwei GPS-Koordinaten unter Verwendung der Haversine-Formel.

    Parameters
    ----------
    lat1 : float
        Breitengrad des ersten Punktes in Grad.
    lon1 : float
        Längengrad des ersten Punktes in Grad.
    lat2 : float
        Breitengrad des zweiten Punktes in Grad.
    lon2 : float
        Längengrad des zweiten Punktes in Grad.

    Returns
    -------
    float
        Entfernung zwischen den beiden Punkten in Metern.
    """
    R = 6371000  # Erdradius in Metern

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
         )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def add_motion_data(gps_data: pd.DataFrame) -> pd.DataFrame:
    """
    Ergänzt die GPS-Daten um Strecke, Zeitdifferenz, Geschwindigkeit,
    Beschleunigung und Steigung.

    Parameters
    ----------
    gps_data : pd.DataFrame
        Eingelesene GPS-Daten mit lat, lon, ele und time.

    Returns
    -------
    pd.DataFrame
        GPS-Daten mit zusätzlichen berechneten Spalten.
    """
    gps_data = gps_data.copy()

    distances = [0.0]
    time_differences = [0.0]
    speeds = [0.0]
    accelerations = [0.0]
    slopes = [0.0]

    for i in range(1, len(gps_data)):
        lat1 = gps_data.loc[i - 1, "lat"]
        lon1 = gps_data.loc[i - 1, "lon"]
        lat2 = gps_data.loc[i, "lat"]
        lon2 = gps_data.loc[i, "lon"]

        distance = calculate_distance(lat1, lon1, lat2, lon2)
        distances.append(distance)

        time_difference = (gps_data.loc[i, "time"] - gps_data.loc[i - 1, "time"]).total_seconds()
        time_differences.append(time_difference)

        if time_difference > 0:
            speed = distance / time_difference
        else:
            speed = 0.0

        speeds.append(speed)

        if time_difference > 0:
            acceleration = (speed - speeds[i - 1]) / time_difference
        else:
            acceleration = 0.0

        accelerations.append(acceleration)

        elevation_difference = gps_data.loc[i, "ele"] - gps_data.loc[i - 1, "ele"]

        if distance > 0:
            slope = elevation_difference / distance
        else:
            slope = 0.0

        slopes.append(slope)

    gps_data["distance_m"] = distances
    gps_data["time_diff_s"] = time_differences
    gps_data["speed_m_s"] = speeds
    gps_data["speed_km_h"] = gps_data["speed_m_s"] * 3.6
    gps_data["acceleration_m_s2"] = accelerations
    gps_data["slope"] = slopes
    gps_data["slope_percent"] = gps_data["slope"] * 100
    gps_data["total_distance_m"] = gps_data["distance_m"].cumsum()

    print("Bewegungsdaten wurden berechnet.")
    print(f"Gesamtstrecke: {gps_data['total_distance_m'].iloc[-1] / 1000:.2f} km")
    print(f"Maximale Geschwindigkeit: {gps_data['speed_km_h'].max():.2f} km/h")
    print(f"Maximale Steigung: {gps_data['slope_percent'].max():.2f} %")

    return gps_data