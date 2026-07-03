# Abschlussprojekt_Programmieren1 - E-Bike Simulation

Dieses Projekt simuliert eine E-Bike-Fahrt auf Basis von GPS-Daten. Aus den GPS-Daten werden Bewegungsdaten, Fahrzeugdaten, Leistungswerte und Akkudaten berechnet. Zusätzlich werden verschiedene Diagramme zur Auswertung der Route und der Akku-Simulation erstellt.

## Projektinhalt

Die Anwendung liest eine CSV-Datei mit GPS-Daten ein und berechnet daraus:

* zurückgelegte Strecke
* Geschwindigkeit
* Beschleunigung
* Steigung
* benötigte Leistung
* Drehmoment am Motor
* Motorstrom
* Ladezustand verschiedener Akkutypen
* Durchschnittsgeschwindigkeit
* benötigte Zeit
* Höhenmeter im Anstieg und Abstieg

Für die Akku-Simulation werden zwei verschiedene Akkutypen betrachtet:

* LiPo-Akku
* NMC-Akku

Die Akkus unterscheiden sich durch ihre Spannungskennlinien und ihren Innenwiderstand.

## Projektstruktur

```text
.
├── data/
│   └── final_project_input_data.csv
├── src/
│   ├── main.py
│   ├── gps_data.py
│   ├── vehicle.py
│   ├── battery_pack.py
│   ├── battery_simulator.py
│   └── plots.py
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Zuerst muss das Repository lokal geklont werden:

```bash
git clone https://github.com/LuisSchuerkens/Abschlussprojekt_Programmieren1.git
cd Abschlussprojekt_Programmieren1
```

Danach wird ein virtuelles Environment erstellt:

```bash
python -m venv .venv
```

Unter Windows in Git Bash wird das Environment so aktiviert:

​```bash
source .venv/Scripts/activate
​```

Unter Windows in PowerShell oder cmd:

​```bash
.venv\Scripts\activate
​```

Anschließend werden die benötigten Pakete installiert:

```bash
pip install -r requirements.txt
```

## Ausführung

Das Programm wird aus dem Hauptordner des Projekts gestartet:

```bash
python src/main.py
```

Wichtig ist, dass die Datei

```text
data/final_project_input_data.csv
```

vorhanden ist.

## Eingabedaten

Die CSV-Datei enthält GPS-Daten mit folgenden Spalten:

```text
lat, lon, ele, time, temperature
```

Diese Daten werden eingelesen, zeitlich sortiert und anschließend für die Simulation vorbereitet.

## Berechnungen

### GPS- und Bewegungsdaten

Aus den GPS-Daten werden die Distanzen zwischen den einzelnen Punkten berechnet. Daraus ergeben sich Geschwindigkeit, Beschleunigung und Steigung.

Da GPS-Daten einzelne Ausreißer enthalten können, wird die berechnete Beschleunigung für die weitere Simulation auf einen plausiblen Bereich begrenzt (von `-3 m/s^2` bis `+3 m/s^2`). Der ursprüngliche Rohwert bleibt zusätzlich erhalten.

### Fahrzeugmodell

Aus Geschwindigkeit, Beschleunigung und Steigung wird die notwendige Antriebskraft berechnet. Daraus werden anschließend Leistung, Drehmoment und Motorstrom bestimmt.

Verwendete Fahrzeugparameter:

```text
Fahrermasse: 70 kg
Fahrradmasse: 10 kg
cW * A: 0.5625 m²
Raddurchmesser: 27 inch
Motorkonstante: 1.5 Nm/A
```

### Akku-Simulation

Für die Akku-Simulation werden zwei Akkutypen mit unterschiedlichen Spannungskennlinien verwendet:

* LiPo
* NMC

Der Akku-Strom wird aus der benötigten Leistung und der aktuellen Akkuspannung berechnet. Dadurch ergeben sich unterschiedliche Spannungs- und Ladezustandsverläufe für LiPo und NMC.

#### Verwendete Akkukapazität

Für die finale Simulation wurde für beide Akkutypen eine Akkukapazität von `35 Ah` verwendet.

Zunächst wurde das Modell mit einer Akkukapazität von `10 Ah` getestet. Diese Kapazität reichte für die simulierte Route jedoch nicht aus, da der Ladezustand am Ende der Fahrt auf `0 %` fiel.

Für die weitere Simulation wurde daher eine größere Akkukapazität von `35 Ah` gewählt. Dadurch bleibt bei beiden Akkutypen eine ausreichende Reserve erhalten und die Entwicklung des Ladezustands über die gesamte Fahrt kann sinnvoll dargestellt werden.

Die beiden simulierten Akkutypen LiPo und NMC verwenden dieselbe Kapazität und denselben Start-Ladezustand, unterscheiden sich jedoch durch ihre Spannungskennlinien und ihren Innenwiderstand. Dadurch ergeben sich unterschiedliche Spannungs- und Ladezustandsverläufe.

## Logging

Das Projekt verwendet das Python-Modul `logging`, um wichtige Programmschritte zu protokollieren. Die Log-Ausgaben werden in der Datei `app.log` gespeichert.

Die Log-Datei wird nicht versioniert, da sie bei jeder Ausführung neu erzeugt wird. Deshalb werden Log-Dateien über `.gitignore` ausgeschlossen:

```text
*.log
```

Beim Ausführen des Programms werden zentrale Kennwerte in die log-Datei geschrieben:

* Gesamtstrecke
* maximale Geschwindigkeit
* maximale Steigung
* maximale Leistung
* maximaler Motorstrom
* End-Ladezustand der beiden Akkus
* minimale Akkuspannung
* Durchschnittsgeschwindigkeit
* benötigte Zeit
* Höhenmeter im Anstieg und Abstieg

Zusätzlich werden Diagramme erzeugt und angezeigt (jeweils in Abhängigkeit der Strecke):

* Höhenprofil
* Geschwindigkeitsprofil
* Leistungsprofil
* Ladezustand der Akkus
* Akkuspannung der Akkus

## Verwendete Pakete

Die benötigten Python-Pakete sind in `requirements.txt` gespeichert.
