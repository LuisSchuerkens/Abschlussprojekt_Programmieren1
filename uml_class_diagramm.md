# UML-Klassendiagramm der Akku-Struktur

Das folgende Klassendiagramm zeigt die objektorientierte Struktur der
Akku-Simulation. Die abstrakte Basisklasse `BatteryBase` enthält die gemeinsame
Logik, die beiden konkreten Akkutypen `LipoBattery` und `NmcBattery` liefern über
`ocv_curve()` ihre jeweilige Spannungskennlinie.

```mermaid
classDiagram
    class BatteryBase {
        <<abstract>>
        +float c_nom
        +float R_int
        +float soc
        +ocv_curve() tuple*
        +apply_current(current, duration) float
        +is_empty() bool
        +is_full() bool
        +open_circuit_voltage() float
        +voltage(current) float
    }
    class LipoBattery {
        +ocv_curve() tuple
    }
    class NmcBattery {
        +ocv_curve() tuple
    }
    class BatterySimulator {
        +BatteryBase battery
        +list soc_profile
        +list voltage_profile
        +list current_profile
        +simulate(current_profile, duration_profile)
        +simulate_power(power_profile, duration_profile)
    }
    BatteryBase <|-- LipoBattery
    BatteryBase <|-- NmcBattery
    BatterySimulator --> BatteryBase : nutzt
```

## Erläuterung

`BatteryBase` ist als abstrakte Basisklasse (ABC) umgesetzt und kann nicht direkt
instanziert werden. Die Methode `ocv_curve()` ist abstrakt (mit `*` markiert) und
muss von jeder Unterklasse implementiert werden.

`LipoBattery` und `NmcBattery` erben die gesamte Berechnungslogik (Ladezustand,
Spannung unter Last, Grenzwertprüfung) und unterscheiden sich nur durch ihre
Kennlinie und ihren Innenwiderstand.

`BatterySimulator` arbeitet ausschließlich mit dem Typ `BatteryBase` und kann
dadurch beide Akkutypen identisch simulieren (Polymorphismus).