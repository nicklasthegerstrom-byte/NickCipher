
#Här bor funktion för att skapa en nyckel (JSON)

"""
NickCipher format

En nyckel består av:
	•	en seed
	•	en mapping där varje tillåtet tecken mappar till exakt 5 unika emojis
	•	ett separat set med exakt 5 unika separator-emojis

Vid kodning ersätts varje tecken med en emoji vald från dess mapping.
Mellan varje token infogas en emoji vald från separator-setet.

Vid avkodning ignoreras separator-emojis helt och övriga emojis mappas entydigt tillbaka.

Varje emoji i systemet måste tillhöra exakt EN kategori.
"""

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
 "n","o","p","q","r","s","t","u","v","w","x","y","z",
 "å","ä","ö"]
sy

for a in alphabet:
    print(a)