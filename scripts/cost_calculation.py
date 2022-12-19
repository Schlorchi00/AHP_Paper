import openpyxl

from ahp.cost_calculation import create_df, total_cost

def main():
    # set path

    path_costtable = str(input('Put in path to your cost table: '))

    # load data from excel workbook

    wb = openpyxl.load_workbook(path_costtable)
    shredd = wb['shredding']
    extr = wb['extrusion']
    gran = wb['granulate']
    con = wb['conditioning']

    # create df
    df_shredd = create_df(shredd)
    df_extr = create_df(extr)
    df_gran = create_df(gran)
    df_con = create_df(con)

    cost_list = [df_shredd, df_extr, df_gran, df_con]

    tot_cost = total_cost(cost_list)



# call main function - safeguard for external includes
if __name__ == "__main__":
    main()








