from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass
class FluidProperties:
    """Свойства теплоносителя при определенной температуре."""
    name: str
    density: float             # кг/м³
    heat_capacity: float       # Дж/(кг·К)
    viscosity: float           # Па·с
    thermal_conductivity: float # Вт/(м·К)
    min_temp: float           # минимальная допустимая температура, °C
    max_temp: float           # максимальная допустимая температура, °C


@dataclass
class HeatExchangerInput:
    """Входные параметры для расчета теплообменника."""
    heated_fluid: str
    cooled_fluid: str
    G1: float                  # кг/с - производительность по нагреваемой среде
    t1_in: float               # °C - начальная температура нагреваемой среды
    t1_out: float              # °C - конечная температура нагреваемой среды
    P1_in: float               # Па - давление на входе
    delta_P_allowable: float   # Па - допустимые потери давления
    t2_in: Optional[float] = None
    t2_out: Optional[float] = None


@dataclass
class TheoreticalResults:
    """Результаты теоретического технологического расчета."""
    t1_avg: float
    t2_avg: float
    t2_in: float
    t2_out: float
    delta_t_log: float
    heat_load: float
    G2: float
    F_approx: float
    n_z: List[Tuple[float, float, int]]
    heated_properties: Dict[str, float]
    cooled_properties: Dict[str, float]


@dataclass
class StandardHeatExchanger:
    """Параметры стандартных кожухотрубчатых теплообменников."""
    diameter: float                   # Диаметр кожуха, мм
    tube_size: str                    # Размер труб (например, "20x2")
    n_passes: int                     # Число ходов
    n_tubes: int                      # Число труб
    surface_areas: Dict[float, float] # {длина [м]: площадь поверхности [м²]}
    flow_area_shell: float            # Сечение в межтрубном пространстве (10⁻² м²)
    flow_area_tube: float             # Сечение в трубах (10⁻² м²)