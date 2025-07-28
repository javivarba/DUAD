# main.py

from human_parts import Head, Hand, Arm, Feet, Leg, Torso, Human

head = Head()

left_hand = Hand()
right_hand = Hand()

left_arm = Arm(left_hand)
right_arm = Arm(right_hand)

left_feet= Feet()
right_feet= Feet()

left_leg= Leg(left_feet)
right_leg= Leg(right_feet)

torso = Torso(head, left_arm, right_arm, left_leg, right_leg)

human = Human(torso)

print(f"Human has {human.torso.head.eyes} eyes.")
print(f"Left hand has {human.torso.left_arm.hand.fingers} fingers.")
print(f"Right foot has {human.torso.right_leg.feet.toes} toes.")