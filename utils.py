from .models import FluidProperties
from .database import FLUIDS_DB


def linear_interpolation(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Выполняет линейную интерполяцию."""
    return y1 + (y2 - y1) / (x2 - x1) * (x - x1)


def get_interpolated_fluid_properties(fluid_name: str, temperature: float) -> FluidProperties:
    """Возвращает свойства теплоносителя с учетом интерполяции по температуре."""
    if fluid_name not in FLUIDS_DB:
        raise ValueError(f"Теплоноситель '{fluid_name}' не найден в базе данных")

    fluid_data = FLUIDS_DB[fluid_name]
    temps = fluid_data["temps"]
    props_list = fluid_data["props"]

    if temperature <= temps[0]:
        return props_list[0]

    if temperature >= temps[-1]:
        return props_list[-1]

    for i in range(len(temps) - 1):
        if temps[i] <= temperature <= temps[i + 1]:
            t1, t2 = temps[i], temps[i + 1]
            p1, p2 = props_list[i], props_list[i + 1]

            return FluidProperties(
                name=fluid_name,
                density=linear_interpolation(temperature, t1, p1.density, t2, p2.density),
                heat_capacity=linear_interpolation(temperature, t1, p1.heat_capacity, t2, p2.heat_capacity),
                viscosity=linear_interpolation(temperature, t1, p1.viscosity, t2, p2.viscosity),
                thermal_conductivity=linear_interpolation(temperature, t1, p1.thermal_conductivity, t2, p2.thermal_conductivity),
                min_temp=p1.min_temp,
                max_temp=p1.max_temp
            )

    return props_list[-1]


def get_fluid_properties(fluid_name: str, temperature: float) -> FluidProperties:
    """Алиас для получения свойств теплоносителя."""
    return get_interpolated_fluid_properties(fluid_name, temperature)


def check_temperature_constraints(fluid_name: str, temperature: float) -> None:
    """Проверяет соответствие температуры допустимому диапазону."""
    props = get_interpolated_fluid_properties(fluid_name, temperature)
    if temperature < props.min_temp or temperature > props.max_temp:
        raise ValueError(
            f"Температура {temperature}°C недопустима для {fluid_name}. "
            f"Допустимый диапазон: {props.min_temp}...{props.max_temp}°C"
        )