import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
# from erp_classifier import stupid_clf
import bisect 
from scipy.interpolate import interp1d
import re

def parse(data_filename, wordlist_filename, timestamp_filename):

	wordlist_df = pd.read_csv(wordlist_filename)
	wordlist_df.columns = ['sentence', 'word', 'prob']

	def check_word(w):
		return re.sub('[^a-zA-Z]+', '', w) in wordlist_df['word'].to_numpy()

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

	channel_list = ['Cz', 'C3', 'C4', 'Fz', 'P3', 'P4'] # in order

	for index, row in timestamp_df.iterrows():
		if row['word'] != "":
			left = bisect.bisect_left(data_times, int(row['time']) / 10**6 - left_interval)
			right = bisect.bisect_right(data_times, int(row['time']) / 10**6 + right_interval)

			# make sure to append in the right order (Cz, C3, C4, Fz, P3, P4)
			if right - left != 0:
				to_append = []
				for channel in channel_list:
					interp = interp1d(np.linspace(start = 0, stop = 1, num = (right - left)), data[channel].to_numpy()[left:right])
					interpolated_data = interp(np.linspace(start = 0, stop = 1, num = 256))
					to_append.append(interpolated_data)

			X.append(to_append)
			print(row['word'], check_word(row['word']))
			y.append(check_word(row['word']))

	return np.array(X), np.array(y)

def save_parse(data_filename, wordlist_filename, timestamp_filename):
	X, y = parse(data_filename, wordlist_filename, timestamp_filename)
	np.save('X_' + str(data_filename).split(".")[0], np.array(X)) 
	np.save('y_' + str(data_filename).split(".")[0], np.array(y))

def save_parse_files(data_filenames, wordlist_filenames, timestamp_filenames, output_filename):
	X = []
	y = []
	for i in range(data_filenames):
		X_a, y_a = parse(data_filenames[i], wordlist_filenames[i], timestamp_filenames[i])
		X.append(X_a)
		y.append(y_a)

	print(np.array(X).shape)



if __name__ == '__main__':
	wordlist_filename = "Fin_List_sent.csv"
	timestamp_filename = "test_timestamps.csv"
	data_filename = "test_data.txt"
	save_parse(data_filename, wordlist_filename, timestamp_filename)