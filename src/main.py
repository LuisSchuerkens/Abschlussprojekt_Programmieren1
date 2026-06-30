from gps_data import load_gps_data


def main():
    """Hauptfunktion des Programms."""
    print("E-Bike Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"
    gps_data = load_gps_data(file_path)

    print("Kontrollausgabe der ersten fünf GPS-Datenpunkte:")
    print(gps_data.head())


if __name__ == "__main__":
    main()