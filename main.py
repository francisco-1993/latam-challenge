import os
import argparse
import subprocess
from typing import Callable
from src import q1_memory, q1_time, q2_memory, q2_time, q3_memory, q3_time

def clean_folder(folder_path:str) -> None:
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def run_memray_command(memory_tracker_path:str) -> None:
    bins_subfolder = os.path.join(memory_tracker_path, 'bins')
    htmls_subfolder = os.path.join(memory_tracker_path, 'htmls')

    # for file in os.listdir(bins_subfolder):
    #     file_path = os.path.join(bins_subfolder, file)
    #     if os.path.isfile(file_path):
    #         command = f'memray3.10 flamegraph -f -o {htmls_subfolder} {file_path}'
    #         subprocess.run(command, shell=True, cwd=bins_subfolder)
    
    for file in os.listdir(bins_subfolder):
        file_path = os.path.join(bins_subfolder, file)
        if os.path.isfile(file_path):
            command = f'memray3.10 flamegraph -f -o {htmls_subfolder} {file_path}'
            try:
                subprocess.run(command, shell=True, cwd=bins_subfolder, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")

def run_function(func_name:Callable, data_path:str) -> None:
    command = [
        'python3',
        '--datapath',
        data_path,
        '--functions',
        f'{func_name}.{func_name}'
    ]
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description='Data Callenge LATAM')
    parser.add_argument('--datapath', required=True, help='Path donde se encuentra data')
    parser.add_argument('--functions', nargs='+', required=True, help='Nombre de funciones a ejecutar')

    args = parser.parse_args()

    data_path = args.datapath
    functions_to_test = args.functions

    #creacion directorios para archivos adicionales generados por memray
    memory_tracker_path = 'memory_tracker_files/'
    bins_subfolder = os.path.join(memory_tracker_path, 'bins')
    htmls_subfolder = os.path.join(memory_tracker_path, 'htmls')
    os.makedirs(bins_subfolder, exist_ok=True)
    os.makedirs(htmls_subfolder, exist_ok=True)

    #limpieza de archivos en subcarpetas de memory_tracker_path, si los hay
    clean_folder(bins_subfolder)
    clean_folder(htmls_subfolder)

    for func_name in functions_to_test:
         run_function(func_name, data_path)
    
    #generacion de htmls para memory usage de memray para todos las funciones testeadas
    run_memray_command(memory_tracker_path)

if __name__ == '__main__':
    main()

#python3 --datapath 'data/farmers-protest-tweets-2021-2-4.json' --functions 'q1_memory'
