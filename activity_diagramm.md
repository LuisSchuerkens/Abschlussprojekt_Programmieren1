# Aktivitätsdiagramm der E-Bike-Simulation

Das folgende Aktivitätsdiagramm zeigt den vollständigen Ablauf der Simulation
von der Programmstartphase bis zur Ausgabe der Ergebnisse.

```mermaid
flowchart TD
    Start([Start]) --> A[GPS-Daten aus CSV laden]
    A --> B{Datei vorhanden<br/>und gültig?}
    B -- Nein --> Err[Fehler protokollieren<br/>und Programm beenden]
    Err --> Ende([Ende])
    B -- Ja --> C[Bewegungsdaten berechnen<br/>Strecke, Zeit, Geschwindigkeit,<br/>Beschleunigung, Steigung]
    C --> D[Fahrzeugdaten berechnen<br/>Kraft, Leistung, Drehmoment,<br/>Motorstrom]
    D --> E[LiPo- und NMC-Akku<br/>initialisieren]
    E --> F[Nächsten Zeitschritt lesen]
    F --> G[Akku-Strom aus Leistung<br/>und Spannung berechnen]
    G --> H[SOC aktualisieren]
    H --> I{SOC im<br/>gültigen Bereich<br/>0 bis 1?}
    I -- Nein --> J[SOC begrenzen<br/>und Warnung loggen]
    J --> K
    I -- Ja --> K[Spannung und Strom<br/>speichern]
    K --> L{Letzter<br/>Zeitschritt?}
    L -- Nein --> F
    L -- Ja --> M[Kenngrößen berechnen<br/>Ø-Speed, Zeit, Höhenmeter]
    M --> N[Ergebnisse loggen]
    N --> O[Diagramme erstellen<br/>und als PNG speichern]
    O --> Ende([Ende])
```

## Erläuterung

Der Ablauf beginnt mit dem Einlesen der GPS-Daten aus der CSV-Datei. Falls die
Datei fehlt oder ungültige Werte enthält, wird der Fehler protokolliert und das
Programm beendet.

Aus den GPS-Daten werden zunächst die Bewegungsdaten berechnet (Strecke,
Geschwindigkeit, Beschleunigung, Steigung). Anschließend wird das Fahrzeugmodell
angewendet, um Kraft, Leistung, Drehmoment und Motorstrom zu bestimmen.

Danach werden die beiden Akkus (LiPo und NMC) initialisiert. Für jeden
Zeitschritt der Fahrt wird der benötigte Akku-Strom aus der Leistung und der
aktuellen Akkuspannung berechnet, der Ladezustand aktualisiert und geprüft, ob
er im gültigen Bereich zwischen 0 und 1 liegt. Verlässt der SOC diesen Bereich,
wird er begrenzt und ein Warnhinweis protokolliert.

Nach Abschluss der Simulation werden die Kenngrößen der gesamten Fahrt
berechnet, in der Log-Datei festgehalten und die Ergebnisdiagramme als PNG-Dateien
im Ordner `results/` gespeichert.