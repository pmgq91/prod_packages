# Importar librerías
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


########################################################################################################
# Autenticación a través de archivo settings (silent auth)
def f_auth_settings_file(
    p_folder_settings,
    p_pydrive_settings_file = 'pydrive_settings.yaml'
):

    o_gauth = GoogleAuth(settings_file = 'f{p_folder_settings}{p_pydrive_settings_file}')
    o_gauth.LocalWebserverAuth()
    
    # Creación de objeto para interactuar con Google Drive
    global o_gdrive
    o_gdrive = GoogleDrive(o_gauth)
    
    
########################################################################################################    
# Contenido en un folder
def f_l_content(p_folder_id = 'root'):
    l_content_raw = o_gdrive.ListFile({'q': "'"+v_folder_id+"' in parents and trashed=false"}).GetList()    
    l_content = []    
    for i_content in l_content_raw:
        l_content.append({'id': i_content['id'], 'title': i_content['title'], 'mimeType': i_content['mimeType']})
    return l_content


########################################################################################################
# Descargar archivo
def f_download_file(p_file_id, p_output_file_name):
    o_gdrive.CreateFile({'id': p_file_id}).GetContentFile(p_output_file_name)
    
    
########################################################################################################    
# Cargar archivo
def f_upload_file(p_destination_file_name, p_local_file_name, p_destination_folder_id = 'root'):
    o_file = o_gdrive.CreateFile({'title': p_destination_file_name, 'parents': [{'id': p_destination_folder_id}]})
    o_file.SetContentFile(p_local_file_name)
    o_file.Upload()
    
    
########################################################################################################    
# Eliminar archivo
def f_trash_file(p_file_title, p2_folder_id = 'root'):

    # Inicializando variable para guardaer id del archivo
    v_file_id = ''
    
    # Identifico id de archivo a eliminar
    for i_content in f_l_content(p_folder_id = p2_folder_id):
        if i_content['title'] == v_file_title:
            v_file_id = content['id']
            
    # Levantar error si el valor del id del archivo sigue siendo ''
    if v_file_id == '':
        raise NameError('File not found!!')

    # Elimino archivo
    o_gdrive.CreateFile({'id': v_file_id}).Trash()
    
    
########################################################################################################
# Renombrar archivo
def f_rename_file(p_file_id, p_new_title):
    o_file_to_rename = o_gdrive.auth.service.files().get(fileId = p_file_id).execute()
    o_file_to_rename['title']= p_new_title
    o_gdrive.auth.service.files().update(fileId = p_file_id, body = o_file_to_rename).execute()

########################################################################################################
# Copiar archivo
def f_copy_file(p_origin_file_id, p_copied_file_name):
    o_gdrive.auth.service.files().copy(fileId = p_origin_file_id, body = {'title': p_copied_file_name}).execute()    