from typing import Optional, Dict, Any
from .models import HeatExchangerInput, TheoreticalResults, StandardHeatExchanger
from .database import FLUIDS_DB
from .calculator import calculate_theoretical
from .selector import select_heat_exchanger


def print_available_fluids():
    print("\nДоступные теплоносители:")
    for i, (name, data) in enumerate(FLUIDS_DB.items(), 1):
        props = data["props"][0]
        print(f"{i}. {name} (t_min={props.min_temp}°C, t_max={props.max_temp}°C)")


def print_input_data(input_data: HeatExchangerInput):
    print("\nВведенные данные:")
    print(f"Нагреваемая среда: {input_data.heated_fluid}")
    print(f"Охлаждаемая среда: {input_data.cooled_fluid}")
    print(f"Производительность: {input_data.G1} кг/с")
    print(f"Температуры: {input_data.t1_in}°C → {input_data.t1_out}°C")
    print(f"Давление: {input_data.P1_in} Па")
    print(f"Допустимые потери давления: {input_data.delta_P_allowable} Па")


def print_theoretical_results(results: TheoreticalResults, input_data: HeatExchangerInput):
    print("\nРезультаты теоретического расчета:")
    print(f"1. Средняя температура ({input_data.heated_fluid}): {results.t1_avg}°C")
    print(f"2. Средняя температура ({input_data.cooled_fluid}): {results.t2_avg}°C")
    print(f"3. Температуры охлаждающей среды: {results.t2_in}°C → {results.t2_out}°C")
    print(f"4. Логарифмический температурный напор: {results.delta_t_log}°C")
    print(f"5. Тепловая нагрузка: {results.heat_load} Вт")
    print(f"6. Расход охлаждающей среды: {results.G2} кг/с")
    print("\nТеоретические параметры аппарата:")
    print(f"7. Ориентировочная площадь (F): {results.F_approx} м²")
    print("8. Ориентировочное число n/z:")
    for d_out, wall, n_z in results.n_z:
        print(f"   - Для труб {d_out}×{wall} мм: n/z ≈ {n_z}")


def print_exchanger_selection_results(selected: Optional[StandardHeatExchanger], selection_data: Dict[str, Any],
                                      F_approx: float, n_z_approx: int):
    if selected is None:
        print(f"\nНе удалось подобрать стандартный теплообменник. Ошибка: {selection_data.get('error')}")
        return

    s = selection_data["selected"]
    alts = selection_data.get("alternatives", [])

    print("\nПодобран стандартный теплообменник:")
    print(f"Диаметр кожуха: {selected.diameter} мм")
    print(f"Размер труб: {selected.tube_size} мм")
    print(f"Число ходов: {selected.n_passes}")
    print(f"Число труб: {selected.n_tubes}")
    print(f"Длина труб: {s['length']} м")
    print(f"Площадь поверхности: {s['surface']} м²")
    print(f"Запас по площади: +{s['surface_diff']:.2f} м² ({s['surface_diff'] / F_approx * 100:.1f}%)")

    if alts:
        print("\nАльтернативные варианты:")
        for i, alt in enumerate(alts, 1):
            e = alt['exchanger']
            print(f"{i}. D={e.diameter} мм, {e.tube_size}, ходов: {e.n_passes}, "
                  f"длина: {alt['length']} м, F: {alt['surface']} м²")


def main():
    print("=== Технологический расчет кожухотрубчатого нагревателя ===")
    print_available_fluids()
    try:
        heated_idx = int(input("\nВыберите номер нагреваемой среды: ")) - 1
        cooled_idx = int(input("Выберите номер охлаждаемой среды: ")) - 1

        heated_fluid = list(FLUIDS_DB.keys())[heated_idx]
        cooled_fluid = list(FLUIDS_DB.keys())[cooled_idx]

        G1 = float(input("\nПроизводительность аппарата (кг/с): "))
        t1_in = float(input("Начальная температура (°C): "))
        t1_out = float(input("Конечная температура (°C): "))
        P1_in = float(input("Давление на входе (Па): "))
        delta_P = float(input("Допустимые потери давления (Па): "))

        input_data = HeatExchangerInput(
            heated_fluid=heated_fluid,
            cooled_fluid=cooled_fluid,
            G1=G1,
            t1_in=t1_in,
            t1_out=t1_out,
            P1_in=P1_in,
            delta_P_allowable=delta_P
        )

        print_input_data(input_data)
        results = calculate_theoretical(input_data)
        print_theoretical_results(results, input_data)

        n_z_approx = results.n_z[0][2] if results.n_z else 1
        selected, selection_data = select_heat_exchanger(results.F_approx, n_z_approx)
        print_exchanger_selection_results(selected, selection_data, results.F_approx, n_z_approx)

    except (ValueError, IndexError) as e:
        print(f"\nОшибка ввода или расчета: {e}")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")