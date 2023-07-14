from modules.loaders import LoadData
from modules.cleaning import detect_pattern
from modules.cleaning import MRVCleaner

loader = LoadData()

cleaner = MRVCleaner(loader.data)
cleaner.data.to_csv("./refined_data/clean_data.csv", index=False)