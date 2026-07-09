import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from battery_pack import LipoBattery, NmcBattery


class TestBattery(unittest.TestCase):
    def test_full_at_start(self):
        battery = LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        self.assertTrue(battery.is_full())

    def test_discharge_lowers_soc(self):
        battery = LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        battery.apply_current(10.0, 60.0)
        self.assertLess(battery.soc, 1.0)

    def test_soc_not_below_zero(self):
        battery = LipoBattery(capacity_nom_Ah=1.0, initial_soc=0.1)
        battery.apply_current(1000.0, 3600.0)
        self.assertEqual(battery.soc, 0.0)
        self.assertTrue(battery.is_empty())

    def test_soc_not_above_one(self):
        battery = LipoBattery(capacity_nom_Ah=1.0, initial_soc=0.9)
        battery.apply_current(-1000.0, 3600.0)
        self.assertEqual(battery.soc, 1.0)
        self.assertTrue(battery.is_full())

    def test_invalid_capacity_raises(self):
        with self.assertRaises(ValueError):
            LipoBattery(capacity_nom_Ah=0.0)

    def test_negative_duration_raises(self):
        battery = LipoBattery(capacity_nom_Ah=35.0)
        with self.assertRaises(ValueError):
            battery.apply_current(10.0, -5.0)

    def test_full_voltage(self):
        lipo = LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        self.assertAlmostEqual(lipo.open_circuit_voltage(), 42.0, places=2)

    def test_empty_voltage(self):
        lipo = LipoBattery(capacity_nom_Ah=35.0, initial_soc=0.0)
        self.assertAlmostEqual(lipo.open_circuit_voltage(), 32.0, places=2)

    def test_voltage_drops_under_load(self):
        battery = LipoBattery(capacity_nom_Ah=35.0, initial_soc=1.0)
        self.assertLess(battery.voltage(10.0), battery.open_circuit_voltage())

    def test_lipo_and_nmc_differ(self):
        lipo = LipoBattery(capacity_nom_Ah=35.0, initial_soc=0.5)
        nmc = NmcBattery(capacity_nom_Ah=35.0, initial_soc=0.5)
        self.assertNotEqual(lipo.open_circuit_voltage(), nmc.open_circuit_voltage())


if __name__ == "__main__":
    unittest.main()