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
│   ├── main.py                    # Hauptsimulation
│   ├── gps_data.py                # GPS-Daten einlesen und auswerten
│   ├── vehicle.py                 # Fahrzeugmodell (Kräfte, Leistung, Motorstrom)
│   ├── battery_pack.py            # Akku-Klassen (BatteryBase, LipoBattery, NmcBattery)
│   ├── battery_simulator.py       # Simulation des Ladezustands
│   ├── plots.py                   # Diagramme und Routenkarte
│   ├── parameter_study.py         # Parameterstudien
│   ├── battery_temperature.py     # Simulation der Akkutemperatur
│   ├── brake_resistance.py        # Simulation des Bremswiderstands
│   ├── geocoding.py               # Reverse Geocoding der Route
│   └── weather.py                 # Wetterdaten und Windeinfluss
├── tests/
│   ├── test_battery.py
│   └── test_gps_data.py
├── results/                       # erzeugte Diagramme und Karte
├── activity_diagramm.md
├── uml_class_diagramm.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Aktivitätsdiagramm

Der vollständige Ablauf der Simulation ist im Aktivitätsdiagramm in
[activity_diagramm.md](activity_diagramm.md) dargestellt.

## UML-Klassendiagramm

Die objektorientierte Struktur der Akku-Simulation ist im UML-Klassendiagramm in
[uml_class_diagramm.md](uml_class_diagramm.md) dargestellt.

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

```bash
source .venv/Scripts/activate
```

Unter Windows in PowerShell oder cmd:

```bash
.venv\Scripts\activate
```

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

Zusätzlich zur Hauptsimulation können die Erweiterungen einzeln ausgeführt werden:

```bash
python src/parameter_study.py
python src/battery_temperature.py
python src/brake_resistance.py
python src/geocoding.py
python src/weather.py
```

Die Skripte `geocoding.py` und `weather.py` benötigen eine Internetverbindung. Sie sind so umgesetzt, dass sie ohne Internet nicht abstürzen, sondern eine entsprechende Meldung ausgeben. Die Hauptsimulation `main.py` läuft immer ohne Internetverbindung.

## Eingabedaten

Die CSV-Datei enthält GPS-Daten mit folgenden Spalten:

```text
lat, lon, ele, time, temperature
```

Diese Daten werden eingelesen, zeitlich sortiert und anschließend für die Simulation vorbereitet.

## Berechnungen

### GPS- und Bewegungsdaten

Aus den GPS-Daten werden die Distanzen zwischen den einzelnen Punkten mit der
Haversine-Formel berechnet. Daraus ergeben sich Geschwindigkeit, Beschleunigung und Steigung.

Da GPS-Daten einzelne Ausreißer enthalten können, wird die berechnete Beschleunigung für die weitere Simulation auf einen plausiblen Bereich begrenzt (von `-3 m/s^2` bis `+3 m/s^2`). Der ursprüngliche Rohwert bleibt zusätzlich erhalten.

### Fahrzeugmodell

Aus Geschwindigkeit, Beschleunigung und Steigung wird die notwendige Antriebskraft berechnet. Daraus werden anschließend Leistung, Drehmoment und Motorstrom bestimmt.

Berücksichtigt werden:

* Luftwiderstand `F_luft = 0.5 * rho * cW*A * v^2`
* Hangabtriebskraft `F_steigung = m * g * sin(phi)`
* Rollwiderstand `F_roll = c_rr * m * g * cos(phi)`
* Beschleunigungskraft `F_beschl = m * a`

Verwendete Fahrzeugparameter:

