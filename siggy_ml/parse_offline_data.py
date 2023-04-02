import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
# from erp_classifier import stupid_clf
import bisect 

wordlist_filename = "Fin_List_sent.csv"
timestamp_filename = "test_timestamps.csv"
data_filename = "test_data.txt"

wordlist_df = pd.read_csv(wordlist_filename)
wordlist_df.columns = ['sentence', 'word', 'prob']

def check_word(w):
	return w in wordlist_df['word'].to_numpy()

data = pd.read_csv(data_filename, sep = "	")
# add data columns
new_columns = [x for x in range(len(data.columns))]

new_columns[1] = 'P3'
new_columns[2] = 'Fz' # actually is Pz
new_columns[3] = 'P4'
new_columns[4] = 'C3'
new_columns[5] = 'Cz'
new_columns[6] = 'C4'
new_columns[-2] = 'time'

data.columns = new_columns


timestamp_df = pd.read_csv(timestamp_filename, keep_default_na=False)
timestamp_df.columns = ["word", "time"]

left_interval = 0.2 # to check
right_interval = 0.8 # to check

X = []
y = []
data_times = data['time'].to_numpy()
print(data_times[0])
print(data_times[-1])
print(1/(data_times[1] - data_times[0]))

for index, row in timestamp_df.iterrows():
	if row['word'] != "":
		left = bisect.bisect_left(data_times, int(row['time']) / 10**6 - left_interval)
		right = bisect.bisect_right(data_times, int(row['time']) / 10**6 + right_interval)
		print(left, right)

		# make sure to append in the right order (Cz, C3, C4, Fz, P3, P4)
		X.append([data['Cz'].to_numpy()[left:right], data['C3'].to_numpy()[left:right], data['C4'].to_numpy()[left:right], data['Fz'].to_numpy()[left:right], data['P3'].to_numpy()[left:right], data['P4'].to_numpy()[left:right]])
		y.append(check_word(row['word']))

print(len(X), len(X[0]), len(X[0][0]))
print(np.array(y).shape)

# plt.plot(X[0][0])
# plt.plot(X[0][1])
# plt.show()
# need to pad X, or change something...

np.save('X_' + str(data_filename), X) 
np.save('y_' + str(data_filename), y)
# clf = stupid_clf()
# processed = clf.preprocess(np.array([sample]))
# print(processed.shape)
# plt.plot(processed[0])
# plt.show()

# note: will need to resample this data to 256 Hz when calling the model