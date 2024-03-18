from typing import List, Tuple
from collections import defaultdict
from heapq import nlargest
from utils import custom_profilers, custom_extractors
import jsonlines
import re

'''
    Acotaciones:
        - Al ser este un problema mas sencillo que q1 se opto por un Counter que es basicamente un diccionario optimizado para sacar cuentas de las llaves que
        lo componen 
        - Se opto por un lista comprensiva manejada de los patrones de emojis antes de librerias como "emoji" por el overhead inncesario que creo pueden agregar

'''

@custom_profilers.memory_profiler
@custom_profilers.exec_time_profiler
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u'\U00010000-\U0010ffff'
        u"\u200d"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\u3030"
        u"\ufe0f"
    "]+", flags=re.UNICODE)

    emoji_counts = defaultdict(int)

    with jsonlines.open(file_path, 'r') as file: 
        for tweet in file: 
            emojis = emoji_pattern.findall(tweet['content'])
            for emoji in emojis:
                emoji_counts[emoji] += 1

    return nlargest(10, emoji_counts.items(), key=lambda x: x[1])