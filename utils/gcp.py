import os
import json
from collections import deque
from typing import Callable, List, Optional
from google.cloud import bigquery
from google.oauth2 import service_account


#Se que este no es mejor metodo por razones de seguridad, ya que se tiene una llave expuesta en local, no obstante por simplicidad y por este ser un challenge puntual
def authenticate(key_path:str) -> tuple:
    credentials = service_account.Credentials.from_service_account_file(key_path)
    project_id = credentials.project_id
    return (credentials, project_id)


def create_dataset(client:bigquery.Client, dataset_id:str, location:str='US'):
    
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = location
    client.create_dataset(dataset, exists_ok=True)

    return dataset_ref
    
def create_table(client:bigquery.Client, dataset_ref:Callable, table_id:str, schema:List[bigquery.SchemaField]):

    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    client.create_table(table, exists_ok=True)
    
    return table_ref


def buffer_jsonl_data(client, table_ref, file_path, num_rows_batch=10000) -> None:
    with open(file_path, 'r') as file:
        batch_data = []
        for line in file:
            json_data = json.loads(line)
            row_data = {
                'date': json_data['date'][:10] # se sube solo slice date como str, para castearlo ya en bigquery
                ,'username': json_data['user']['username']
                ,'content': json_data['content']  
                #,'mentioned_usernames': [user['username'] for user in json_data.get('mentionedUsers', []) if isinstance(user, dict) and 'username' in user]
                ,'mentioned_usernames': [
                    user_dict.get('username')
                    for mentioned_users in (json_data.get('mentionedUsers') or [])
                    if isinstance(mentioned_users, list)
                    for user_dict in mentioned_users
                    if isinstance(user_dict, dict)
                ]
            }
            batch_data.append(row_data)


            if len(batch_data) == num_rows_batch:
                #el metodo insert_rows_json genera un mapeo de los errores en dicho caso, se aprovecha eso para generar el if-else
                errors = client.insert_rows_json(table_ref, batch_data)
                if not errors:
                    print(f'Inserted {len(batch_data)} rows.')
                else:
                    print(f'Encountered errors while inserting rows: {errors}')
                batch_data = []
        
        #en caso de que el tamaño del batch no sea divisible por num_rows_batch
        if batch_data:
            errors = client.insert_rows_json(table_ref, batch_data)
            if not errors:
                print(f'Inserted {len(batch_data)} rows.')
            else:
                print(f'Encountered errors while inserting rows: {errors}')


def execute_query(client: bigquery.Client, query_file: str, performance_file: str, project_id:str, dataset_id:str, table_id:str)-> None:  

    with open(query_file, 'r') as file:
        query_string = file.read()

    query_string = query_string.replace('${DATASET_ID}', dataset_id)
    query_string = query_string.replace('${PROJECT_ID}', project_id)
    query_string = query_string.replace('${TABLE_ID}', table_id)

    query_job = client.query(query_string)
    results = query_job.result()

    total_bytes_processed_mb = query_job.total_bytes_processed / (1024 * 1024)
    total_bytes_billed_mb = query_job.total_bytes_billed / (1024 * 1024)

    performance_data = {
        'query': query_string
        ,'total_bytes_processed': f'{total_bytes_processed_mb:.2f} MB'
        ,'total_bytes_billed': f'{total_bytes_billed_mb:.2f} MB'
        ,'billing_tier': query_job.billing_tier
        ,'cache_hit': query_job.cache_hit
        ,'query_time': str(query_job.ended - query_job.started)
    }

    with open(performance_file, 'w') as file:
        json.dump(performance_data, file, indent=4)
    
    #return results

