import random


class Emojicipher:
    
    def __init__(self, key:dict, password:int):
        
        self.key = key
        self.password = password

    def encode(self, text:str) -> str:

        random.seed(self.password)
        encoded_result = ""

        for t in text:
            if t in self.key:
                t_emoji = random.choice(self.key[t])
                encoded_result += t_emoji

        return encoded_result


    