```text
Fahrermasse: 70 kg
Fahrradmasse: 10 kg
cW * A: 0.5625 m²
Raddurchmesser: 27 inch
Motorkonstante: 1.5 Nm/A
Rollwiderstandsbeiwert: 0.008
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

## Ergebnisse der Fahrt

Die wichtigsten Kennwerte der simulierten Fahrt:

```text
Zurückgelegte Strecke: 94.27 km
Benötigte Zeit: 4.55 h
Durchschnittsgeschwindigkeit: 20.73 km/h
Maximale Geschwindigkeit: 48.77 km/h
Höhenmeter Anstieg: 1096 m
Höhenmeter Abstieg: 1097 m
Maximale Leistung: 2703 W
Maximaler Motorstrom: 64.58 A
End-Ladezustand LiPo: 48.91 %
End-Ladezustand NMC: 47.18 %
```

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

## Fehlerbehandlung

Die Simulation ist an mehreren Stellen gegen ungültige Werte abgesichert:

* Der Ladezustand kann nicht unter `0 %` fallen oder über `100 %` steigen
* Eine Akkukapazität von `0` oder kleiner wird abgelehnt
* Negative Zeitschritte werden abgelehnt
* Fehlende oder ungültige Werte in der CSV-Datei führen zu einer Fehlermeldung
* Zeitschritte von `0` werden abgefangen, damit es keine Division durch null gibt.
* Die API-Aufrufe (Geocoding, Wetterdaten) sind mit `try/except` abgesichert.

## Umgesetzte Erweiterungen

Zusätzlich zu den Minimalanforderungen wurden folgende Erweiterungen umgesetzt:

### Diverse Diagramme

Neben den Standard-Diagrammen wird ein farbcodiertes Höhenprofil erstellt, bei dem
die Steigung farblich dargestellt wird (rot = bergauf, blau = bergab).
Siehe `results/hoehenprofil_steigung.png`.

Erzeugt werden insgesamt (jeweils über der Strecke):

* Höhenprofil (`results/hoehenprofil.png`)
* Höhenprofil mit Steigung (`results/hoehenprofil_steigung.png`)
* Geschwindigkeitsprofil (`results/geschwindigkeit.png`)
* Leistungsprofil (`results/leistung.png`)
* Ladezustand der Akkus (`results/akku_soc.png`)
* Akkuspannung der Akkus (`results/akku_spannung.png`)
* interaktive Routenkarte (`results/route_karte.html`, im Browser zu öffnen)

### Conventional Commits

Alle Commit-Messages im Repository folgen dem Konzept der Conventional Commits
(`feat`, `fix`, `docs`, `test`, `refactor`), um die Nachvollziehbarkeit der
Entwicklung zu gewährleisten.

### Routenkarte

Die gefahrene Route wird mit dem Paket `folium` auf einer interaktiven
OpenStreetMap-Karte dargestellt (`results/route_karte.html`). Die Marker für
Start/Ziel und den höchsten Punkt sind mit den Ortsnamen aus dem Reverse
Geocoding beschriftet.

### Unit-Tests

Für die Haversine-Distanzberechnung und die Akku-Klassen existieren 14 Unit-Tests
(Modul `unittest`). Getestet wird unter anderem die geforderte Fehlerbehandlung:
der Ladezustand kann nicht unter 0 % oder über 100 % fallen. Ausführen mit:

```bash
python -m unittest discover -s tests -v
```

### Parameterstudien

Mit `src/parameter_study.py` wird der Einfluss von zwei Parametern auf den
Akku-Ladezustand untersucht:

* Fahrermasse (60 / 70 / 85 kg) → `results/parameterstudie_masse.png`
* Luftwiderstandsbeiwert cW*A (0.4 / 0.5625 / 0.7) → `results/parameterstudie_cwa.png`

Erwartungsgemäß entlädt sich der Akku bei höherer Masse und bei höherem
Luftwiderstand schneller. Der Reifendurchmesser wurde bewusst nicht variiert, da
er in diesem Modell nur Drehmoment und Motorstrom beeinflusst, nicht aber die
Antriebsleistung und damit den Ladezustand.

### UML-Klassendiagramm

Die objektorientierte Struktur der Akku-Simulation (abstrakte Basisklasse
`BatteryBase` mit den Unterklassen `LipoBattery` und `NmcBattery`) ist in
[uml_class_diagramm.md](uml_class_diagramm.md) dokumentiert.

### Luftdichte aus Temperatur und Höhe

Die Luftdichte wird nicht pauschal angenommen, sondern für jeden Datenpunkt aus
Höhe und Temperatur berechnet. Der Luftdruck folgt aus der barometrischen
Höhenformel, die Dichte aus der idealen Gasgleichung:

```text
p = p0 * (1 - 0.0065 * h / 288.15)^5.255
rho = p / (R_s * T)     mit R_s = 287.05 J/(kg*K)
```

Auf der simulierten Route liegt die Luftdichte zwischen etwa `1.05` und
`1.12 kg/m³` und damit deutlich unter dem oft verwendeten Standardwert von
`1.23 kg/m³`. Die Temperaturspalte der Eingangsdaten wird dadurch genutzt.

### Rollwiderstand

Das Fahrzeugmodell berücksichtigt den Rollwiderstand
`F_roll = c_rr * m * g * cos(phi)` mit einem Rollwiderstandsbeiwert von `0.008`
(typischer Wert für Fahrradreifen auf Asphalt). Der Rollwiderstand wirkt über die
gesamte Fahrt und senkt den End-Ladezustand deutlich.

### Simulation der Akkutemperatur

`src/battery_temperature.py` enthält die Klasse `ThermalBattery`, die von
`LipoBattery` erbt. Die Akkutemperatur steigt durch die ohmschen Verluste
(`I² * R`) und sinkt durch Kühlung Richtung Umgebungstemperatur. Über die Fahrt
erwärmt sich der Akku von `28 °C` auf etwa `31.4 °C`.
Ergebnis: `results/akku_temperatur.png`.

### Simulation eines Bremswiderstands

`src/brake_resistance.py` bildet die Rekuperation beim Bergabfahren ab. Der Akku
kann nur bis zu einem maximalen Ladestrom von `10 A` aufnehmen, die überschüssige
Energie wird in einem Bremswiderstand dissipiert. Über die Fahrt werden etwa
`131 kJ` rekuperiert und `19 kJ` im Bremswiderstand in Wärme umgewandelt.
Ergebnis: `results/bremswiderstand.png`.

### Reverse Geocoding

`src/geocoding.py` wandelt die GPS-Koordinaten der markanten Punkte (Start, Ziel,
höchster und tiefster Punkt) über die Nominatim-API von OpenStreetMap in
Ortsnamen um. Die Ortsnamen werden zusätzlich als Beschriftung der Marker auf der
Routenkarte dargestellt.

### Wetterdaten und Windeinfluss

`src/weather.py` holt über die Open-Meteo-Archiv-API die realen Winddaten für den
Fahrttag und rechnet die Fahrt mit Windkomponente nach. Der Wind wirkt nur
entlang der Fahrtrichtung, die über den Kurswinkel aus den GPS-Daten bestimmt
wird. Da es sich um einen Rundkurs handelt, gleichen sich Gegen- und Rückenwind
teilweise aus, der Effekt ist entsprechend moderat.
Ergebnis: `results/wind_einfluss.png`.

### Bestimmung der Himmelsrichtung

Aus je zwei aufeinanderfolgenden GPS-Punkten wird der Kurswinkel (Bearing)
berechnet und einer der acht Himmelsrichtungen (N, NO, O, SO, S, SW, W, NW)
zugeordnet. Die Werte stehen in den Spalten `bearing` und `compass` und werden
für die Windberechnung verwendet.

## Verwendete Annahmen

Nicht alle Modellparameter sind in der Aufgabenstellung vorgegeben. Für die
Erweiterungen wurden folgende Werte als begründete Annahmen gewählt und im
Code als Konstanten hinterlegt:

 Parameter | Wert 
 
 Rollwiderstandsbeiwert `c_rr` | 0.008 
 
 Wärmekapazität / Kühlkoeffizient des Akkus | 1200 J/K / 0.8 W/K 
 
 Umgebungstemperatur | 28 °C 
 
 Maximaler Ladestrom (Rekuperation) | 10 A 
 
 Akkukapazität | 35 Ah 
 
 Parameterstudien | 60/70/85 kg, cW*A 0.4/0.5625/0.7 

Für den fiktiven Akku liegt kein Datenblatt vor, daher sind die thermischen
Werte und der Ladestrom vereinfachte Annahmen. Die Erweiterungen zeigen deshalb
qualitative Tendenzen, keine exakten Vorhersagen.

## Quellen

### Aufgabenstellung und Kursunterlagen

* MCI-MECH-B-2-PRO1-PRO1-ILV, Foliensatz "Abschlussprojekt SS 2026":
  Haversine-Formel zur Streckenberechnung, Freikörperdiagramm und
  Luftwiderstandskraft, Zusammenhang von Antriebskraft, Drehmoment und
  Motorstrom, alle Fahrzeugparameter (Massen, cW*A, Raddurchmesser,
  Motorkonstante), Aufbau und OCV-Kennlinien der beiden Akkutypen sowie Foliensätze zur objektorientierten Programmierung, Aufbau des UML- und Klassendiagramm und zu git

### Physikalische Standardformeln

Standardformeln aus der Physik/Thermodynamik :

* Barometrische Höhenformel zur Bestimmung des Luftdrucks über der Höhe,
  in der Form der ISA-Normatmosphäre (ICAO-Standardatmosphäre) mit
  Temperaturgradient 0.0065 K/m und Bezugstemperatur 288.15 K
* Ideale Gasgleichung in der Form rho = p / (R_s * T) mit der spezifischen
  Gaskonstante für trockene Luft R_s = 287.05 J/(kg*K)
* Rollwiderstandskraft F_roll = c_rr * m * g * cos(phi)
* Joulesche Wärme Q = I^2 * R * t für die Verlustleistung im Innenwiderstand
* Newtonsches Abkühlungsgesetz für die Wärmeabgabe an die Umgebung
* Berechnung des Kurswinkels (Bearing) zwischen zwei Punkten auf der
  Kugeloberfläche mittels sphärischer Trigonometrie

### Verwendete APIs

* Nominatim (OpenStreetMap) für das Reverse Geocoding:
  https://nominatim.openstreetmap.org — 
* Open-Meteo Archiv-API für die historischen Wetterdaten des Fahrttages:
  https://archive-api.open-meteo.com

### Verwendete Pakete und deren Dokumentation

* pandas: https://pandas.pydata.org/docs/
* matplotlib: https://matplotlib.org/stable/
* numpy: https://numpy.org/doc/
* folium: https://python-visualization.github.io/folium/
* unittest (Python-Standardbibliothek): https://docs.python.org/3/library/unittest.html

(Zusätzliche werden Module aus der Python-Standartbibliothek verwendet Diese müssen nicht separat installiert werden.

### Werkzeuge

* Diagramme (Aktivitäts- und Klassendiagramm) erstellt mit Mermaid:
  https://mermaid.js.org
* Conventional Commits: https://www.conventionalcommits.org
