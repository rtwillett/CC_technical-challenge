import pandas as pd
import re

def detect_pattern(pattern:str, s:str, flags = None) -> str:
    '''
    This function makes makes is simpler to use the regex in the re package because it aligns the datatypes going through
    the process (str in, str out). No need to deal with the group syntax. Returns the first occurrence of given pattern
    in a str or a blank string.
    '''

    if flags is None:
        result = re.findall(pattern, s)
    else:
        result = re.findall(pattern, s, flags = flags)

    if result != []:
        return result[0]
    else: 
        return ""

class MRVCleaner:
    
    def __init__(self, data:pd.DataFrame) -> None: 
        self.data = data
        
        self.data.columns = [s.upper() for s in self.data]
        
        self.data.drop_duplicates(inplace=True)
        
        self.cleaning_string_columns()
        
        self.dtype_casting()
    
    def monitoring_method_coding(self): 
        import numpy as np
        self.data['A'] = self.data['A'].map({'Yes': 1, np.nan:0})
        self.data['B'] = self.data['B'].map({'Yes': 1, np.nan:0})
        self.data['C'] = self.data['C'].map({'Yes': 1, np.nan:0})
        self.data['D'] = self.data['D'].map({'Yes': 1, np.nan:0})
        
    def date_cleaning(self) -> None:
        import pandas as pd

        self.data['DOC ISSUE DATE'] = [pd.to_datetime('1900-01-01') if 'not issued' in d else pd.to_datetime(d) for d in self.data['DOC ISSUE DATE']]
        self.data['DOC EXPIRY DATE'] = [pd.to_datetime('1900-01-01') if 'not issued' in d else pd.to_datetime(d) for d in self.data['DOC EXPIRY DATE']]
        
    def cleaning_string_columns(self) -> None: 
        import pandas as pd
        
        df_dtypes = pd.DataFrame(self.data.dtypes).reset_index(drop=False)
        df_dtypes.columns = ['colname', 'dtype']
        
        object_colnames = df_dtypes.loc[df_dtypes.dtype == 'object'].colname
        
        self.data[object_colnames] = self.data[object_colnames].fillna("")
        
        for c in object_colnames:
            self.data[c] = self.data[c].apply(lambda x: self.remove_badentries(str(x)))
        
    def remove_badentries(self, s:str) -> str: 
        import re


        if detect_pattern('[A-Z]', s) != "":
            if re.search('DIVISION\sBY\sZERO|NOT\sAPPLICABLE|N\/A', s.upper()) is None:
                return s
            else: 
                return '-999'
        else: 
            return s
        
    def dtype_casting(self) -> None: 
        self.data['REPORTING PERIOD'] = self.data['REPORTING PERIOD'].astype('int')
        self.data["ANNUAL AVERAGE FUEL CONSUMPTION PER DISTANCE [KG / N MILE]"] = self.data["ANNUAL AVERAGE FUEL CONSUMPTION PER DISTANCE [KG / N MILE]"].astype('float64')