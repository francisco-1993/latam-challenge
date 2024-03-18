from typing import List, Tuple
from collections import Counter
from utils import custom_profilers, custom_extractors
import jsonlines
import re


@custom_profilers.memory_profiler
@custom_profilers.exec_time_profiler
def q2_time(file_path: str) -> List[Tuple[str, int]]:

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

    emoji_counts = Counter()

    for tweet in custom_extractors.buffered_reader(file_path, buffer_size=1024*1000*20):      
        emojis = emoji_pattern.findall(tweet['content'])
        emoji_counts.update(emojis)

    return emoji_counts.most_common(10)