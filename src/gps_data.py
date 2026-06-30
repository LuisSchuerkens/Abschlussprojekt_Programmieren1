from pathlib import Path
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