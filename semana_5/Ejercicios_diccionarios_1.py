
#Practice Dictionary

hotel= {
    "name": " Palace",
    "stars_rating" : 4,
    "rooms" : [
        {"number" : 101, "floor" : 1, "rate" : 110.5},
        {"number" : 102, "floor" : 1, "rate" : 120.5},
        {"number" : 201, "floor" : 2, "rate" : 210.5},
    ]
}

print("Hotel", hotel["name"])
print ("Star rating is",hotel ["stars_rating"])

for rooms in hotel ["rooms"]:
    print (f"Room {rooms ["number"]} in the floor {rooms ["floor"]} cuesta {rooms ["rate"]} per night")