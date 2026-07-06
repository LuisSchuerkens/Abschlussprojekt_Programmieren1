import logging
from abc import ABC, abstractmethod

import numpy as np


class BatteryBase(ABC):
    """
    Basisklasse für einen Akku.
    Jeder Akkutyp liefert seine Spannungskennlinie.
    """

    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float,
        initial_soc: float = 1.0,
    ):
        if capacity_nom_Ah <= 0:
            raise ValueError("Battery capacity has to be > 0")

        self.c_nom = capacity_nom_Ah * 3600
        self.R_int = internal_resistance_mOhm / 1000
        self.soc = max(0.0, min(initial_soc, 1.0))

    @abstractmethod
    def ocv_curve(self) -> tuple[list[float], list[float]]:
        """Gibt die Kennlinie als (soc_points, voltage_points) zurück."""
        ...

    def apply_current(self, current: float, duration: float) -> float:
        if duration < 0:
            raise ValueError("Duration must not be negative")

        self.soc = self.soc - ((current * duration) / self.c_nom)
        self.soc = max(0.0, min(self.soc, 1.0))

        return self.soc

    def is_empty(self) -> bool:
        return self.soc <= 0

    def is_full(self) -> bool:
        return self.soc >= 1

    def open_circuit_voltage(self) -> float:
        soc_points, voltage_points = self.ocv_curve()
        return float(np.interp(self.soc, soc_points, voltage_points))

    def voltage(self, current: float = 0.0) -> float:
        return self.open_circuit_voltage() - (self.R_int * current)

    def __str__(self):
        return f"{type(self).__name__}(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"


class LipoBattery(BatteryBase):
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        super().__init__(
            capacity_nom_Ah=capacity_nom_Ah,
            internal_resistance_mOhm=80.0,
            initial_soc=initial_soc,
        )

    def ocv_curve(self) -> tuple[list[float], list[float]]:
        soc_points = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26,
                      0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        voltage_points = [32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81,
                          39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42.00]
        return soc_points, voltage_points


class NmcBattery(BatteryBase):
    def __init__(self, capacity_nom_Ah: float, initial_soc: float = 1.0):
        super().__init__(
            capacity_nom_Ah=capacity_nom_Ah,
            internal_resistance_mOhm=70.0,
            initial_soc=initial_soc,
        )

    def ocv_curve(self) -> tuple[list[float], list[float]]:
        soc_points = [0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26,
                      0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00]
        voltage_points = [32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.39,
                          35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00]
        return soc_points, voltage_points