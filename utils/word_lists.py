
objects = ["cactus","turtle","bowl of soup","block of ice","barrel of monkeys",
           "statue","boulder","Toyota Camry","washing machine","vacant doghouse","baseball","basketball",
           "football","tennis ball","golf ball","recliner","television","record player","magic mirror",
           "broken treadmill","villainous character","stunt-seeking daredevil","Minecraft villager",
           "mischievious rapscalion","clown","giant spider","miniature elephant","kitschy porcelain figurine","priceless artifact",
           "crown jewel","tuba","snare drum","block of concrete","kindergartener's action figure","bonsai tree", 
           "The Infamous Epi Demick","box of tnt"
           ]

proj_verbs = ["catapulted","cannon-fired","launched","chucked","thrown","propelled","kaboomed into the air",
              "hurled","pitched","tossed","flung","lobbed","blasted","ejected","deployed",
              "heaved","set into motion","put into flight","sent skyward"
              ]

def random_noun():
    import random
    return random.choice(objects)

def random_proj_verb():
    import random
    return random.choice(proj_verbs)