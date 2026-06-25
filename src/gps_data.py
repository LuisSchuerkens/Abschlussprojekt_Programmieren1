from pathlib import Path
import pandas as pd


def load_gps_data(file_path: str) -> pd.DataFrame:
    """
    Lädt GPS-Daten aus CSV-Datei.

    Parameter
    ----------
    file_path : str
        Pfad zur CSV-Datei.

    Returns
    -------
    pd.DataFrame
        Eingelesene GPS-Daten.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden: {file_path}")

    gps_data = pd.read_csv(path)

    print("GPS-Daten wurden erfolgreich geladen.")
    print(f"Anzahl der Datenpunkte: {len(gps_data)}")
    print("Vorhandene Spalten:")
    print(gps_data.columns.tolist())

    return gps_data