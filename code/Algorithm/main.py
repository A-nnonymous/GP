from PyTsetlinMachineCUDA.tm import RegressionTsetlinMachine
from PyTsetlinMachineCUDA.tools import Booleanizer
import numpy as np
from time import time
from sklearn.model_selection import train_test_split
import pandas as pd

f1=open("ConfirmedTimeSeriesFeature.csv","r")
data=pd.read_csv(f1).to_numpy()
f2=open("ConfirmedTimeSeriesOUT.csv","r")
target=pd.read_csv(f2)["Washington"].to_numpy()
X = data
Y = target

b = Booleanizer(max_bits_per_feature = 20)
b.fit(X)
X_transformed = b.transform(X)

tm = RegressionTsetlinMachine(10000, 500*10, 2.75)

print("\nRMSD over 25 runs:\n")
tm_results = np.empty(0)
for i in range(25):
	X_train, X_test, Y_train, Y_test = train_test_split(X_transformed, Y)

	start = time()
	tm.fit(X_train, Y_train, epochs=100)
	stop = time()
	tm_results = np.append(tm_results, np.sqrt(((tm.predict(X_test) - Y_test)**2).mean()))

	print("#%d RMSD: %.2f +/- %.2f (%.2fs)" % (i+1, tm_results.mean(), 1.96*tm_results.std()/np.sqrt(i+1), stop-start))
