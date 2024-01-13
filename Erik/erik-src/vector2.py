import math

class vector2:
    x, y = 0, 0
    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)    
    @property
    def magnitudeSquared(self):
        return self.x**2 + self.y**2
    @property
    def angle(self):
        return math.atan2(self.y, self.x)
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __init__(self):
        self.x = 0
        self.y = 0
    @staticmethod 
    @property
    def identity():
        return Vector2(0, 0)
    
    def dot(self, other):
        return self.x * other.X + self.y * other.Y
    def __add__(self, other):
        return Vector2(self.x + other.X, self.y + other.Y)
    def __sub__(self, other):
        return Vector2(self.x - other.X, self.y - other.Y)
    def scale(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)    
    def translate(self, x, y):
        return Vector2(self.x + x, self.y + y)
    def translateSelf(self, x, y):
        self.x += x
        self.y += y
    def addSelf(self, other):
        self.x += other.X
        self.y += other.Y
    def subSelf(self, other):
        self.x -= other.X
        self.y -= other.Y
    def scaleSelf(self, scalar):
        self.x *= scalar
        self.y *= scalar
    def distance(self, other):
        return math.sqrt((self.x - other.X)**2 + (self.y - other.Y)**2)
    def distanceSquared(self, other):
        return (self.x - other.X)**2 + (self.y - other.Y)**2
    def __str__(self):
        return "vector2({0}, {1})".format(self.x, self.y)
    