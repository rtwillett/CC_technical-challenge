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
        '''
        Converts all of the monitoring methods to binary. 
        These data are not currently useful at the moment, so this method is not crucial to the cleaning. 
        '''
        
        import numpy as np
        self.data['A'] = self.data['A'].map({'Yes': 1, np.nan:0})
        self.data['B'] = self.data['B'].map({'Yes': 1, np.nan:0})
        self.data['C'] = self.data['C'].map({'Yes': 1, np.nan:0})
        self.data['D'] = self.data['D'].map({'Yes': 1, np.nan:0})
        
    def date_cleaning(self) -> None:
        '''
        Cleans common bad entries (e.g. "not issued") from the date columns and casts them to pandas datetime objects.
        '''

        import pandas as pd

        self.data['DOC ISSUE DATE'] = [pd.to_datetime('1900-01-01') if 'not issued' in d else pd.to_datetime(d) for d in self.data['DOC ISSUE DATE']]
        self.data['DOC EXPIRY DATE'] = [pd.to_datetime('1900-01-01') if 'not issued' in d else pd.to_datetime(d) for d in self.data['DOC EXPIRY DATE']]
        
    def cleaning_string_columns(self) -> None: 
        '''
        Using pandas, if numerical columns also contain strings (e.g. "N/A", "No data", etc) it will read the whole series
        in as a string series. This method will detect all of the columns that are designated as string columns and run
        each column through a string cleaner (.remove_badentries). These series can then be cast as the appropriate 
        numerical dtype within error.
        '''

        import pandas as pd
        
        df_dtypes = pd.DataFrame(self.data.dtypes).reset_index(drop=False)
        df_dtypes.columns = ['colname', 'dtype']
        
        object_colnames = df_dtypes.loc[df_dtypes.dtype == 'object'].colname
        
        self.data[object_colnames] = self.data[object_colnames].fillna("")
        
        for c in object_colnames:
            self.data[c] = self.data[c].apply(lambda x: self.remove_badentries(str(x)))
        
    def remove_badentries(self, s:str) -> str: 
        '''
        Takes in a string and removes common bad substrings.
        Useful to clean up numerical (int or float) columns that have been read in as string objects by pandas.
        '''
        
        import re

        if detect_pattern('[A-Z]', s) != "":
            if re.search('DIVISION\sBY\sZERO|NOT\sAPPLICABLE|N\/A', s.upper()) is None:
                return s
            else: 
                return '-999'
        else: 
            return s
        
    def dtype_casting(self) -> None: 
        '''
        Takes in columns that have been cleaned (usually as a string) and cast the pandas series in to the appropriate
        dtype for subsequent analysis.
        '''
        
        self.data['REPORTING PERIOD'] = self.data['REPORTING PERIOD'].astype('int')
        self.data["ANNUAL AVERAGE FUEL CONSUMPTION PER DISTANCE [KG / N MILE]"] = self.data["ANNUAL AVERAGE FUEL CONSUMPTION PER DISTANCE [KG / N MILE]"].astype('float64')