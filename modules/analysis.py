class MissingnessProfiler:
    
    def __init__(self, data):
        self.data = data
        
    def summarize_missingness(self):
        '''
        For numerically summarizing missingness of data from each column of a data frame. 
        '''
        
        print(self.data.isna().sum())
        
    def plot_missingness(self):
        '''
        Creates a black-white tile mosaic for data that is present and missing. This is a useful way to inspect the
        structure and patterns of missingness from small to medium data sets.
        '''
        
        from matplotlib import rcParams
        import matplotlib.pyplot as plt
        import seaborn as sns

        # figure size in inches
        plt.rcParams['figure.figsize'] = 11.7,8.27
        return sns.heatmap(self.data.isna(), cbar=False)