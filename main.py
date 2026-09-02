import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any


@dataclass
class FluidProperties:
    """Класс для хранения свойств теплоносителя"""
    name: str
    density: float  # кг/м3
    heat_capacity: float  # Дж/(кг·К)
    viscosity: float  # Па·с
    thermal_conductivity: float  # Вт/(м·К)
    min_temp: float  # минимальная допустимая температура, °C
    max_temp: float  # максимальная допустимая температура, °C


# База данных теплоносителей с данными для интерполяции (добавлены свойства при разных температурах)
FLUIDS_DB = {
    "Гептан": {
        "props": [
            FluidProperties(name="Гептан", density=684.4, heat_capacity=2180, viscosity=450e-6, thermal_conductivity=125e-3, min_temp=-90.6, max_temp=98.4),  # при -50°C
            FluidProperties(name="Гептан", density=686.0, heat_capacity=2150, viscosity=406.8e-6, thermal_conductivity=125.0e-3, min_temp=-90.6, max_temp=98.4),  # при 20°C
            FluidProperties(name="Гептан", density=642.0, heat_capacity=2410, viscosity=260e-6, thermal_conductivity=109e-3, min_temp=-90.6, max_temp=98.4),  # при 70°C
        ],
        "temps": [-50, 20, 70]  # Температуры, для которых заданы свойства
    },
    "Вода": {
        "props": [
            FluidProperties(name="Вода", density=999.8, heat_capacity=4190, viscosity=1724e-6, thermal_conductivity=567e-3, min_temp=0, max_temp=100),  # при 0°C
            FluidProperties(name="Вода", density=987.8, heat_capacity=4190, viscosity=546.6e-6, thermal_conductivity=637e-3, min_temp=0, max_temp=100),  # при 50°C
            FluidProperties(name="Вода", density=957.8, heat_capacity=4230, viscosity=280.6e-6, thermal_conductivity=676e-3, min_temp=0, max_temp=100),  # при 100°C
        ],
        "temps": [0, 50, 100]
    },
    "Масло минеральное": {
        "props": [
            FluidProperties(name="Масло минеральное", density=920, heat_capacity=1800, viscosity=1.0, thermal_conductivity=0.13, min_temp=-20, max_temp=200),  # при 0°C
            FluidProperties(name="Масло минеральное", density=900, heat_capacity=1880, viscosity=0.1, thermal_conductivity=0.15, min_temp=-20, max_temp=200),  # при 100°C
            FluidProperties(name="Масло минеральное", density=880, heat_capacity=1950, viscosity=0.02, thermal_conductivity=0.17, min_temp=-20, max_temp=200),  # при 200°C
        ],
        "temps": [0, 100, 200]
    },
    "Этиленгликоль": {
        "props": [
            FluidProperties(name="Этиленгликоль", density=1130, heat_capacity=2300, viscosity=0.026, thermal_conductivity=0.242, min_temp=-12.9, max_temp=197.3),  # при 0°C
            FluidProperties(name="Этиленгликоль", density=1113, heat_capacity=2382, viscosity=0.0161, thermal_conductivity=0.258, min_temp=-12.9, max_temp=197.3),  # при 50°C
            FluidProperties(name="Этиленгликоль", density=1080, heat_capacity=2500, viscosity=0.008, thermal_conductivity=0.275, min_temp=-12.9, max_temp=197.3),  # при 150°C
        ],
        "temps": [0, 50, 150]
    }
}


@dataclass
class HeatExchangerInput:
    """Входные данные для расчета теплообменника"""
    heated_fluid: str
    cooled_fluid: str
    G1: float  # кг/с - производительность по нагреваемой среде
    t1_in: float  # °C - начальная температура нагреваемой среды
    t1_out: float  # °C - конечная температура нагреваемой среды
    P1_in: float  # Па - давление на входе в теплообменник
    delta_P_allowable: float  # Па - допустимые потери давления
    t2_in: Optional[float] = None  # °C - начальная температура охлаждаемой среды (рассчитывается)
    t2_out: Optional[float] = None  # °C - конечная температура охлаждаемой среды (рассчитывается)


@dataclass
class TheoreticalResults:
    """Результаты теоретического расчета"""
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


