# AHP_Monte_Carlo

Package of scripts to apply an AHP with Monte Carlo simulation

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install openpyxl.

```bash
pip3 install openpyxl
```

Clone this repository onto your local machine.

```bash
git clone https://github.com/Schlorchi00/AHP_Paper.git
```

### Conda usage
install environment `ahp` by typing `conda env create --file ahp_env.txt`

## Usage

##cost_calculation.py

In order to run the program just start the cost_calculation.py, which has to be marked as executable and put in your paths for the dummy data files

```bash
chmod +x cost_calculation.py
./cost_calculation.py
```



## Description

The program reads an excel table, where the practitioner had to measure all the relevant cost parameters and protocol it. The file calculates the cost positions based on the excel file
