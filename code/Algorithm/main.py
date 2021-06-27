from PyTsetlinMachineCUDA.tm import RegressionTsetlinMachine
from PyTsetlinMachineCUDA.tools import Booleanizer
#from pyTsetlinMachineParallel.tm import  RegressionTsetlinMachine
#from pyTsetlinMachineParallel.tools import Binarizer
import numpy as np
from time import time
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

f1=open("../dataPool/win/data.csv","r")
data=pd.read_csv(f1)[['people_vaccinated_per_hundred',
          'people_fully_vaccinated_per_hundred',
          'people_vaccinated',
          'confirmed']].to_numpy()
f2=open("../dataPool/win/death.csv","r")
target=pd.read_csv(f2).to_numpy().flatten()

X = data
Y =target

b = Booleanizer(max_bits_per_feature = 10)
#b= Binarizer(max_bits_per_feature=32)
b.fit(X)
X_transformed = b.transform(X)

############################Description of argument###############################
# Clauses:
# 	Num of clauses,decides the expression power of the RTM
# T:
# 	A larger T requires more literal products to reach a particular value y.
# 	Thus, increasing T makes the regression function increasingly fine-grained
#	A higher T reduces the overall probability of feedback, resulting in more conservative learning
#   Produces an ensemble effect by stimulating up to T clauses to output 2 for each input, but
# 	not more than T
# s:
# 	Type Ib feedback is provided to TAs stochastically using this user set parameter
#	Is used by the TM to control the granularity of the clauses, playing a similar role as so-called
#	support in frequent itemset mining
#	Controls how fine-grained patterns the TM seeks
############################Description ends here##################################
tm = RegressionTsetlinMachine(8000, 4000,12.5,max_weight=4)
#tm = RegressionTsetlinMachine(80000, 20000,32,max_weight=14,number_of_state_bits=6)

print("\nRMSD per runs:\n")
tm_results = np.empty(0)

X_train, X_test, Y_train, Y_test = train_test_split(X_transformed, Y)

tm.fit(X_train, Y_train, epochs=100)


tm_results = np.append(tm_results, np.sqrt(((tm.predict(X_test) - Y_test)**2).mean()))
out=pd.DataFrame(tm.predict(X)).to_csv("output.csv")
print("RMSD: %.2f " % (tm_results.mean()))
