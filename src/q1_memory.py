from typing import List, Tuple
from datetime import datetime
from collections import defaultdict
from utils import custom_profilers
from heapq import nlargest
import jsonlines
import json

'''
    Acotaciones:
        - defaultdict permite definicion automatica de llaves cuando estas no este definidas
        - jsonlines esta optimizada para leer archivos jsonl sin cargarlo todo en memoria, entiendo lee 1 fila a la vez, por lo que lo veo como un buffer donde el tamaño del chunk es cada linea,
        con esto, a costa de tiempo de ejecucion puedo ahorrar bastante memoria
        - Se parsean solo los campos requeridos para la solucion ya que no es necesario cargan mas en memoria 
        - strptime por sobre dateutil ya que es mas sencilla y requiere menos memoria, no obstante es mas rigida y se debe conocer el formato de antemano, dado que se estan testeando muestras,
        se asumen tienen formato conocido, finalmente hacer un slicing antes para reducir la complejidad del formato de fecha a inputar ayuda en tiempo mas que en memoria, pero se considero como 
        optimizacion para todas las preguntas en general, donde aplicara
        -Se uso un heap para el top 10 dates, ya que es mas eficiente que sorted en el uso de memoria ya que no crea estructura adicional para odernar sino que lo hace in-place

'''


@custom_profilers.memory_profiler
#@custom_profilers.exec_time_profiler
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:

    #{date: {username: tweets_count}} -> registros de todos los username con respectivas menciones (tweet_count) para cada date
    date_counts =  defaultdict(lambda: defaultdict(int)) 
    top_dates = []

    with jsonlines.open(file_path) as file:     

        for tweet in file:
            date = datetime.strptime(tweet['date'][:10],'%Y-%m-%d').date() 
            user = tweet['user']['username']
            date_counts[date][user] += 1

    #(date, {username: tweets_count}) -->  se obtiene top date basando en suma global de tweet_count para dicho date 
    top_dates = nlargest(10, date_counts.items(), key=lambda x: sum(x[1].values())) 
    

    #[(date, username)] --> para el top_dates, se toma para cada date el username con mas tweet_count
    result = [(date, max(users.items(), key=lambda x: x[1])[0]) for date, users in top_dates]
    
    return result
