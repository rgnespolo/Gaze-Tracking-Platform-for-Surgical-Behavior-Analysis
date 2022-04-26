import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv(r'all_experts_one_sheet.csv')
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.display.width = None


phases = ['rhexis', 'phaco', 'cortex', 'core_vitr', 'memb_peel', 'laser']
#IDs of each group of surgeons
attendings = [1,2,9] 
residents = [4,5,6]
fellows = [3,7,8,10,11]
def main():
    for i in (n + 1 for n in range(len(phases))): #stats are generated for each surgical phase
        df_single_phase = df.query('phase == ' + str(i) + '& user == ' + str(attendings)) #Filter for the desired group of surgeons or specific surgeon 

        #Average distance traveled by the selected group of surgeons 
        #print(round(df_single_phase['dist'].sum(),2)/len(fellows))
        print((df_single_phase.groupby('user')['dist'].sum()).std())




if __name__ == "__main__":
    main()

