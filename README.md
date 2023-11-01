# AHP

Package of scripts to apply an AHP. Project files [in the google drive folder](https://drive.google.com/drive/folders/17u5-oOsBx12wAZ7zGiRGsdAQbPqbG3Fh)

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
1. Activate conda environment by typing `conda activate ahp` after running the [install steps](#conda-usage).
2. navigate to the base directory (`cd <base_directory_of_environment>` - mostly AHP_Paper)
3. run the script by typing (`python scripts/cost_calculation.py -i <path to the data file>` - path is mostly data/cost/cost_polymers.xlsx)

## Cost Calculation
The cost calculation can be found in the [scripts](./scripts/cost_calculation.py) directory.
Run from the base directory after activating the environment with:
```
    python scripts/cost_calculation.py -i <file> -s <scale> -n <name> -v <value> OPTIONAL -t -o <output_location>
```
Can be run as a command line utility without changes to the code. Will append a linear scaling sheet, without quadratic options, explained [below](#scaling). 
Parameters are explained below

### Parameters

* -i, --input: path to an input xls file with the fields filled in. An example file is supplied in: **path to example file here**. Can be multiple, with -i <file1> -i <file2> etc. 
* -s, --scale: Scaling Factor. List. Weight of the recycling mass in gram, to rescale to euros per gramm. Will check for same length as inputs. In order of inputs. E.g. -i <file1> -s <scale1> etc. 
* -n, --name: the name of a material to be used in the output
* -v, --value: the value that material is supposed to be assigned. Name and value are lists and are appended in position with one another. E.g. -n <Material1> -v <Value1> -n <Material2> -v <Value2>
* -t, --time: Boolean flag wether to use time or energy in the calculation of operational costs. Defaults to energy. If set, will use time.
* -o, --output: Output location of the file to be written. Defaults to None. If none, will print dataframe for checking to command line.
* -h, --help: display the help, which will illustrate the parameters 

## Preprocessing
The cost calculation can be found in the [scripts](./scripts/preprocessing.py) directory.
Run from the base directory after activating the environment with:
```
    python scripts/preprocessing.py -i <input> -s <scaling> -o <output>
```
Can be run as a command line utility without changes to the code.
A scaling sheet is appended to the example file which can be found **path to example file**. Scaling options are explained [below](#scaling).
Consistency checks will be performed as part of the script.
Parameters are explained below

### Parameters

* -i, --input: REQUIRED location of the file with the values that have been recorded for each alternative, which will all be leaf nodes. Each line corresponds to a leaf node, measured values, each column to an alternative
* -o, --output: directory where the leaf nodes will be written to. A leaf node has a value for each of the alternatives. If none given, will print to command line. Defaults to none.
* -s, --scaling: optional. Will scale the values to be between {0, 1} according to what _optimal_ values are considered to be.

### Scaling
Scaling values are supplied as a second sheet to the preprocessing excel file. This sheet ensures that recorded measurements for each alternative are scaled between {0,1}
Possibilities exist for linear or quadratic scaling. If values for quadratic are present in the sheet, quadratic scaling will be applied.
* Linear scaling
    * Min: minimum possible value. If None, will use minimum from inputs. E.g. if theoretical minimum for a value is known, supply. 
    * Max: Maximum possible value. if None, will use maximum from inputs. E.g. if theoretical maximum is known, supply. 
    * Inversion: if set to 1, low values represent better options. E.g. Lower costs are usually better. 
* Quadratic scaling
    * Optimal: if an optimal value can be achieved, use this and quadratic distance between optimal and threshold value (or largest distance) will be used. E.g. printing diameter has an optimal centrepoint 
    * Threshold: Set a threshold value after which all parameters will be 0. E.g. in case of diameter, +- 5cm from optimal

## Calculating a tree
Example script is provided [here](./scripts/test_ahp.py)
The only parameter is an input directory, from which the tree structure will be set up. The script runs four steps including consistency checks

1. Reading a tree from a directory structure. This checks for directory and spreadsheet naming conventions 
2. Preparing a tree from the structure provided in the previous steps
3. Checking the integrity of values and weights
4. Calculating the final decision support tree

The final result will be printed to the command line. 
Changes can be made in the script after the calculation. Weights and values can be plotted or printed through node convenience methods, see [example](/src/ahp/ahp_functions.py#L409) 

### Parameters

* --input, -i: base directory for a tree setup. The tree should be structured 
