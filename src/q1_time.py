from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, deque
from heapq import nlargest
from utils import custom_profilers, custom_extractors
import json


#@custom_profilers.memory_profiler
@custom_profilers.exec_time_profiler

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_counts = defaultdict(int)
    user_counts = defaultdict(lambda: defaultdict(int))

    for tweet in custom_extractors.buffered_reader(file_path, buffer_size=1024*1000*20):
        date = datetime.strptime(tweet['date'][:10],'%Y-%m-%d').date() #datetime.strptime(tweet['date'][:10], '%Y-%m-%d').date() #tweet['date'][:10] 
        user = tweet['user']['username']
        date_counts[date] += 1
        user_counts[date][user] += 1

    top_dates = nlargest(10, date_counts, key=date_counts.get)

    result = deque()
    for date in top_dates:
        top_user = max(user_counts[date], key=user_counts[date].get)
        result.append((date, top_user))

    return result



###############################################################################################
#intento con dask, para aprovechar de procesar en paralelo
#status: No funcional
#estuve iterando entre to many values to unpack, colocando filtros en la data para cubrir dichos errores, finalmente logre ejecutar aunque retorna una lista vacia


# from dask import bag as db
# from dask.distributed import Client, LocalCluster
# def process_tweet(tweet):
#     try:
#         date = datetime.strptime(tweet['date'][:10], '%Y-%m-%d').date()
#         user = tweet['user']['username']
#         return date, user
#     except (KeyError, ValueError, TypeError):
#         pass


# def aggregate_counts(tweet_data):

#     dates_users_counts = {}

#     for tweet in tweet_data:
#         date, user = tweet
#         #surgio de posible error que crei podia estar en la data, no obstante, si bien no fue asi, se deja para manejar casos donde objetos no tengan alguno de los valores o llaves
#         if isinstance(tweet, tuple) and len(tweet) == 2:
#             if date not in dates_users_counts:
#                 dates_users_counts[date] = {'total_count': 0, 'user_counts': {}} #inicialización de dict si no hay llave
#             dates_users_counts[date]['total_count'] += 1
#             dates_users_counts[date]['user_counts'][user] = dates_users_counts[date]['user_counts'].get(user, 0) + 1

#     return dates_users_counts


# def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:

#     #'http://127.0.0.1:8787/status' - ruta dashboard
#     # valores seteados son los que por defecto son utilizados en general
#     with Client(LocalCluster(n_workers=4, memory_limit='1GiB', processes=True, scheduler_port=8786, dashboard_address='localhost:8787')):

#         bag = db.read_text(file_path).map(json.loads)
#         tweet_data = bag.map(process_tweet)


        
#         top_users_date = tweet_data.reduction(aggregate_counts, aggregate_counts).compute()
#         print(top_users_date)
#         top_dates = nlargest(10, top_users_date, key=lambda x: top_users_date[x]['total_count'])
        
#         result = []
#         for date in top_dates:
#             top_user = max(top_users_date[date]['user_counts'].items(), key=lambda x: x[1])[0]

#             result.append((date, top_user))

#         return result