def linear_interpolation(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Линейная интерполяция"""
    return y1 + (y2 - y1) / (x2 - x1) * (x - x1)


def get_interpolated_fluid_properties(fluid_name: str, temperature: float) -> FluidProperties:
    """Получение интерполированных свойств теплоносителя при заданной температуре"""
    if fluid_name not in FLUIDS_DB:
        raise ValueError(f"Теплоноситель {fluid_name} не найден в базе данных")
    
    fluid_data = FLUIDS_DB[fluid_name]
    temps = fluid_data["temps"]
    props_list = fluid_data["props"]
    
    # Если температура ниже минимальной - берем свойства при минимальной температуре
    if temperature <= temps[0]:
        return props_list[0]
    
    # Если температура выше максимальной - берем свойства при максимальной температуре
    if temperature >= temps[-1]:
        return props_list[-1]
    
    # Находим интервал для интерполяции
    for i in range(len(temps) - 1):
        if temps[i] <= temperature <= temps[i+1]:
            # Интерполируем все свойства
            t1, t2 = temps[i], temps[i+1]
            p1, p2 = props_list[i], props_list[i+1]
            
            density = linear_interpolation(temperature, t1, p1.density, t2, p2.density)
            heat_capacity = linear_interpolation(temperature, t1, p1.heat_capacity, t2, p2.heat_capacity)
            viscosity = linear_interpolation(temperature, t1, p1.viscosity, t2, p2.viscosity)
            thermal_conductivity = linear_interpolation(temperature, t1, p1.thermal_conductivity, t2, p2.thermal_conductivity)
            
            return FluidProperties(
                name=fluid_name,
                density=density,
                heat_capacity=heat_capacity,
                viscosity=viscosity,
                thermal_conductivity=thermal_conductivity,
                min_temp=p1.min_temp,
                max_temp=p1.max_temp
            )
    
    # Если не нашли интервал (хотя должны были)
    return props_list[-1]


def get_fluid_properties(fluid_name: str, temperature: float) -> FluidProperties:
    """Получение свойств теплоносителя при заданной температуре (с интерполяцией)"""
    return get_interpolated_fluid_properties(fluid_name, temperature)


def check_temperature_constraints(fluid_name: str, temperature: float) -> None:
    """Проверка допустимости температуры для теплоносителя"""
    props = get_interpolated_fluid_properties(fluid_name, temperature)
    if temperature < props.min_temp or temperature > props.max_temp:
        raise ValueError(
            f"Температура {temperature}°C недопустима для {fluid_name}. "
            f"Допустимый диапазон: {props.min_temp}...{props.max_temp}°C"
        )


def calculate_hot_fluid_temperatures(t1_in: float, t1_out: float, cooled_fluid: str) -> Tuple[float, float]:
    """Определение температур горячего теплоносителя с учетом движущей силы процесса"""
    props = get_interpolated_fluid_properties(cooled_fluid, (t1_in + t1_out)/2)

    # Для воды используем стандартные параметры как в ручном расчете
    if cooled_fluid == "Вода":
        t2_in = 95.0  # Фиксированная температура на входе
        t2_out = 40.0  # Фиксированная температура на выходе
    else:
        # Для других теплоносителей
        if cooled_fluid == "Масло минеральное":
            t2_in = 180.0
        elif cooled_fluid == "Этиленгликоль":
            t2_in = 150.0
        else:
            t2_in = props.max_temp - 5.0

        t2_out = t1_out + 15.0
        t2_out = min(t2_out, props.max_temp - 5.0)
        t2_out = max(t2_out, t1_out + 5.0)

    return t2_in, t2_out


def calculate_theoretical(input_data: HeatExchangerInput) -> TheoreticalResults:
    """Функция теоретического расчета теплообменника"""
    # Проверка температурных ограничений
    check_temperature_constraints(input_data.heated_fluid, input_data.t1_in)
    check_temperature_constraints(input_data.heated_fluid, input_data.t1_out)

    # Проверка, что начальная и конечная температуры нагреваемой среды разные
    if input_data.t1_in == input_data.t1_out:
        raise ValueError(
            f"Ошибка: Начальная и конечная температуры нагреваемой среды не могут быть одинаковыми!\n"
            f"Введенные значения: {input_data.t1_in}°C → {input_data.t1_out}°C\n"
            f"Для теплообмена необходимо, чтобы температура изменялась."
        )

    # Проверка, что конечная температура выше начальной (для нагревателя)
    if input_data.t1_out <= input_data.t1_in:
        raise ValueError(
            f"Ошибка: Для нагревателя конечная температура должна быть БОЛЬШЕ начальной!\n"
            f"Введенные значения: t1_in = {input_data.t1_in}°C, t1_out = {input_data.t1_out}°C\n"
            f"Проверьте введенные данные - аппарат работает как нагреватель, "
            f"поэтому t1_out должно быть > t1_in"
        )

    # Определение температур горячего теплоносителя
    t2_in, t2_out = calculate_hot_fluid_temperatures(
        input_data.t1_in,
        input_data.t1_out,
        input_data.cooled_fluid
    )

    # Проверка температур горячего теплоносителя
    check_temperature_constraints(input_data.cooled_fluid, t2_in)
    check_temperature_constraints(input_data.cooled_fluid, t2_out)

    # 1. Расчет средних температур
    t1_avg = (input_data.t1_in + input_data.t1_out) / 2
    t2_avg = (t2_in + t2_out) / 2

    # 2. Получение свойств теплоносителей (с интерполяцией)
    heated_props = get_fluid_properties(input_data.heated_fluid, t1_avg)
    cooled_props = get_fluid_properties(input_data.cooled_fluid, t2_avg)

    # 3. Расчет температурной схемы (противоток)
    delta_t_b = abs(input_data.t1_out - t2_in)
    delta_t_m = abs(input_data.t1_in - t2_out)

    # 4. Средняя логарифмическая разность температур
    if delta_t_b == delta_t_m:
        delta_t_log = delta_t_b
    elif delta_t_b == 0 or delta_t_m == 0:
        raise ValueError(
            "Нулевая разность температур!\n"
            "Проверьте введенные температуры - возможно, они подобраны так, что разность температур "
            "на одном из концов теплообменника равна нулю.\n"
            f"Δt на горячем конце: {delta_t_b}°C, на холодном конце: {delta_t_m}°C"
        )
    else:
        delta_t_log = (delta_t_b - delta_t_m) / math.log(delta_t_b / delta_t_m)

    # 5. Тепловая нагрузка
    Q = input_data.G1 * heated_props.heat_capacity * (input_data.t1_out - input_data.t1_in)

    # 6. Расход охлаждающей среды (ИСПОЛЬЗУЕМ ΔT_log как вы просили)
    if cooled_props.heat_capacity == 0 or delta_t_log == 0:
        raise ValueError("Нулевая теплоемкость или разность температур")
    G2 = Q / (cooled_props.heat_capacity * (delta_t_log))  # Исправлено по формуле

    # 7. Ориентировочный выбор теплообменника
    Re_approx = 15000
    tube_diameters = [(25e-3, 2e-3), (20e-3, 2e-3)]

    n_z_results = []
    for d_out, wall in tube_diameters:
        d_in = d_out - 2 * wall
        n_z = (4 * input_data.G1) / (math.pi * d_in * Re_approx * heated_props.viscosity)
        n_z_results.append((d_out * 1e3, wall * 1e3, round(n_z)))

    # 8. Ориентировочная поверхность теплообмена
    K_approx = 400
    F_approx = Q / (K_approx * delta_t_log)

    return TheoreticalResults(
        t1_avg=round(t1_avg, 1),
        t2_avg=round(t2_avg, 1),
        t2_in=round(t2_in, 1),
        t2_out=round(t2_out, 1),
        delta_t_log=round(delta_t_log, 2),
        heat_load=round(Q, 2),
        G2=round(G2, 2),
        F_approx=round(F_approx, 2),
        n_z=n_z_results,
        heated_properties={
            "density": heated_props.density,
            "heat_capacity": heated_props.heat_capacity,
            "viscosity": heated_props.viscosity,
            "thermal_conductivity": heated_props.thermal_conductivity
        },
        cooled_properties={
            "density": cooled_props.density,
            "heat_capacity": cooled_props.heat_capacity,
            "viscosity": cooled_props.viscosity,
            "thermal_conductivity": cooled_props.thermal_conductivity
        }
    )


def print_available_fluids():
    """Вывод списка доступных теплоносителей"""
    print("\nДоступные теплоносители:")
    for i, (name, data) in enumerate(FLUIDS_DB.items(), 1):
        props = data["props"][0]  # Берем первый набор свойств для получения min_temp/max_temp
        print(f"{i}. {name} (t_min={props.min_temp}°C, t_max={props.max_temp}°C)")


def print_input_data(input_data: HeatExchangerInput):
    """Вывод введенных данных"""
    print("\nВведенные данные:")
    print(f"Нагреваемая среда: {input_data.heated_fluid}")
    print(f"Охлаждаемая среда: {input_data.cooled_fluid}")
    print(f"Производительность аппарата: {input_data.G1} кг/с")
    print(f"Температуры нагреваемой среды: {input_data.t1_in}°C → {input_data.t1_out}°C")
    print(f"Давление на входе: {input_data.P1_in} Па")
    print(f"Допустимые потери давления: {input_data.delta_P_allowable} Па")


def print_theoretical_results(results: TheoreticalResults, input_data: HeatExchangerInput):
    """Вывод результатов теоретического расчета"""
    print("\nРезультаты теоретического расчета:")
    print(f"1. Средняя температура {input_data.heated_fluid}: {results.t1_avg}°C")
    print(f"2. Средняя температура {input_data.cooled_fluid}: {results.t2_avg}°C")
    print(f"3. Температуры охлаждаемой среды: {results.t2_in}°C → {results.t2_out}°C")
    print(f"4. Средняя логарифмическая разность температур: {results.delta_t_log}°C")
    print(f"5. Тепловая нагрузка: {results.heat_load} Вт")
    print(f"6. Расход охлаждающей среды: {results.G2} кг/с")

    print("\nТеоретические параметры теплообменника:")
    print(f"7. Ориентировочная поверхность теплообмена (F): {results.F_approx} м²")
    print("8. Ориентировочное значение n/z (число труб / число ходов):")
    for d_out, wall, n_z in results.n_z:
        print(f"   - Для труб {d_out}×{wall} мм: n/z ≈ {n_z}")

    print("\nСвойства теплоносителей при средних температурах:")
    print(f"9. {input_data.heated_fluid}:")
    print(f"   - Плотность: {results.heated_properties['density']} кг/м³")
    print(f"   - Теплоемкость: {results.heated_properties['heat_capacity']} Дж/(кг·К)")
    print(f"   - Вязкость: {results.heated_properties['viscosity']} Па·с")
    print(f"   - Теплопроводность: {results.heated_properties['thermal_conductivity']} Вт/(м·К)")

    print(f"10. {input_data.cooled_fluid}:")
    print(f"    - Плотность: {results.cooled_properties['density']} кг/м³")
    print(f"    - Теплоемкость: {results.cooled_properties['heat_capacity']} Дж/(кг·К)")
    print(f"    - Вязкость: {results.cooled_properties['viscosity']} Па·с")
    print(f"    - Теплопроводность: {results.cooled_properties['thermal_conductivity']} Вт/(м·К)")


@dataclass
class StandardHeatExchanger:
    """Класс для хранения параметров стандартных теплообменников"""
    diameter: float  # Диаметр кожуха, мм
    tube_size: str  # Размер труб (например, "20x2")
    n_passes: int  # Число ходов
    n_tubes: int  # Число труб
    surface_areas: Dict[float, float]  # {длина: площадь поверхности, м2}
    flow_area_shell: float  # Площадь сечения потока в межтрубном пространстве, 10^-2 м2
    flow_area_tube: float  # Площадь сечения потока в трубах, 10^-2 м2


# База данных стандартных теплообменников (полная по предоставленной таблице)
STANDARD_EXCHANGERS = [
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


def select_heat_exchanger(F_approx: float, n_z_approx: int) -> Tuple[Optional[StandardHeatExchanger], Dict[str, Any]]:
    """Выбор подходящего стандартного теплообменника"""
    candidates = []

    for exchanger in STANDARD_EXCHANGERS:
        for length, surface in exchanger.surface_areas.items():
            # Ищем теплообменники с запасом по поверхности (не менее 10%)
            if surface >= F_approx * 1.1:
                n_z_actual = exchanger.n_tubes / exchanger.n_passes
                surface_diff = surface - F_approx
                n_z_diff = n_z_actual - n_z_approx

                # Оцениваем приоритет (меньше отклонение - лучше)
                priority = (surface_diff / F_approx) * 0.7 + abs(n_z_diff / n_z_approx) * 0.3

                candidates.append({
                    "exchanger": exchanger,
                    "length": length,
                    "surface": surface,
                    "surface_diff": surface_diff,
                    "n_z_actual": n_z_actual,
                    "n_z_diff": n_z_diff,
                    "priority": priority
                })
    if not candidates:
        # Если не нашли с запасом 10%, ищем просто с запасом
        for exchanger in STANDARD_EXCHANGERS:
            for length, surface in exchanger.surface_areas.items():
                if surface >= F_approx:
                    n_z_actual = exchanger.n_tubes / exchanger.n_passes
                    surface_diff = surface - F_approx
                    n_z_diff = n_z_actual - n_z_approx
                    priority = (surface_diff / F_approx) * 0.7 + abs(n_z_diff / n_z_approx) * 0.3

                    candidates.append({
                        "exchanger": exchanger,
                        "length": length,
                        "surface": surface,
                        "surface_diff": surface_diff,
                        "n_z_actual": n_z_actual,
                        "n_z_diff": n_z_diff,
                        "priority": priority
                    })

    if not candidates:
        return None, {"error": "Не найдено подходящих теплообменников"}

    # Сортируем по приоритету (лучшие варианты сначала)
    candidates.sort(key=lambda x: x["priority"])

    # Выбираем 3 лучших варианта
    top_candidates = candidates[:3]

    return top_candidates[0]["exchanger"], {
        "selected": top_candidates[0],
        "alternatives": top_candidates[1:]
    }


def print_exchanger_selection_results(selected: Optional[StandardHeatExchanger], selection_data: Dict[str, Any],
                                      F_approx: float, n_z_approx: int):
    """Вывод результатов выбора теплообменника"""
    if selected is None:
        print("\nНе удалось подобрать стандартный теплообменник")
        print(f"Причина: {selection_data.get('error', 'неизвестная ошибка')}")
        return

    selected_data = selection_data["selected"]
    alternatives = selection_data.get("alternatives", [])

    print("\nПодобран стандартный теплообменник:")
    print(f"Диаметр кожуха: {selected.diameter} мм")
    print(f"Размер труб: {selected.tube_size} мм")
    print(f"Число ходов: {selected.n_passes}")
    print(f"Число труб: {selected.n_tubes}")
    print(f"Длина труб: {selected_data['length']} м")
    print(f"Площадь поверхности: {selected_data['surface']} м²")
    print(
        f"Отклонение по площади: +{selected_data['surface_diff']:.2f} м² ({selected_data['surface_diff'] / F_approx * 100:.1f}%)")
    print(f"Отклонение по n/z: {selected_data['n_z_diff']:.1f} ({selected_data['n_z_actual']} vs {n_z_approx})")

    if alternatives:
        print("\nАльтернативные варианты:")
        for i, alt in enumerate(alternatives, 1):
            print(f"{i}. Диаметр {alt['exchanger'].diameter} мм, {alt['exchanger'].tube_size}, "
                  f"ходов: {alt['exchanger'].n_passes}, труб: {alt['exchanger'].n_tubes}, "
                  f"длина: {alt['length']} м, площадь: {alt['surface']} м²")


def main():
    print("Технологический расчет кожухотрубчатого нагревателя")
    print_available_fluids()

    try:
        # Ввод данных
        heated_idx = int(input("\nВыберите номер нагреваемой среды: ")) - 1
        cooled_idx = int(input("Выберите номер охлаждаемой среды: ")) - 1

        heated_fluid = list(FLUIDS_DB.keys())[heated_idx]
        cooled_fluid = list(FLUIDS_DB.keys())[cooled_idx]

        while True:
            G1 = float(input("\nПроизводительность аппарата (кг/с): "))
            if G1 <= 0:
                print("Ошибка: расход не может быть отрицательным или нулевым!")
                continue
            break

        t1_in = float(input("Начальная температура нагреваемой среды (°C): "))
        t1_out = float(input("Конечная температура нагреваемой среды (°C): "))

        while True:
            P1_in = float(input("Давление на входе в теплообменник (Па): "))
            if P1_in < 0:
                print("Ошибка: давление не может быть отрицательным!")
                continue
            break

        while True:
            delta_P = float(input("Допустимые потери давления (Па): "))
            if delta_P < 0:
                print("Ошибка: потери давления не могут быть отрицательными!")
                continue
            break

        # Создание объекта входных данных
        input_data = HeatExchangerInput(
            heated_fluid=heated_fluid,
            cooled_fluid=cooled_fluid,
            G1=G1,
            t1_in=t1_in,
            t1_out=t1_out,
            P1_in=P1_in,
            delta_P_allowable=delta_P
        )

        # Вывод введенных данных
        print_input_data(input_data)

        # Выполнение расчета
        results = calculate_theoretical(input_data)

        # Вывод результатов
        print_theoretical_results(results, input_data)

        # Подбор стандартного теплообменника
        # Используем первый вариант труб для подбора
        n_z_approx = results.n_z[0][2] if results.n_z else 1
        selected_exchanger, selection_data = select_heat_exchanger(results.F_approx, n_z_approx)

        # Вывод результатов подбора
        print_exchanger_selection_results(selected_exchanger, selection_data, results.F_approx, n_z_approx)

    except (ValueError, IndexError) as e:
        print(f"\nОшибка: {e}")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
