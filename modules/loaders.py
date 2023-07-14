from glob import glob
import pandas as pd

# Source site to download the data from
# https://mrv.emsa.europa.eu/#public/emission-report

class LoadData:

    def __init__(self) -> None:
        
        self.glob_excel()
        self.import_all_xlsx()

    def glob_excel(self) -> None:
        all_xlsx_filenames = glob('./data/*.xlsx')

        # If the user has a file open, Excel will make a temporary locked file that cannot be opened with a ~ in it.
        # This statement filters out the open filesfor improved usability running the code with open files.
        self.xlsx_filenames = [fn for fn in all_xlsx_filenames if '~' not in fn]

    def import_all_xlsx(self) -> None:
        self.data = pd.concat([self.read_excel_file(i) for i in self.xlsx_filenames])

    def read_excel_file(self, f) -> pd.DataFrame:

        print(f"Loading .... {f}")
        return pd.read_excel(f, skiprows=[0,1], engine="openpyxl")