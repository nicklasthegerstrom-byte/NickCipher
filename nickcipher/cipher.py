import random


class Emojicipher:
    
    def __init__(self, key:dict, password:int):
        
        self.key = key
        self.password = password

        reversed_key = {}
        for letter in key:
            for emoji in key[letter]:
                reversed_key[emoji] = letter

        self.reversed_key = reversed_key

    def encode(self, text:str) -> str:

        random.seed(self.password)
        encoded_result = ""

        for t in text:
            if t in self.key:
                t_emoji = random.choice(self.key[t])
                encoded_result += t_emoji

        return encoded_result
    
    def decode(self, emoji_code:str) -> str:

        random.seed(self.password)
        decoded_result = ""
        for e in emoji_code:
            if e in self.reversed_key:
                decoded_result += self.reversed_key[e]




    
