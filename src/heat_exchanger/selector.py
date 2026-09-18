from typing import Tuple, Optional, Dict, Any
from .models import StandardHeatExchanger
from .database import STANDARD_EXCHANGERS


def select_heat_exchanger(F_approx: float, n_z_approx: int) -> Tuple[Optional[StandardHeatExchanger], Dict[str, Any]]:
    """Выбирает подходящий стандартный теплообменник по поверхности и n/z."""
    candidates = []

    for exchanger in STANDARD_EXCHANGERS:
        for length, surface in exchanger.surface_areas.items():
            if surface >= F_approx * 1.1:
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
        return None, {"error": "Не найдено подходящих аппаратов"}

    candidates.sort(key=lambda x: x["priority"])
    top_candidates = candidates[:3]

    return top_candidates[0]["exchanger"], {
        "selected": top_candidates[0],
        "alternatives": top_candidates[1:]
    }