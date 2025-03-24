# Import modules
import os
from pmgq import pydrive_functions as pyd
import time



# Folder with keys
if os.getcwd() == '/home/ubuntu':
    v_keys_folder = '/home/ubuntu/personal/keys/'
else:
    v_keys_folder = os.getcwd()[0:os.getcwd().find('personal')] + 'personal/keys/'
    


# Establishing connection to gDrive
pyd.f_auth_settings_file(p_folder_settings = f'{v_keys_folder}pydrive/')



# Functions


def f_get_v_prod_db_file_id(p01_folder_id, p01_prod_DB_file_name):
    # Generate list of files within gDrive folder
    l_files = pyd.f_l_content(p_folder_id = p01_folder_id)
    # Identify the file_id of the prod DB
    v_prod_db_file_id = None
    for i_file in l_files:
        if i_file['title'] == p01_prod_DB_file_name:
            v_prod_db_file_id = i_file['id']
    return v_prod_db_file_id


def f_download_DB(p001_prod_DB_file_name, p001_folder_id, p001_backup_DB_file_name, p_recreate_backup = True):
    
    # Remove if exists a local copy of the prod DB 
    try:
        os.remove(p001_prod_DB_file_name)
        # Log message
        print('There was a local prod DB that has been removed.')
    except:
        pass

    # Get `v_prod_db_file_id`
    v_prod_db_file_id = f_get_v_prod_db_file_id(
        p01_folder_id = p001_folder_id,
        p01_prod_DB_file_name = p001_prod_DB_file_name
    )
    if v_prod_db_file_id == None:
        # Identify the `file_id` of the backup DB
        for i_file in pyd.f_l_content(p_folder_id = p001_folder_id):
            if i_file['title'] == p001_backup_DB_file_name:
                v_backup_db_file_id = i_file['id']
        # Copy the backup DB as prod DB
        pyd.f_copy_file(p_origin_file_id = v_backup_db_file_id, p_copied_file_name = p001_prod_DB_file_name)
        # Wait 5 seconds for file to be created
        time.sleep(5)    
        # Log message
        print('The prod DB was not on gDrive, so it was recreated based on the gDrive backup DB.')
        v_prod_db_file_id = f_get_v_prod_db_file_id(
            p01_folder_id = p001_folder_id,
            p01_prod_DB_file_name = p001_prod_DB_file_name
        )

    # Download prod DB into local cwd
    pyd.f_download_file(p_file_id = v_prod_db_file_id, p_output_file_name = p001_prod_DB_file_name)
    # Log messages
    print('Successfully downloaded gDrive prod DB to local.')

    if p_recreate_backup:
        # Delete previous backup DB in gDrive
        pyd.f_trash_file(p_file_title = p001_backup_DB_file_name, p2_folder_id = p001_folder_id)
        # Rename old prod gDrive DB as backup DB
        pyd.f_rename_file(p_file_id = v_prod_db_file_id, p_new_title = p001_backup_DB_file_name)
        # Log messages
        print('Successfully recreated backup DB in gDrive based in current gDrive prod DB.')


def f_upload_DB(p001_prod_DB_file_name, p001_folder_id):
    
    # Upload local prod DB to gDrive
    pyd.f_upload_file(
        p_destination_file_name = p001_prod_DB_file_name,
        p_local_file_name = p001_prod_DB_file_name,
        p_destination_folder_id = p001_folder_id
    )

    # Remove local prod DB
    os.remove(p001_prod_DB_file_name)

    # Log messages
    print('Successfully uploaded local prod DB to gDrive and removed it from local.')