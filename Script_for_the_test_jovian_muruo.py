# Script d'estimation de valeurs

# Import des bibliothèques
import numpy as np
from random import randint

# Start
print("Script is starting")

# Test libraries
x = np.zeros(5) # (install numpy)
randint(0, 10)

# Load data

database = np.genfromtxt("Sample.csv", delimiter=",")
nbRows, _ = database.shape

def monteCarlo(colIdx, nbVal = 12):
	"""
	Return an array of random selected values.
	"""
	ans = np.zeros(nbVal)
	randIdx = 0

	for k in range(nbVal):
		randIdx = randint(0, nbRows - 1)
		ans[k] = database[randIdx, colIdx]

	return ans

def computeMax(tab1, tab2, nbVal = 12):
	"""
	Compute max for each case
	"""
	ans = np.zeros(nbVal)

	for k in range(nbVal):
		ans[k] = max(tab1[k], tab2[k])

	return ans

def computeV1(tab, amount):
	"""
	Compute V1 from a income array
	"""
	# Loop
	V1 = amount

	for k in range(12):
		V1 = V1 * (1.0 + tab[k])

	return V1

def computeV0(V1, rf):
	return V1 / (1.0 + rf)

def estimateOnce(rf, amount, keepV1):
	"""
	Make one MonteCarlo trajectory and return V0
	"""

	# Use random
	monteCarloWTI = monteCarlo(0)
	monteCarloCAC40 = monteCarlo(1)

	# Compute income
	basket = computeMax(monteCarloWTI, monteCarloCAC40)

	# Get V1
	V1 = computeV1(basket, amount)

	# Bypass V0
	if keepV1 :
		return V1

	# Get V0
	return computeV0(V1, rf)

def meanSeveralTimes(N, rf = 0.25 / 100, amount = 100000.0, keepV1 = False):
	""" 
	Make a computation N times and return the mean
	"""
	total = 0.0

	for k in range(N):
		total += estimateOnce(rf, amount, keepV1)

	return total / N

def meanSeveralTimesWithOption(N, rf = 0.25 / 100, amount = 100000.0, keepV1 = False, lmin = -5.0 / 100.0, lmax = 10.0 / 100.0):
	""" 
	Make a computation N times and return the mean
	takes in to account limits max and min
	"""
	total = 0.0

	for k in range(N):
		delta = estimateOnce(rf, amount, keepV1) - amount;

		if delta > amount * lmax :
			delta = amount * lmax

		if delta < amount * lmin :
			delta = amount * lmin

		total += amount + delta

	return total / N

def space():
	print("- - - - - - - - - - ", end='\n')

# Examples
space()
print("Parameters")
riskFreeRate = 0.25 / 100
baseAmount = 100000.0
N = 10000

print("riskFreeRate : ", riskFreeRate)
print("baseAmount : ", baseAmount, end="\n")
print("number of iterations", N)
space()

print("[Step 1]")
print("Compute a random trajectory")
V1 = estimateOnce(riskFreeRate, baseAmount, keepV1 = True)
print("V1 : ", V1)
V0 = computeV0(V1, riskFreeRate)
print("V0 : ", V0)
space()

print("[Step 2]")
print("Mean of V0 for ", N, " computations")
print("Computation in progress ...")
V0mean = meanSeveralTimes(N, rf = riskFreeRate, amount = baseAmount);
print("V0 mean : ", V0mean)
print("Rate mean : ", (V0mean - baseAmount) / baseAmount * 100.0, "%")
space()

print("[Step 3]")
print("Compute V0bis = E(V1) / (1 + rf)")
print("Computation in progresss ...")
EV1 = meanSeveralTimes(N, rf = riskFreeRate, amount = baseAmount, keepV1 = True)
V0bis = EV1 / (1 + riskFreeRate)

print("V0bis : ", V0bis)
space()

print("[Step 4]")
print("Iplement the min max option.")
limitMax = 10.0
limitMin = -5.0
print("Option between ", limitMin, "%", " and ", limitMax, "%")
print("Computation in progresss ...")
Eopt = meanSeveralTimesWithOption(N, rf = riskFreeRate, amount = baseAmount, lmin = limitMin / 100.0, lmax = limitMax / 100.0)
print("Mean with option ", Eopt)

space()
print("End of programm")