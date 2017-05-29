from random import randrange
import math
import matplotlib.pylab as pl
import sys
DiffW0 = 0
DiffW1 = 0
DiffW2 = 0
DiffWeigh = [0.0 for i in range(0, 3)]
LEARNING_RATE = 0.01
inputs = [[]]
totalSampleCount = 0
Attribute1 = []
Attribute2 = []
Output = []
maxIterations = 35


# Sigmoid function
def sigmoid(value):
    x = 1 / (1 + math.exp(-value))
    if(x >= 0.5):
        return 1
    return 0


def writeHeader(filename):
    file = open(filename, 'w')
    file.write("0,0,0,0,\n")


# records the weights of each iteration
def recordIterationValue(iteration, Weight, expectedOutput, actualOutput, filename, error):
    file = open(filename, 'a+')
    file.write(str(iteration) + ",")
    for w in Weight:
        file.write(str(w) + ",")
    # file.write(str(error))
    file.write("\n")


def updateDifferenceFactor(expectedValue, actualOutput, inputValue):
    for k in range(0, 3):
        DiffWeigh[k] += LEARNING_RATE * \
            (float(actualOutput) - float(expectedValue)) * inputValue[k]


# get the input data and
def getData(filename):
    global totalSampleCount, inputs, Output
    inputs = [[0 for j in range(0, 1)]for i in range(0, 100)]
    Output = [0 for j in range(0, 100)]
    X1 = [0.0 for j in range(0, 100)]
    X2 = [0.0 for j in range(0, 100)]
    # read data from the data file and store them in input and output vector
    for line in open(filename):
        X1[totalSampleCount], X2[totalSampleCount], Output[
            totalSampleCount] = line.split(",")
        totalSampleCount = totalSampleCount + 1
    for i in range(0, totalSampleCount):
        inputs[i] = 1.0, float(X1[i]), float(X2[i])


def plotGraph(iteration, plotArray):
    pl.figure()
    pl.xlim([0, maxIterations + 3])
    pl.title('Epoch vs Error-rate')
    pl.ylabel('Error- SSD')
    pl.xlabel('iterations')
    iterValue = [i for i in range(0, iteration)]
    pl.plot(iterValue, plotArray)
    pl.show()


def calculateError(hwX, Y):
    errorRate = 0
    for i in range(0, totalSampleCount):
        errorRate += math.pow((float(hwX[i]) - float(Y[i])), 2)
    return errorRate


def logicalRegression(filename):
    getData(filename)
    # Initialize random weights
    weight = [randrange(0, 100) / 100, randrange(0, 100) /
              100, randrange(0, 100) / 100]
    writeHeader("weights.csv")
    errorRate = [0 for i in range(0, maxIterations)]
    for iterations in range(0, maxIterations):
        # calculate expected value vector
        Calc_Output = [0.0 for i in range(0, 100)]

        #"Calculating Expected result"
        for sample in range(0, totalSampleCount):
            # h(x) = W. X : dot product
            for k in range(0, 3):
                Calc_Output[sample] += weight[k] * inputs[sample][k]
            # Squashing the obtained Calc_Output over sigmoid
            # update the difference quotient for every sample
            Calc_Output[sample] = sigmoid(Calc_Output[sample])
            updateDifferenceFactor(
                Calc_Output[sample], Output[sample], inputs[sample])
        # Update weights for each iteration
        for i in range(0, 3):
            weight[i] = weight[i] + DiffWeigh[i]
        # update error for each iteration
        errorRate[iterations] = calculateError(Calc_Output, Output)

        # Write the Weight summary to
        recordIterationValue(
            iterations, weight, Calc_Output, Output, "weights.csv", errorRate[iterations])
    plotGraph(maxIterations, errorRate)


def function(x1):
    for line in open("weights.csv"):
        i, w0, w1, w2, dummy = line.split(",")
    return (-float(w0) - float(w1) * float(x1)) / float(w2)


def expectedOutput(w0, w1, w2, x1, x2):
    return w0 + w1 * x1 + w2 * x2


def getBoundaryFromWeight(filename):
    getData(filename)
    pl.figure()
    pl.title('Decision boundary graph')
    pl.ylabel('Attribute 2')
    pl.xlabel('Attribute 1')
    pl.xlim(0, 10)
    pl.ylim(0, 10)
    wrongBcount = 0
    WrongXcount = 0
    for sample in range(0, totalSampleCount):
        # 0 denotes the test_append input
        if(inputs[sample][1] == 0):
            continue
        if(int(Output[sample]) == 1):
            if function(inputs[sample][1]) < inputs[sample][2]:
                WrongXcount = WrongXcount + 1
            pl.plot(inputs[sample][1], inputs[sample][2], 'rx')
        else:
            if function(inputs[sample][1]) > inputs[sample][2]:
                print(
                    inputs[sample][1], inputs[sample][2], "__", function(inputs[sample][1]))
                wrongBcount = wrongBcount + 1
            pl.plot(inputs[sample][1], inputs[sample][2], 'b.')
    print("Wrongly classified : Class-1", wrongBcount,
          "\n Wrongly classified Class-0", WrongXcount)
    # pl.show()
    min1 = 9999.0
    max1 = 0.0
    for i in range(0, totalSampleCount):
        if inputs[i][1] < min1:
            min1 = inputs[i][1]
        if inputs[i][1] > max1:
            max1 = inputs[i][1]
    X = [0 for i in range(0, int(max1) - int(min1))]
    Y = [0 for i in range(0, int(max1) - int(min1))]
    for i in range(int(min1), int(max1)):
        X[i] = i
        Y[i] = function(i)
    pl.plot(X, Y)
    pl.show()


# Uses logistic regression and find the weights and updates the weight of
# every epoche in the weights file
if len(sys.argv) != 2:
    print("usage python logreg.py <dataFile>")
    exit()
filename = sys.argv[1]
logicalRegression(filename)
print("Reading Weights and drawing graph")
# displays the decision boundary and the valueswrongly updated count
getBoundaryFromWeight(filename)
