import os.path
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
                                * load .xlsx - file
                                
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

if __name__=="__main__":
    print_something()
    ppath = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    datadir = os.path.join(ppath, '..', 'data', 'ecology')

    df_path = os.path.join(datadir, 'LCA_Endpoints_PLA_Coins.xlsx' )
    df = read_excel(df_path, series=False)
    print(df)

    # preprocess here

    # read files
    #read_from_xlsx()

    # write to excel file
    #write_to_xlsx()