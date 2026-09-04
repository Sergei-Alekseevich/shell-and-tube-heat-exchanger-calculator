# shell-and-tube-heat-exchanger-calculator
Python tool for thermodynamic calculation, fluid property interpolation, and automatic selection of shell-and-tube heat exchangers

> Note: The console output and fluid database currently use Russian terminology in accordance with GOST and national industrial standards for chemical and process engineering.

## Key Features

1) Dynamic Fluid Property Interpolation: Automatic calculation of fluid properties (density, viscosity, heat capacity, thermal conductivity) at average process temperatures using linear interpolation for fluids like Water, Heptane, Ethylene Glycol, and Mineral Oil.
2) Thermodynamic Calculation:
  * Logarithmic mean temperature difference ($\Delta t_{log}$) computation.
  * Calculation of heat duty ($Q$) and required coolant mass flow rate ($G_2$).
  * Estimation of required heat transfer surface area ($F_{approx}$) and hydrodynamic ratio ($n/z$).
3) Automated Equipment Selection: Evaluates and ranks standard shell-and-tube heat exchanger units from built-in structural catalogs with a minimum recommended surface margin ($\ge 10\%$).
4) Process Constraint Validation: Integrated checks for operating temperature limits, valid temperature driving forces, and boundary conditions.

## Tech Stack

* Python 3.8+
* dataclasses — Structuring domain entities (FluidProperties, HeatExchangerInput, StandardHeatExchanger).
* typing — Type hinting for improved code readability and reliability.
* math — Mathematical functions for hydrodynamic and heat transfer modeling.

## Core Calculation Workflow

1) Property Interpolation:  
   $$f(T) = y_1 + \frac{y_2 - y_1}{x_2 - x_1} \cdot (T - x_1)$$
2) Heat Duty ($Q$):  
   $$Q = G_1 \cdot c_p \cdot (t_{1,out} - t_{1,in})$$
3) Logarithmic Mean Temperature Difference ($\Delta t_{log}$):  
   $$\Delta t_{log} = \frac{\Delta t_{max} - \Delta t_{min}}{\ln(\Delta t_{max} / \Delta t_{min})}$$
4) Candidate Ranking: Ranks structural exchanger options based on surface margin and $n/z$ geometrical parameters.

## Quick Start

No external dependencies are required.

```bash
# Clone the repository
git clone https://github.com/Sergei-Alekseevich/shell-and-tube-heat-exchanger-calculator.git

# Run the calculator module
python main.py
```

* Follow the interactive console prompts to select operating fluids and input process parameters...
​
# Project Context
​This tool was developed as a final evaluation project during a professional development program (DPO). It demonstrates practical application of Python algorithms to process engineering and thermodynamic design. It could save from 2 to 5 hours of manual engineering calculations.
