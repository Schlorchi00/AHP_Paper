# AHP_Monte_Carlo

Package of scripts to apply an AHP with Monte Carlo simulation. Project files [in the google drive folder](https://drive.google.com/drive/folders/17u5-oOsBx12wAZ7zGiRGsdAQbPqbG3Fh)

![Description of the image of the AHP structure](./docs/cost_model.jpg)

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
install environment `ahp` by typing `conda env create --file ahp_env.txt` or `conda en create --file ahp_env.yml` on Mac.
Dump environments by running `conda env export --no-builds > ahp_env.yml`
activate environments by running `conda activate ahp`
Active environments are denoted by a `(ahp)` preceeding the `user@host:` notation

### Pip installation
**Within the activated conda environment** (`conda activate ahp`)
install the package by running `pip install -e .`, see [this source](https://goodresearch.dev/setup.html#pip-install-your-package)

# Script usages
## Cost Calculation
The cost calculation can be found in the [scripts](./scripts/cost_calculation.py) directory.
Run from the base directory after activating the environment with:
```
    python scripts/cost_calculation.py -i
```
Parameters are explained below

### Parameters

* -i, --input: path to an input xls file with the fields filled in. An example file is supplied in: **path to example file here**. Can be multiple, with -i <file1> -i <file2> etc. 
* -s, --scale: Scaling Factor. List. Weight of the recycling mass in gram, to rescale to euros per gramm. Will check for same length as inputs. In order of inputs. E.g. -i <file1> -s <scale1> etc. 
* -n, --name: the name of a material to be used in the output
* -v, --value: the value that material is supposed to be assigned. Name and value are lists and are appended in position with one another. E.g. -n <Material1> -v <Value1> -n <Material2> -v <Value2>
* -t, --time: Boolean flag wether to use time or energy in the calculation of operational costs. Defaults to energy. If set, will use time.
* -o, --output: Output location of the file to be written. Defaults to None. If none, will print dataframe for checking to command line.
* -h, --help: display the help, which will illustrate the parameters 


In order to run the program just start the cost_calculation.py, which has to be marked as executable and put in your paths for the dummy data files

```bash
chmod +x cost_calculation.py
./cost_calculation.py
```

### Usage with Conda Environment and argument parser
1. Activate conda environment by typing `conda activate ahp` after running the [install steps](#conda-usage).
2. navigate to the base directory (`cd <base_directory_of_environment>` - mostly AHP_Paper)
3. run the script by typing (`python scripts/cost_calculation.py -i <path to the data file>` - path is mostly data/cost/cost_polymers.xlsx)

## Description

The program reads an excel table, where the practitioner had to measure all the relevant cost parameters and protocol it. The file calculates the cost positions based on the excel file

## Issues
[ ] Nico - cannot run `cost_calculation.py` - statement wb `shredding` does not exist in [excel file](./data/cost/cost_polymers.xlsx)