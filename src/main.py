import gps_data

def main():
    """Hauptfunktion des Programms."""
    print("E-Bike Simulation gestartet.")

    file_path = "data/final_project_input_data.csv"
    route_data = gps_data.load_gps_data(file_path)
    route_data = gps_data.add_motion_data(route_data)

    print("Kontrollausgabe der ersten fünf GPS-Datenpunkte:")
    print(route_data.head())


if __name__ == "__main__":
    main()