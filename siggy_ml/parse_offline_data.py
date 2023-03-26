import numpy as np 
import pandas as pd

wordlist_filename = "test_data.txt"
data_filename = "Fin_List_sent.xlsx"
outout_filename = ""

wordlist_df = pd.read_excel(wordlist_filename)
data = pd.read_csv(data_filename, sep = "	")

print(wordlist_df)
