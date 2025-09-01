
import json

with open ('pokemon.json', 'r', encoding ='utf-8') as archive:
    pokemon_list = json.load(archive)

name = input("Pokemon name: ")
type = input("Type, use comma for split: ").split(',')
hp = int(input("HP: "))
attack = int(input("Attack: "))
defense = int(input("Defense: "))
sp_attack = int(input("Sp. Attack: "))
sp_defense = int(input("Sp. Defense: "))
speed = int(input("Speed: "))

new_pokemon = {
    "name": {
        "english": name
    },
    "type": [t.strip() for t in type],  
    "base": {
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Sp. Attack": sp_attack,
        "Sp. Defense": sp_defense,
        "Speed": speed
    }
}

pokemon_list.append(new_pokemon)

with open('pokemon.json', 'w', encoding='utf-8') as archive:
    json.dump(pokemon_list, archive, indent=2, ensure_ascii=False)


print("New Pokemon Added!")