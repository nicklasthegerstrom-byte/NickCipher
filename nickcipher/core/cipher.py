import random

class StaticEmojiCipher:
    
    def __init__(self, key:dict):
        
        self.key = key

        reversed_key = {}
        for letter in key:
            for emoji in key[letter]:
                reversed_key[emoji] = letter

        self.reversed_key = reversed_key

    def encode(self, text:str) -> str:

        encoded_result = ""

        for t in text:
            if t in self.key:
                t_emoji = random.choice(self.key[t])
                encoded_result += t_emoji

        return encoded_result
    
    def decode(self, emoji_code:str) -> str:

        decoded_result = ""
        for e in emoji_code:
            if e in self.reversed_key:
                decoded_result += self.reversed_key[e]


class DynamicEmojiCipher:

    def __init__(self, emoji_pool, weights):

        self.emoji_pool = emoji_pool
        self.weights = weights
        self.key = None
        self.reversed_key = None
        

    def generate_key(self, password):

        required_emojis = sum(self.weights.values())

        if len(self.emoji_pool) < required_emojis:
            raise ValueError("Not enough emojis in pool")
       
        random.seed(password)
        remaining_pool = self.emoji_pool.copy()
        self.key = {}
       
        for char in self.weights:
           amount = self.weights[char]
           chosen_emojis = random.sample(remaining_pool, amount)
           self.key[char] = chosen_emojis
           remaining_pool = [e for e in remaining_pool if e not in chosen_emojis]

        self.reversed_key = {}
        for letter in self.key:
            for emoji in self.key[letter]:
                self.reversed_key[emoji] = letter

    
    def encode(self, text:str):

        if self.key is None:
            raise ValueError("No key generated")
        
        encoded_result =""

        for t in text.lower():

            if t not in self.key:
                print(f"VARNING: Tecknet '{t}' (unicode: {ord(t)}) saknas i nyckeln! Använder fallback.")
            # Om tecknet inte finns i din weights/key, använd fallback-tecknet "$"
            target = t if t in self.key else "$"
            
            # Välj en slumpmässig emoji från poolen för det tecknet
            t_emoji = random.choice(self.key[target])
            encoded_result += t_emoji
            
        return encoded_result
    
    def decode(self, text:str):

        if self.reversed_key is None:
            raise ValueError("No decode key generated")
        
        decoded_result = ""
        for e in text:
            if e in self.reversed_key:
                decoded_result += self.reversed_key[e]

        return decoded_result
