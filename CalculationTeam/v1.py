#This is version 1 of the code, intended as a draft

# -- Constants
mpt = 20 #metres per thingy
maxCount = 10 #Number of matches to be combined into one average for later calculations

speedSum = 0
speedCount = 0
count = 0
ydifSum = 0
xdifSum = 0

gradientChange = []
speedChange = []

def inputFunction(input):
    #input[0] = [x1, y1]
    #input[1] = [x2, y2]
    #input[2] = time
    count += 1
    x1 = input[0][0]
    y1 = input[0][1]
    x2 = input[1][0]
    y2 = input[1][1]
    time = input[2]
    xdif = x1 - x2
    ydif = y1 - y2
    xdifSum += xdif
    ydifSum += ydif
    distance = (((xdif ** 2) + (ydif ** 2)) ** 0.5) * mpt
    speed = distance / time
    #Rotation spin of Earth ~ 470 m/s, estimated ISS speed ~ 7660 m/s, hence large error margins
    if speed < 8200 and speed > 7100:
        speedSum += speed
        speedCount += 1
    if count == maxCount:
        averageFunction()

def averageFunction():
    if speedCount != 0:
        speedAverage = speedSum / speedCount
        speedChange.append(speedAverage)
        gradientAverage = ydifSum / xdifSum
        gradientChange.append(gradientAverage)
    speedSum = 0
    speedCount = 0
    count = 0
    ydifSum = 0
    xdifSum = 0