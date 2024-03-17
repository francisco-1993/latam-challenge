from cProfile import Profile as cProfile
from pstats import Stats, SortKey
from functools import wraps
from typing import Callable
from memray import Tracker, FileDestination
import os

def exec_time_profiler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        with cProfile() as profiler:
            result = func(*args, **kwargs)
        print(f'Execution time for {func.__name__}:')
        stats = Stats(profiler).sort_stats(SortKey.TIME)
        stats.print_stats()
        
        return result
    return wrapper

def memory_profiler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        directory='memory_tracks_files/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with Tracker(destination=FileDestination(f'{directory}{func.__name__}.bin', overwrite=True)):
            result = func(*args, **kwargs)
        return result
    return wrapper


