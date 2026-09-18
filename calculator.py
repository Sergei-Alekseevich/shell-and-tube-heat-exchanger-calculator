import math
from typing import Tuple
from .models import HeatExchangerInput, TheoreticalResults
from .utils import (
    get_interpolated_fluid_properties,
    get_fluid_properties,
    check_temperature_constraints
)


def calculate_hot_fluid_temperatures(t1_in: float, t1_out: float, cooled_fluid: str) -> Tuple[float, float]:
    """Определяет начальную и конечную температуру охлаждающей среды."""
    props = get_interpolated_fluid_properties(cooled_fluid, (t1_in + t1_out) / 2)

    if cooled_fluid == "Вода":
        t2_in = 95.0
        t2_out = 40.0
    else:
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
    """Выполняет теоретический технологический расчет."""
    check_temperature_constraints(input_data.heated_fluid, input_data.t1_in)
    check_temperature_constraints(input_data.heated_fluid, input_data.t1_out)

    if input_data.t1_in == input_data.t1_out:
        raise ValueError(
            f"Ошибка: Начальная и конечная температуры одинаковы ({input_data.t1_in}°C).\n"
            f"Для теплообмена необходим перепад температур."
        )

    if input_data.t1_out <= input_data.t1_in:
        raise ValueError(
            f"Ошибка: Конечная температура ({input_data.t1_out}°C) должна быть строго больше "
            f"начальной ({input_data.t1_in}°C) для нагревателя."
        )

    t2_in, t2_out = calculate_hot_fluid_temperatures(
        input_data.t1_in, input_data.t1_out, input_data.cooled_fluid
    )

    check_temperature_constraints(input_data.cooled_fluid, t2_in)
    check_temperature_constraints(input_data.cooled_fluid, t2_out)

    t1_avg = (input_data.t1_in + input_data.t1_out) / 2
    t2_avg = (t2_in + t2_out) / 2

    heated_props = get_fluid_properties(input_data.heated_fluid, t1_avg)
    cooled_props = get_fluid_properties(input_data.cooled_fluid, t2_avg)

    delta_t_b = abs(input_data.t1_out - t2_in)
    delta_t_m = abs(input_data.t1_in - t2_out)

    if delta_t_b == delta_t_m:
        delta_t_log = delta_t_b
    elif delta_t_b == 0 or delta_t_m == 0:
        raise ValueError("Нулевая разность температур на одном из концов теплообменника!")
    else:
        delta_t_log = (delta_t_b - delta_t_m) / math.log(delta_t_b / delta_t_m)

    Q = input_data.G1 * heated_props.heat_capacity * (input_data.t1_out - input_data.t1_in)

    if cooled_props.heat_capacity == 0 or delta_t_log == 0:
        raise ValueError("Деление на ноль: нулевая теплоемкость или разность температур.")

    G2 = Q / (cooled_props.heat_capacity * delta_t_log)

    Re_approx = 15000
    tube_diameters = [(25e-3, 2e-3), (20e-3, 2e-3)]
    n_z_results = []
    for d_out, wall in tube_diameters:
        d_in = d_out - 2 * wall
        n_z = (4 * input_data.G1) / (math.pi * d_in * Re_approx * heated_props.viscosity)
        n_z_results.append((d_out * 1e3, wall * 1e3, round(n_z)))

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