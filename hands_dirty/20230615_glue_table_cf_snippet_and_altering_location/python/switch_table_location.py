import boto3
import json 


def get_glue_table_location(glue_client, database_name, table_name):
    try:
        response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
        table_input = response['Table']
 
        return table_input['StorageDescriptor']['Location']
    except Exception as e:
        print(f"Error getting location of the table '{table_name}': {str(e)}")        

def update_glue_table_location(glue_client, database_name, table_name, new_location):        
    try:
        response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
        table_input = response['Table']
        
        table_input['StorageDescriptor']['Location'] = new_location
        del table_input['CreateTime']
        del table_input['UpdateTime']
        del table_input['DatabaseName']
        del table_input['CreatedBy']
        del table_input['IsRegisteredWithLakeFormation']    
        del table_input['CatalogId']
        del table_input['VersionId']
        
        glue_client.update_table(DatabaseName=database_name, TableInput=table_input)
        print(f"Successfully updated the location of the table '{table_name}'.")
    
    except glue_client.exceptions.EntityNotFoundException:
        print(f"The table '{table_name}' does not exist in the database '{database_name}'.")
    
    except Exception as e:
        print(f"An error occurred while updating the location of the table '{table_name}': {str(e)}")



glue_client = boto3.client('glue')

# Usage
database_name = 'db-athenatbl'
table_name = 'sample_table'

valid_locations_folders = ['dataset_a/','dataset_b/']

current_location = get_glue_table_location(glue_client, database_name, table_name)

# switching between dataset_a and dataset_b
if current_location.endswith(valid_locations_folders[0]):
    new_folder = valid_locations_folders[1]
    current_folder = valid_locations_folders[0]   
else:
    new_folder = valid_locations_folders[0]
    current_folder = valid_locations_folders[1]    

new_location = current_location.replace(current_folder, new_folder)
print(f"New location: {new_location} ({current_folder} -> {new_folder})")

update_glue_table_location(glue_client, database_name, table_name, new_location)
