from gps_data import load_gps_data

def main():
    """Hauptfunktion des Programms."""
    print("E-Bike Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"
    gps_data = load_gps_data(file_path)

    """für Kontrolle, ob die Daten eingelesen wurden"""
    print("Erste fünf Zeilen der GPS-Daten:")
    print(gps_data.head())


if __name__ == "__main__":
    main()