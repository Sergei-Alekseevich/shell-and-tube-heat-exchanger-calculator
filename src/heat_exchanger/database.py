from typing import Dict, Any, List
from .models import FluidProperties, StandardHeatExchanger

FLUIDS_DB: Dict[str, Dict[str, Any]] = {
    "Гептан": {
        "props": [
            FluidProperties(name="Гептан", density=684.4, heat_capacity=2180, viscosity=450e-6, thermal_conductivity=125e-3, min_temp=-90.6, max_temp=98.4),
            FluidProperties(name="Гептан", density=686.0, heat_capacity=2150, viscosity=406.8e-6, thermal_conductivity=125.0e-3, min_temp=-90.6, max_temp=98.4),
            FluidProperties(name="Гептан", density=642.0, heat_capacity=2410, viscosity=260e-6, thermal_conductivity=109e-3, min_temp=-90.6, max_temp=98.4),
        ],
        "temps": [-50, 20, 70]
    },
    "Вода": {
        "props": [
            FluidProperties(name="Вода", density=999.8, heat_capacity=4190, viscosity=1724e-6, thermal_conductivity=567e-3, min_temp=0, max_temp=100),
            FluidProperties(name="Вода", density=987.8, heat_capacity=4190, viscosity=546.6e-6, thermal_conductivity=637e-3, min_temp=0, max_temp=100),
            FluidProperties(name="Вода", density=957.8, heat_capacity=4230, viscosity=280.6e-6, thermal_conductivity=676e-3, min_temp=0, max_temp=100),
        ],
        "temps": [0, 50, 100]
    },
    "Масло минеральное": {
        "props": [
            FluidProperties(name="Масло минеральное", density=920, heat_capacity=1800, viscosity=1.0, thermal_conductivity=0.13, min_temp=-20, max_temp=200),
            FluidProperties(name="Масло минеральное", density=900, heat_capacity=1880, viscosity=0.1, thermal_conductivity=0.15, min_temp=-20, max_temp=200),
            FluidProperties(name="Масло минеральное", density=880, heat_capacity=1950, viscosity=0.02, thermal_conductivity=0.17, min_temp=-20, max_temp=200),
        ],
        "temps": [0, 100, 200]
    },
    "Этиленгликоль": {
        "props": [
            FluidProperties(name="Этиленгликоль", density=1130, heat_capacity=2300, viscosity=0.026, thermal_conductivity=0.242, min_temp=-12.9, max_temp=197.3),
            FluidProperties(name="Этиленгликоль", density=1113, heat_capacity=2382, viscosity=0.0161, thermal_conductivity=0.258, min_temp=-12.9, max_temp=197.3),
            FluidProperties(name="Этиленгликоль", density=1080, heat_capacity=2500, viscosity=0.008, thermal_conductivity=0.275, min_temp=-12.9, max_temp=197.3),
        ],
        "temps": [0, 50, 150]
    }
}

