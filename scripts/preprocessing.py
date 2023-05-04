import os.path
import openpyxl
from ahp.utils import *


"""
        ! Required for Preprocessing
            * from an excel file
        
        ! Structure Data
            * Ecology Table:
                                Atlernative I   Alternative II  ... Alternative n
                    Param I         Value           Value       ...     Value
                    Param II        ...
                    Param III       ...                                     
                    Total           ...                                 ...
        
            * Performance Table = [Sheet 1 = Param 1, Param 2, Param 3]
                * Each Param:
                
                                 Atlernative I   Alternative II  ... Alternative n
                    Max             Value           Value       ...     Value
                    Min             ...
                    Mean            ...                                     
                    Stdv            ...                                 ...
            
            * Process Table = [Sheet 1 = Param 1, Param 2]
                * Each Param:
                
                                 Atlernative I   Alternative II  ... Alternative n
                    Max             Value           Value       ...     Value
                    Min             ...
                    Mean            ...                                     
                    Stdv            ...                                 ...
                    
            * Cost Table:
                                Atlernative I   Alternative II  ... Alternative n
                    Param I         Value           Value       ...     Value
                    
                    
        ! Preprocessing should be 
        TODO:
            * [ ] save normalized .xlsx -file
                * [ ] transform param matrix into 1 x len(altneratives) 
                    * [ ] check which normalization method is required
                    * [ ] apply normalization method
                        * [ ] define if minimum or maximum threshold is required (maybe with flag)
                        * [ ] set thresholds in first and last column (maybe other module)
                            * [ ] Check which Table (Performance, Process, Ecology, Cost)
                            * [ ] Extract params (other module)
                            + [ ] Store them in dictionary
                                * load  .xlsx - file
                                
            * [ ] save total cost .xlsx - file
                * [ ] horizontal stack of alternatives 
                    * [ ] Get standard (virgin) alternative
                    * [ ] Get unmodified (lab calculation) alternative(s) 
                    * [ ] Get modified (industrial calculation) alternative(s)
                        * [ ] calculation of unmodified alternative -> cost calculation
                        * [ ] calculation of modified alternative -> how to change cost calculation script (other module)
                            

                
"""


def print_something():
    print("Use this structure to develop functions. Only move to utils when done")

def read_domain(subdomain, filename, data = 'data'):
    """
    loads excel files and creates workbook
    :param subdomain: string of the name regarding the subdomain
    :param filename: string of filename.xlsx
    :param data: string of the foldername
    :return: workbook
    """

    ppath = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    datadir = os.path.join(ppath, '..', data, subdomain)
    df_path = os.path.join(datadir,filename)
    wb = openpyxl.load_workbook(df_path)

    return wb

#create data frames

def create_df(wb, sheet1 = 'Sheet1', sheet2 = None, sheet3 = None):
    """
    modifies a workbook into a suitable dataframe
    :param wb: workbook
    :return: dataframe
    """
    if sheet2 == None  and sheet3 == None:
        sheet_1 = wb[sheet1]
        df = pd.DataFrame(sheet_1.values)
        df = df.rename(columns=df.iloc[1])
        df = df.iloc[2:,:].reset_index(drop=True)

        return df

    if sheet3 == None:

        sheet_1 = wb[sheet1]
        df = pd.DataFrame(sheet_1.values)
        df = df.rename(columns=df.iloc[1])
        df_1 = df.iloc[2:,:].reset_index(drop=True)

        sheet_2 = wb[sheet2]
        df = pd.DataFrame(sheet_2.values)
        df = df.rename(columns=df.iloc[1])
        df_2 = df.iloc[2:, :].reset_index(drop=True)

        return df_1, df_2

    else:
        sheet_1 = wb[sheet1]
        df = pd.DataFrame(sheet_1.values)
        df = df.rename(columns=df.iloc[1])
        df_1 = df.iloc[2:, :].reset_index(drop=True)

        sheet_2 = wb[sheet2]
        df = pd.DataFrame(sheet_2.values)
        df = df.rename(columns=df.iloc[1])
        df_2 = df.iloc[2:, :].reset_index(drop=True)

        sheet_3 = wb[sheet3]
        df = pd.DataFrame(sheet_3.values)
        df = df.rename(columns=df.iloc[1])
        df_3 = df.iloc[2:, :].reset_index(drop=True)

        return df_1, df_2, df_3




if __name__=="__main__":

    print_something()

    #read files TODO: Check correctness regarding amount of leaf nodes

    wb_eco = read_domain('ecology', 'LCA_Endpoints_PLA_Coins.xlsx')
    wb_mech_90 = read_domain('performance', 'Mechanical_Params_90_degrees.xlsx')
    wb_mech_0 = read_domain('performance', 'Mechanical_Params_0_degrees.xlsx')
    wb_process_fila = read_domain('process', 'FILA_CHAR.xlsx')
    wb_process_mvr = read_domain('process', 'MFI_Polymers.xlsx')
    wb_cost = read_domain('cost', 'cost_polymers.xlsx')

    #create df
    df_mech_90 = create_df(wb_mech_90, sheet1 = 'E_modulus', sheet2='tensile strain', sheet3='tensile stress')


    # preprocess here

    # read files
    #read_from_xlsx()

    # write to excel file
    #write_to_xlsx()