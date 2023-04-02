import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
# from erp_classifier import stupid_clf 

wordlist_filename = "Fin_List_sent.csv"
timestamp_filename = "timestamps/"
data_filename = "test_data.txt"
output_filename = ""

wordlist_df = pd.read_csv(wordlist_filename)
wordlist_df.columns = ['sentences', 'words', 'prob']
data = pd.read_csv(data_filename, sep = "	")

def check_word(w):
	return w in wordlist_df['words'].to_numpy()

print(check_word('banana'), check_word('clook'))

channels = []

sample = data.iloc[:, 3].to_numpy()
plt.plot(sample)
# clf = stupid_clf()
# processed = clf.preprocess(np.array([sample]))
# print(processed.shape)
# plt.plot(processed[0])
plt.show()