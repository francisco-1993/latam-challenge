import json
from collections import deque


'''
Acotaciones:

-buffered_reader: este es un buffer tradicional para intentar generar una lectura por chunks de data en vez de linea por linea, teniendo como objetivo 
la reduccion en tiempo de ejecucion con un aumento razonable de memoria

-buffered_reader_in_memory: intente definir un retorno de inmediato y en memoria de todo el buffer, en vez de a travez de un generator con yield
pensando en lograr un tiempo de ejecucion aun mejor que el anterior a costa de mas memoria en teoria, no obstante, para la data utilizada los cambios fueron
insignificantes, no obstante a mayor tamaño del archivo a analizar podria ser interesante de analizar, aunque tambien se debe tener en cuenta que para 
archivos que ya sean demasiado grandes, claramente este enfoque fallaria ya que el buffer siempre se sigue leyendo de forma secuencial, aunque se encuentre
todo en memeoria

'''

def buffered_reader(file_path:str, buffer_size:int):
    buff = deque()
    with open(file_path, 'r') as file:
        while True:
            lines = file.readlines(buffer_size)
            if not lines:
                break
            for line in lines:
                yield json.loads(line)
    return buff

def buffered_reader_in_memory(file_path:str, buffer_size:int):
    buff = deque()
    with open(file_path, 'r') as file:
        while True:
            lines = file.readlines(buffer_size)
            if not lines:
                break
            for line in lines:
                buff.append(json.loads(line))
                #yield json.loads(line)
    return buff