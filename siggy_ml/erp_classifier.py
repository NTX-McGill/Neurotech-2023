import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

class classifier:
	def __init__(self, sampling_rate = 256, offset = 0.2):
		self.sampling_rate = sampling_rate
		self.offset = offset

	def preprocess(self, data):
		# apply some filters/interpolation/resampling/smoothing/transform
		nyquist = self.sampling_rate / 2
		b,a = iirnotch(60, 30, self.sampling_rate)
		data = filtfilt(b, a, data)

		b, a = butter(4, [0.5 / nyquist, 20 / nyquist], 'bandpass', analog=False)
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
		n400_mean = np.mean(X[:, int(avg_range[0]): int(avg_range[1])], axis = 1)

		return np.greater(n400_mean, mu).astype(int)

class avg_ANOVA(classifier):
	def predict(self, X):
		pass

class waveform_random_forest(classifier):
	def __init__(self):
		super().__init__()
		self.model = None

	def preprocess(self, data):
		pass

	def predict(self, X):
		pass

	def train_model(train_X, train_y):
		pass

class ensemble_classifier(classifier):
	def __init__(self, classifier_list):
		super().__init__()
		self.classifier_list = classifier_list

	def predict(self, X):
		return np.round(np.mean([c.predict(X) for c in classifier_list]))


if __name__ == '__main__':
	clf = stupid_clf()
	raw = np.random.randn(20, 256)
	out = clf.preprocess(raw)

	print(clf.predict(raw))
	test_y = np.random.randint(low = 0, high = 2, size = 20)
	clf.test(raw, test_y)

	plt.plot(out[0])
	plt.plot(raw[0])
	plt.show()

	# clf2 = stupid_clf()
	# clf3 = stupid_clf()
	# ens = ensemble_classifier(classifier_list = [clf, clf2, clf3])
	# clf.test(raw, test_y)