#human parts

class Head:
    def __init__(self):
        self.eyes= 2
        self.nose= 1
        self.mouth= 1

class Hand:
    def __init__(self):
        self.fingers= 5

class Arm:
    def __init__(self, hand: Hand):
        self.hand = hand

class Feet:
    def __init__(self):
        self.toes= 5

class Leg:
    def __init__(self, feet: Feet):
        self.feet = feet

class Torso:
    def __init__(self, head: Head, left_arm: Arm, right_arm: Arm, left_leg:Leg, right_leg:Leg):
        self.head = head
        self.left_arm= left_arm
        self.right_arm= right_arm
        self.left_leg= left_leg
        self.right_leg= right_leg
        

class Human:
    def __init__(self, torso: Torso):
        self.torso = torso