from glob import glob
import pandas as pd

# Source site to download the data from
# https://mrv.emsa.europa.eu/#public/emission-report

class LoadData:

    def __init__(self) -> None:
        
        self.glob_excel()
        self.import_all_xlsx()

    def glob_excel(self) -> None:
        '''
        Reads in a all of the Excel files that have been deposited in the data directory and saves them to the 
        .xlsx_filenames attribute.
        '''

        all_xlsx_filenames = glob('./data/*.xlsx')

        # If the user has a file open, Excel will make a temporary locked file that cannot be opened with a ~ in it.
        # This statement filters out the open filesfor improved usability running the code with open files.
        self.xlsx_filenames = [fn for fn in all_xlsx_filenames if '~' not in fn]

    def import_all_xlsx(self) -> None:
        '''
        Opens all of the filenames in the xlsx_filenames attributes with the open function.
        '''
        
        self.data = pd.concat([self.read_excel_file(i) for i in self.xlsx_filenames])

    def read_excel_file(self, f) -> pd.DataFrame:
        '''
        Opens Excel files from a filepath and returns the data frame of it. 
        '''

        print(f"Loading .... {f}")
        return pd.read_excel(f, skiprows=[0,1], engine="openpyxl")