from utils.gcp import *
from pprint import pprint

def main():
    
    key_path = 'keys/data-challenge-latam-8a0d0091a1ff.json'
    location = 'US'
    dataset_id = 'dataset_challenge_de_latam'
    table_id = 'table_challenge_de_latam'
    data_path = 'data/farmers-protest-tweets-2021-2-4.json'
    credentials, project_id = authenticate(key_path)

    with bigquery.Client(project=project_id, credentials=credentials, location=location) as client:

        dataset_ref = create_dataset(client, dataset_id, location)
        schema = [
            bigquery.SchemaField('date', 'STRING'),
            bigquery.SchemaField('username','STRING'),
            bigquery.SchemaField('content', 'STRING'),
            bigquery.SchemaField('mentioned_usernames', 'STRING', mode='REPEATED')
            ]
        table_ref = create_table(client, dataset_ref, table_id, schema)

        buffer_jsonl_data(client, table_ref, data_path)

        sql_folder = 'sql/'
        for i in range(1, 4):
            query_file = os.path.join(sql_folder, f'q{i}.sql')
            performance_file = os.path.join(sql_folder, f'q{i}_performance.json')
            results = execute_query(client, query_file, performance_file, project_id, dataset_id, table_id)

if __name__ == '__main__':
    main()
