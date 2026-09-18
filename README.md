# shell-and-tube-heat-exchanger-calculator

Python tool for thermodynamic calculation, fluid property interpolation, and automatic selection of shell-and-tube heat exchangers.

> **Note:** The console output and fluid database currently use Russian terminology in accordance with GOST and national industrial standards for chemical and process engineering.

---

## Key Features

* **Dynamic Fluid Property Interpolation:** Automatic calculation of fluid properties (density, viscosity, heat capacity, thermal conductivity) at average process temperatures using linear interpolation for fluids like Water, Heptane, Ethylene Glycol, and Mineral Oil.
* **Thermodynamic Calculation:**
  * Logarithmic mean temperature difference ($\Delta t_{log}$) computation.
  * Calculation of heat duty ($Q$) and required coolant mass flow rate ($G_2$).
  * Estimation of required heat transfer surface area ($F_{approx}$) and hydrodynamic ratio ($n/z$).
* **Automated Equipment Selection:** Evaluates and ranks standard shell-and-tube heat exchanger units from built-in structural catalogs with a minimum recommended surface margin ($\ge 10\%$).
* **Process Constraint Validation:** Integrated checks for operating temperature limits, valid temperature driving forces, and boundary conditions.

---

## Tech Stack

* **Python 3.8+** (Standard Library only)
* **`dataclasses`** — Structuring domain entities (`FluidProperties`, `HeatExchangerInput`, `StandardHeatExchanger`).
* **`typing`** — Type hinting for code readability and static analysis.
* **`math`** — Mathematical functions for hydrodynamic and heat transfer modeling.

---

## Project Structure & Architecture

    shell-and-tube-heat-exchanger-calculator/
    │
    ├── src/
    │   └── heat_exchanger/
    │       ├── __init__.py       # Package initialization & public API exports
    │       ├── models.py         # Dataclass entities for inputs, results, and catalog items
    │       ├── database.py       # Thermophysical fluid data (GOST) and exchanger catalog
    │       ├── utils.py          # Linear interpolation algorithms and range checkers
    │       ├── calculator.py     # Core thermodynamic calculation formulas
    │       ├── selector.py       # Equipment lookup and priority ranking logic
    │       └── cli.py            # Console user interface and output formatting
    │
    ├── main.py                   # Main entry point for running the application
    ├── .gitignore                # Git exclusion rules
    ├── requirements.txt          # Dependency manifest
    └── README.md                 # Project documentation

### Module Breakdown

* **`src/heat_exchanger/models.py`**: Defines core data structures using `@dataclass` (`FluidProperties`, `HeatExchangerInput`, `TheoreticalResults`, `StandardHeatExchanger`).
* **`src/heat_exchanger/database.py`**: Stores reference tables for fluid properties at various temperatures (`FLUIDS_DB`) and standard catalog sizes for shell-and-tube units (`STANDARD_EXCHANGERS`).
* **`src/heat_exchanger/utils.py`**: Contains utility functions for 1D linear interpolation of temperature-dependent properties and boundary condition validation.
* **`src/heat_exchanger/calculator.py`**: Implements process thermodynamics logic (heat load, logarithmic mean temperature difference, mass flow rates, and surface estimations).
* **`src/heat_exchanger/selector.py`**: Compares theoretical requirements against standard catalog items and ranks candidates by surface margin and tube pass configuration ($n/z$).
* **`src/heat_exchanger/cli.py`**: Manages interactive terminal inputs, validation errors, and formatted output presentation.
* **`main.py`**: Root entry point script that connects package modules and launches the CLI.

---

## Core Calculation Workflow

1. **Property Interpolation:**
   $$f(T) = y_1 + \frac{y_2 - y_1}{x_2 - x_1} \cdot (T - x_1)$$

2. **Heat Duty ($Q$):**
   $$Q = G_1 \cdot c_p \cdot (t_{1,out} - t_{1,in})$$

3. **Logarithmic Mean Temperature Difference ($\Delta t_{log}$):**
   $$\Delta t_{log} = \frac{\Delta t_{max} - \Delta t_{min}}{\ln(\Delta t_{max} / \Delta t_{min})}$$

4. **Candidate Ranking:** Ranks structural exchanger options based on surface margin and $n/z$ geometrical parameters.

---

## Quick Start

No external dependencies are required.

    # Clone the repository
    git clone https://github.com/Sergei-Alekseevich/shell-and-tube-heat-exchanger-calculator.git

    # Navigate into project directory
    cd shell-and-tube-heat-exchanger-calculator

    # Run the calculator module
    python main.py

Follow the interactive console prompts to select operating fluids and input process parameters.

---

## Project Context

This tool was developed as a final evaluation project during a professional development program (DPO). It demonstrates practical application of Python algorithms to process engineering and thermodynamic design, saving approximately 2 to 5 hours of manual engineering calculations per unit design.
