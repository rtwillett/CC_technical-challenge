from modules.loaders import LoadData
from modules.cleaning import detect_pattern
from modules.cleaning import MRVCleaner

loader = LoadData()

cleaner = MRVCleaner(loader.data)
cleaner.data.to_csv("./refined_data/eu-mrv.csv", index=False)
