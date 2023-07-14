class MissingnessProfiler:
    
    def __init__(self, data):
        self.data = data
        
    def summarize_missingness(self):
        print(self.data.isna().sum())
        
    def plot_missingness(self):
        from matplotlib import rcParams
        import matplotlib.pyplot as plt
        import seaborn as sns

        # figure size in inches
        plt.rcParams['figure.figsize'] = 11.7,8.27
        return sns.heatmap(self.data.isna(), cbar=False)