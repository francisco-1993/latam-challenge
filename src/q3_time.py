from typing import List, Tuple
from collections import Counter, deque
from utils import custom_profilers, custom_extractors
import jsonlines


@custom_profilers.memory_profiler
@custom_profilers.exec_time_profiler
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    
    mention_counts = Counter()
    for tweet in custom_extractors.buffered_reader(file_path, buffer_size=1024*1000*20):
        top_mentions_users = deque()
        mentioned_users = tweet['mentionedUsers'] 
        if mentioned_users:
            for user in mentioned_users:
                top_mentions_users.append(user.get('username', None))
            mention_counts.update(filter(None, top_mentions_users))

    return mention_counts.most_common(10)