STANDARD_EXCHANGERS: List[StandardHeatExchanger] = [
    # Диаметр 159 мм
    StandardHeatExchanger(159, "20x2", 1, 19, {1.0: 1.0, 1.5: 2.0, 2.0: 2.5, 3.0: 3.5}, 0.3, 0.4),
    StandardHeatExchanger(159, "25x2", 1, 13, {1.0: 1.0, 1.5: 1.5, 2.0: 2.0, 3.0: 3.0}, 0.4, 0.5),
    # Диаметр 273 мм
    StandardHeatExchanger(273, "20x2", 1, 61, {1.0: 4.0, 1.5: 6.0, 2.0: 7.5, 3.0: 11.5}, 0.7, 1.2),
    StandardHeatExchanger(273, "25x2", 1, 37, {1.0: 3.0, 1.5: 4.5, 2.0: 6.0, 3.0: 9.0}, 0.9, 1.3),
    # Диаметр 325 мм
    StandardHeatExchanger(325, "20x2", 1, 100, {1.5: 9.5, 2.0: 12.5, 3.0: 19.0, 4.0: 25.0}, 1.1, 2.0),
    StandardHeatExchanger(325, "20x2", 2, 90, {1.5: 8.5, 2.0: 11.0, 3.0: 17.0, 4.0: 22.5}, 1.1, 0.9),
    StandardHeatExchanger(325, "25x2", 1, 62, {1.5: 7.5, 2.0: 10.0, 3.0: 14.5, 4.0: 19.5}, 1.3, 2.1),
    StandardHeatExchanger(325, "25x2", 2, 56, {1.5: 6.5, 2.0: 9.0, 3.0: 13.0, 4.0: 17.5}, 1.3, 1.0),
    # Диаметр 400 мм
    StandardHeatExchanger(400, "20x2", 1, 181, {2.0: 23.0, 3.0: 34.0, 4.0: 46.0, 6.0: 68.0}, 1.7, 3.6),
    StandardHeatExchanger(400, "20x2", 2, 166, {2.0: 21.0, 3.0: 31.0, 4.0: 42.0, 6.0: 63.0}, 1.7, 1.7),
    StandardHeatExchanger(400, "25x2", 1, 111, {2.0: 17.0, 3.0: 26.0, 4.0: 35.0, 6.0: 52.0}, 2.0, 3.8),
    StandardHeatExchanger(400, "25x2", 2, 100, {2.0: 16.0, 3.0: 24.0, 4.0: 31.0, 6.0: 47.0}, 2.0, 1.7),
    # Диаметр 600 мм
    StandardHeatExchanger(600, "20x2", 1, 389, {2.0: 49.0, 3.0: 73.0, 4.0: 98.0, 6.0: 147.0}, 4.1, 7.8),
    StandardHeatExchanger(600, "20x2", 2, 370, {2.0: 47.0, 3.0: 70.0, 4.0: 93.0, 6.0: 139.0}, 4.1, 3.7),
    StandardHeatExchanger(600, "20x2", 4, 334, {2.0: 42.0, 3.0: 63.0, 4.0: 84.0, 6.0: 126.0}, 4.1, 1.6),
    StandardHeatExchanger(600, "20x2", 6, 316, {2.0: 40.0, 3.0: 60.0, 4.0: 79.0, 6.0: 119.0}, 3.7, 0.9),
    StandardHeatExchanger(600, "25x2", 1, 257, {2.0: 40.0, 3.0: 61.0, 4.0: 81.0, 6.0: 121.0}, 4.0, 8.9),
    StandardHeatExchanger(600, "25x2", 2, 240, {2.0: 38.0, 3.0: 57.0, 4.0: 75.0, 6.0: 113.0}, 4.0, 4.2),
    StandardHeatExchanger(600, "25x2", 4, 206, {2.0: 32.0, 3.0: 49.0, 4.0: 65.0, 6.0: 97.0}, 4.0, 1.8),
    StandardHeatExchanger(600, "25x2", 6, 196, {2.0: 31.0, 3.0: 46.0, 4.0: 61.0, 6.0: 91.0}, 3.7, 1.1),
    # Диаметр 800 мм
    StandardHeatExchanger(800, "20x2", 1, 717, {3.0: 90.0, 4.0: 135.0, 6.0: 180.0, 9.0: 270.0}, 6.9, 14.4),
    StandardHeatExchanger(800, "20x2", 2, 690, {3.0: 87.0, 4.0: 130.0, 6.0: 173.0, 9.0: 260.0}, 6.9, 6.9),
    StandardHeatExchanger(800, "20x2", 4, 638, {3.0: 80.0, 4.0: 120.0, 6.0: 160.0, 9.0: 240.0}, 6.9, 3.0),
    StandardHeatExchanger(800, "20x2", 6, 618, {3.0: 78.0, 4.0: 116.0, 6.0: 155.0, 9.0: 233.0}, 6.5, 2.0),
    StandardHeatExchanger(800, "25x2", 1, 465, {3.0: 73.0, 4.0: 109.0, 6.0: 146.0, 9.0: 219.0}, 7.0, 16.1),
    StandardHeatExchanger(800, "25x2", 2, 442, {3.0: 69.0, 4.0: 104.0, 6.0: 139.0, 9.0: 208.0}, 7.0, 7.7),
    StandardHeatExchanger(800, "25x2", 4, 404, {3.0: 63.0, 4.0: 95.0, 6.0: 127.0, 9.0: 190.0}, 7.0, 3.0),
    StandardHeatExchanger(800, "25x2", 6, 384, {3.0: 60.0, 4.0: 90.0, 6.0: 121.0, 9.0: 181.0}, 6.5, 2.2),
    # Диаметр 1000 мм
    StandardHeatExchanger(1000, "20x2", 1, 1173, {4.0: 221.0, 6.0: 295.0, 9.0: 442.0}, 10.1, 23.6),
    StandardHeatExchanger(1000, "20x2", 2, 1138, {4.0: 214.0, 6.0: 286.0, 9.0: 429.0}, 10.1, 11.4),
    StandardHeatExchanger(1000, "20x2", 4, 1072, {4.0: 202.0, 6.0: 269.0, 9.0: 404.0}, 10.1, 5.1),
    StandardHeatExchanger(1000, "20x2", 6, 1044, {4.0: 197.0, 6.0: 262.0, 9.0: 393.0}, 9.6, 3.4),
    StandardHeatExchanger(1000, "25x2", 1, 747, {4.0: 176.0, 6.0: 235.0, 9.0: 352.0}, 10.6, 25.9),
    StandardHeatExchanger(1000, "25x2", 2, 718, {4.0: 169.0, 6.0: 226.0, 9.0: 338.0}, 10.6, 12.4),
    StandardHeatExchanger(1000, "25x2", 4, 666, {4.0: 157.0, 6.0: 209.0, 9.0: 314.0}, 10.6, 5.5),
    StandardHeatExchanger(1000, "25x2", 6, 642, {4.0: 151.0, 6.0: 202.0, 9.0: 302.0}, 10.2, 3.6),
    # Диаметр 1200 мм
    StandardHeatExchanger(1200, "20x2", 1, 1701, {6.0: 427.0, 9.0: 641.0}, 14.5, 34.2),
    StandardHeatExchanger(1200, "20x2", 2, 1658, {6.0: 417.0, 9.0: 625.0}, 14.5, 16.5),
    StandardHeatExchanger(1200, "20x2", 4, 1580, {6.0: 397.0, 9.0: 595.0}, 14.5, 7.9),
    StandardHeatExchanger(1200, "20x2", 6, 1544, {6.0: 388.0, 9.0: 582.0}, 13.1, 4.9),
    StandardHeatExchanger(1200, "25x2", 1, 1083, {6.0: 340.0, 9.0: 510.0}, 16.4, 37.5),
    StandardHeatExchanger(1200, "25x2", 2, 1048, {6.0: 329.0, 9.0: 494.0}, 16.4, 17.9),
    StandardHeatExchanger(1200, "25x2", 4, 986, {6.0: 310.0, 9.0: 464.0}, 16.4, 8.4),
    StandardHeatExchanger(1200, "25x2", 6, 958, {6.0: 301.0, 9.0: 451.0}, 14.2, 5.2),
]