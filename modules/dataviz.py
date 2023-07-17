import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt
import seaborn as sns

class MRVDataviz:


    '''
    Note:
    The graphing methods of this class make use of a y_trim parameter, which allows one to manually trim the y_axis
    and remove outliers to better view the distribution of the violin plot. Future efforts would implement an outlier
    detection approach to more rigorously and precisely optimize visualization of the distribution. 
    '''

    def __init__(self, df):
        self.data = df

    def total_emissions(self): 
        '''
        Makes vilin plot by ship type of total emissions.
        '''
        
        return self.compile_violinplot(y_col = 'TOTAL CO₂ EMISSIONS [M TONNES]', y_varname = 'tot_emissions', y_trim=100000)

    def between_msports_emissions(self):
        '''
        Makes violin plot by ship type of emissions from voyages that betwee MS ports.        
        '''
        
        return self.compile_violinplot(y_col = 'CO₂ EMISSIONS FROM ALL VOYAGES BETWEEN PORTS UNDER A MS JURISDICTION [M TONNES]', y_varname = 'tot_emissions_btw_MS_ports', y_trim=50000)

    def departed_msports_emissions(self): 
        '''
        Makes violin plot by ship type of emissions from voyages that departed from MS ports.
        '''
        
        return self.compile_violinplot(y_col = 'CO₂ EMISSIONS FROM ALL VOYAGES WHICH DEPARTED FROM PORTS UNDER A MS JURISDICTION [M TONNES]', y_varname = 'tot_emissions_departed_MS_ports', y_trim=25000)
        
    def within_msports_emissions(self):
        '''
        Makes violin plot by ship type of emissions within MS ports at berth.
        '''
        
        return self.compile_violinplot(y_col = 'CO₂ EMISSIONS WHICH OCCURRED WITHIN PORTS UNDER A MS JURISDICTION AT BERTH [M TONNES]', y_varname = 'tot_emissions_within_MS_ports', y_trim=10000)

    def annual_ave_emissions_per_distance(self):
        '''
        Makes violin plot by ship type of annual average emissions per distance.
        '''
        
        return self.compile_violinplot(y_col = 'ANNUAL AVERAGE CO₂ EMISSIONS PER DISTANCE [KG CO₂ / N MILE]', y_varname = 'annual_ave_emissions_dist', y_trim=2000)


    def compile_violinplot(self, y_col, y_varname, y_trim = None):
        '''
        Composer method for building violin plots to summarize "SHIP TYPE". 
        '''
        
        if y_trim is None:
            df_emissions_msports = self.data[['SHIP TYPE', y_col]].copy()
            df_emissions_msports.columns = ['type', y_varname]
        else: 
            df_emissions_msports = self.data[['SHIP TYPE', y_col]].copy()
            df_emissions_msports.columns = ['type', y_varname]
            df_emissions_msports = df_emissions_msports.loc[df_emissions_msports[y_varname] < y_trim]

        # figure size in inches
        # Should allow customization with input parameters (future)
        plt.rcParams['figure.figsize'] = 11.7,8.27

        p = sns.violinplot(data=df_emissions_msports, x = 'type', y = y_varname)
        plt.xticks(rotation=45)
        plt.xlabel("Ship Type")
        plt.ylabel("Total Emissions of CO2")
        plt.title(y_col)
        plt.ylim(0, )

        return p