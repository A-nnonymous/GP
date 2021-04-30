from pyTsetlinMachineParallel.tm import RegressionTsetlinMachine
from pyTsetlinMachineParallel.tools import Binarizer
import numpy as np
from time import time
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

f1=open("TFeatures.csv","r")
data=pd.read_csv(f1).to_numpy()
f2=open("TTarget.csv","r")
target=pd.read_csv(f2).to_numpy().flatten()

X = data
Y =target

b = Binarizer(max_bits_per_feature = 16)
b.fit(X)
X_transformed = b.transform(X)

tm = RegressionTsetlinMachine(80000, 20000,32,weighted_clauses=True)

print("\nRMSD over 25 runs:\n")
tm_results = np.empty(0)
for i in range(25):
	X_train, X_test, Y_train, Y_test = train_test_split(X_transformed, Y)

	start = time()
	tm.fit(X_train, Y_train, epochs=20)
	stop = time()

	tm_results = np.append(tm_results, np.sqrt(((tm.predict(X_test) - Y_test)**2).mean()))
	out=pd.DataFrame(tm.predict(X)).to_csv("output.csv")
	print("#%d RMSD: %.2f +/- %.2f (%.2fs)" % (i+1, tm_results.mean(), 1.96*tm_results.std()/np.sqrt(i+1), stop-start))
