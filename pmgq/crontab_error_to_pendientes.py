import gspread
import os

def f_o_tab_error(p_path_service_account):
    o_gs_service_account = gspread.service_account(filename = p_path_service_account)
    o_spreadsheet = o_gs_service_account.open_by_key('1JVvnOiuLusdCHMZcvHRVzbKUMrTp4QpuzGbgPV9jvck')
    o_spreadsheet_errors = o_gs_service_account.open_by_key('12FmsjHWh0fLyuXTqHc_wHqT8uP4tNNVe5z6-hGBbUTY')
    o_tab_error = o_spreadsheet_errors.get_worksheet_by_id(1054369469)
    l_error_values = o_tab_error.col_values(1)
    v_row_error_entry = len(l_error_values) + 1
    return o_tab_error, v_row_error_entry

def f_write_error(p_o_tab_error, p_row_error_entry, p_error_message):
    try:
        v_script_name = os.path.basename(__file__)
    except:
        v_script_name = '??jupyter_nb??'
    p_o_tab_error.update('A' + str(p_row_error_entry), v_script_name + ': ' + p_error_message)

#USAGE:
'''
v_path_service_account = '{{path}}'

o_tab_error, v_row_error_entry = lib_error.f_o_tab_error(p_path_service_account = v_path_service_account)

lib_error.f_write_error(
    p_o_tab_error = o_tab_error,
    p_row_error_entry = v_row_error_entry,
    p_error_message = 'hola'
)
'''