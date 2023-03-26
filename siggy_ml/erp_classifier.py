import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from tsfresh import extract_features

class classifier:
	def __init__(self, sampling_rate = 256, offset = 0.2):
		self.sampling_rate = sampling_rate
		self.offset = offset

	def preprocess(self, data, lower = 0.5, upper = 40):
		# apply some filters/interpolation/resampling/smoothing/transform

		data -= np.expand_dims(np.mean(data, axis = -1), -1)
		nyquist = self.sampling_rate / 2
		b,a = iirnotch(60, 30, self.sampling_rate)
		data = filtfilt(b, a, data)
		b, a = butter(4, [lower / nyquist, upper / nyquist], 'bandpass', analog=False)
		data = filtfilt(b, a, data)
		return data

	def predict(self, sample): # implement in child class
		pass

	def test(self, test_X, test_y):
		# outputs accuracy and confusion matrix for given test data

		preds = self.predict(test_X)
		accuracy = accuracy_score(test_y, preds)
		print("Accuracy:", accuracy)

		confusion = confusion_matrix(test_y, preds)
		print("Confusion Matrix:")
		print(confusion)
		cm_display = ConfusionMatrixDisplay(confusion_matrix = confusion, display_labels = [False, True])
		cm_display.plot()
		plt.show()

		return accuracy, confusion

class stupid_clf(classifier):
	def predict(self, X):
		X = self.preprocess(X)

		mu = np.mean(X, axis = 1)
		avg_range = (np.array([0.3, 0.5]) + self.offset)*self.sampling_rate
		# print(np.linspace(-0.2, 0.8, 256)[int(avg_range[0])])
		# print(np.linspace(-0.2, 0.8, 256)[int(avg_range[1])])

		n400_mean = np.mean(X[:, int(avg_range[0]): int(avg_range[1])], axis = 1)

		return np.greater(mu, n400_mean).astype(int)

class feature_SVC(classifier):
    def __init__(self, features = ['0__fft_coefficient__attr_"real"__coeff_1', '0__fft_coefficient__attr_"angle"__coeff_1', '0__fft_coefficient__attr_"imag"__coeff_1', '0__quantile__q_0.6', '0__median', '0__quantile__q_0.7', '0__fft_coefficient__attr_"real"__coeff_0', '0__sum_values', '0__mean', '0__quantile__q_0.4']):
        super().__init__()
        self.model = SVC()
        self.features = features

    def preprocess(self, x):
        x_df = pd.DataFrame(x[0].T)
        x_df["time"] = [i for i in range(x.shape[1])]
        x_df["id"] = 0

        for i in range(1, x.shape[0]):
            to_add = pd.DataFrame(x[i])
            to_add["id"] = i
            to_add["time"] = [x for x in range(x.shape[1])]
            x_df = pd.concat([x_df, to_add])

        out = extract_features(x_df, column_id= "id", column_sort = "time")
        return out[self.features]

    def predict(self, X):
        return self.model.predict(self.preprocess(X))

    def train_model(self, train_X, train_y):
        self.model.fit(self.preprocess(train_X), train_y)

class feature_RF(feature_SVC):
	def __init__(self, features = ['0__fft_coefficient__attr_"real"__coeff_1', '0__fft_coefficient__attr_"angle"__coeff_1', '0__fft_coefficient__attr_"imag"__coeff_1', '0__quantile__q_0.6', '0__median', '0__quantile__q_0.7', '0__fft_coefficient__attr_"real"__coeff_0', '0__sum_values', '0__mean', '0__quantile__q_0.4']):
		self.sampling_rate = sampling_rate
		self.offset = offset
		self.model = RandomForestClassifier()
		self.features = features

class peak_SVC(classifier):
    def __init__(self):
        super().__init__()
        self.model = SVC()
        
    def preprocess(self, x):
        peak_dataset = []

        for i in range(len(x)):
            sample = -super().preprocess(x[i], upper = 10)
            peaks, _ = find_peaks(sample)
            peaks = peaks[peaks < self.sampling_rate*(self.offset + 0.5)]
            peaks = peaks[peaks > self.sampling_rate*(self.offset + 0.3)]

            if len(peaks) == 0:
                peaks = [0.6*256, -20]
            else:
                max_p = peaks[0]
                for p in peaks[1:]:
                    if sample[p] > max_p:
                        max_p = p

                peaks = [max_p, sample[max_p]]


            peak_dataset.append(peaks)
            
        return peak_dataset

    def predict(self, X):
        return self.model.predict(self.preprocess(X))

    def train_model(self, train_X, train_y):
        self.model.fit(self.preprocess(train_X), train_y)


class ensemble_classifier(classifier):
	def __init__(self, classifier_list):
		super().__init__()
		self.classifier_list = classifier_list

	def predict(self, X):
		return np.round(np.mean([c.predict(X) for c in classifier_list]))


if __name__ == '__main__':
	clf = stupid_clf()
	# raw = np.random.randn(5, 6, 256)
	raw = np.load('multichannel_dataset/X_test.npy')
	plt.plot(raw[0, 0])

	# plt.show()
	out = clf.preprocess(raw)
	plt.plot(out[0,0])
	# print(out)
	plt.show()

	# print(clf.predict(raw))
	# test_y = np.random.randint(low = 0, high = 2, size = 20)
	# clf.test(raw, test_y)

	# plt.plot(out[0])
	# plt.plot(raw[0])
	# plt.show()

	# clf2 = stupid_clf()
	# clf3 = stupid_clf()
	# ens = ensemble_classifier(classifier_list = [clf, clf2, clf3])
	# clf.test(raw, test_y)