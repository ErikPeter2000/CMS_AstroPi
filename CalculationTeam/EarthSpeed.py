import math

radius = 6371 #metres
spinTime = 86400 #seconds
maxInclination = 51.6 #degrees
currentInclination = 0 #degrees
matchSpeed = 0 #metres per second

#the variable currentInclination should be set to the ISS's current latitude in degrees
#the variable matchSpeed should be set to the aquired speed value from the matching points

def calculate(radius, spinTime, maxInclination, currentInclination, matchSpeed):
    newRadius = radius * math.cos(math.radians(currentInclination)) #radius of Earth relative to the ISS parallel to the equator
    newCircumference = math.pi * (newRadius ** 2) #circumference of Earth at this point
    newEarthSpeed = newCircumference / spinTime #speed of Earth at this point
    currentAngle = maxInclination - abs(currentInclination) #angle between Earth velocity and ISS velocity
    aC = math.pi - math.radians(currentAngle) #angle for velocity triangle
    a = newEarthSpeed #side for velocity triangle
    c = matchSpeed #side for velocity triangle
    newSpeed = (c * math.sin(math.pi - aC - math.asin((a * math.sin(aC)) / c))) / (math.sin(aC)) #velocity triangle and trigonometry
    return newSpeed #returns the adjusted speed in metres per second