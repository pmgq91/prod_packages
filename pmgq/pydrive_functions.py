# Importar librerías
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


########################################################################################################
# Autenticación a través de archivo settings (silent auth)
def f_auth_settings_file(
    v_folder_settings,
    v_pydrive_settings_file='pydrive_settings.yaml'
):

    o_gauth=GoogleAuth(settings_file=v_folder_settings+v_pydrive_settings_file)
    o_gauth.LocalWebserverAuth()
    
    # Creación de objeto para interactuar con Google Drive
    global o_gdrive
    o_gdrive=GoogleDrive(o_gauth)
    
    
########################################################################################################    
# Contenido en un folder
def f_l_content(v_folder_id='root'):
    l_content_raw=o_gdrive.ListFile({'q':"'"+v_folder_id+"' in parents and trashed=false"}).GetList()    
    l_content=[]    
    for content in l_content_raw:
        l_content.append({'id':content['id'],'title':content['title'],'mimeType':content['mimeType']})        
    return l_content


########################################################################################################
# Descargar archivo
def f_download_file(v_file_id,v_output_file_name):
    o_gdrive.CreateFile({'id':v_file_id}).GetContentFile(v_output_file_name)
    
    
########################################################################################################    
# Cargar archivo
def f_upload_file(v_destination_file_name,v_local_file_name,v_destination_folder_id='root'):    
    o_file=o_gdrive.CreateFile({'title':v_destination_file_name,'parents':[{'id':v_destination_folder_id}]})
    o_file.SetContentFile(v_local_file_name)
    o_file.Upload()
    
    
########################################################################################################    
# Eliminar archivo
def f_trash_file(v_file_title,v2_folder_id='root'):

    # Inicializando variable para guardaer id del archivo
    v_file_id=''
    
    # Identifico id de archivo a eliminar
    for content in f_l_content(v_folder_id=v2_folder_id):
        if content['title']==v_file_title:
            v_file_id=content['id']
            
    # Levantar error si el valor del id del archivo sigue siendo ''
    if v_file_id=='':
        raise NameError('Archivo no encontrado!!')

    # Elimino archivo
    o_gdrive.CreateFile({'id':v_file_id}).Trash()
    
    
########################################################################################################
# Renombrar archivo
def f_rename_file(v_file_id,v_new_title):
    o_file_to_rename=o_gdrive.auth.service.files().get(fileId=v_file_id).execute()
    o_file_to_rename['title']=v_new_title
    o_gdrive.auth.service.files().update(fileId=v_file_id,body=o_file_to_rename).execute()

########################################################################################################
# Copiar archivo
def f_copy_file(v_origin_file_id,v_copied_file_name):
    o_gdrive.auth.service.files().copy(fileId=v_origin_file_id,body={'title':v_copied_file_name}).execute()    