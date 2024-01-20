#This is version 1 of the code, intended as a draft
#Input is expected as an array with one match as follows: [[x_value_1, y_value_1], [x_value_2, y_value_2], time_period, timestamp]

# -- Global Variables
#Constants
mpu = 20 #metres per unit given
maxCount = 10 #Number of matches to be averaged into one value to be used to find a trend
minSpeed = 7100 #Rotation spin of Earth ~ 400 to 500 m/s, estimated ISS speed ~ 7600 to 7700 m/s, lower margin ~ 7100 m/s
maxSpeed = 8200 #Rotation spin of Earth ~ 400 to 500 m/s, estimated ISS speed ~ 7600 to 7700 m/s, upper margin ~ 8200 m/s

#Average variables
matchCount = 0 #Current number of matches to track when to calculate an average
speedSum = 0 #Sum of calculated speed to find average
ydifSum = 0 #Sum of change in y-value for gradient average
xdifSum = 0 #Sum of change in x-value for gradient average
timestampSum = 0 #Sum of timestamps for average match time

#Final values
gradientChange = [] #The change in average gradient of the speed of the ISS over time
speedChange = [] #The change in average speed of the ISS over time
timestamps = [] #Timestamps for speed and gradient changes
# --

#Function called with each match
def inputFunction(input):
    x1 = input[0][0] #point 1 x-value
    y1 = input[0][1] #point 1 y-value
    x2 = input[1][0] #point 2 x-value
    y2 = input[1][1] #point 2 y-value
    time = input[2] #match time difference
    timestamp = input[3] #timestamp of match
    xdif = x1 - x2 #change in x
    ydif = y1 - y2 #change in y
    distance = (((xdif ** 2) + (ydif ** 2)) ** 0.5) * mpu #pythagoras
    speed = distance / time
    if speed < maxSpeed and speed > minSpeed: #check if calculated speed is within sensible range
        xdifSum += xdif
        ydifSum += ydif
        speedSum += speed
        timestampSum += timestamp
        matchCount += 1
    if matchCount == maxCount:
        average()

#Function to create combined match average
def average():
    speedChange.append(speedSum / matchCount) #Average speed
    gradientChange.append(ydifSum / xdifSum) #Average gradient
    timestamps.append(timestampSum / matchCount) #Average timestamp
    #Resetting variables
    matchCount = 0
    speedSum = 0
    ydifSum = 0
    xdifSum = 0
    timestampSum = 0