import gspread
import os

def f_o_tab_error(p_path_service_account):
    o_gs_service_account = gspread.service_account(filename = p_path_service_account)
    o_spreadsheet_errors = o_gs_service_account.open_by_key('12FmsjHWh0fLyuXTqHc_wHqT8uP4tNNVe5z6-hGBbUTY')
    o_tab_error = o_spreadsheet_errors.get_worksheet_by_id(1054369469)
    return o_tab_error

def f_write_error(p_o_tab_error, p_script_and_error_message):
    l_error_values = p_o_tab_error.col_values(1)
    v_row_error_entry = len(l_error_values) + 1    
    p_o_tab_error.update('A' + str(v_row_error_entry), p_script_and_error_message)

#USAGE:
'''
from pmgq import crontab_error_to_pendientes as lib_error

v_path_service_account = '{{path}}'

o_tab_error = lib_error.f_o_tab_error(p_path_service_account = v_path_service_account)

lib_error.f_write_error(
    p_o_tab_error = o_tab_error,
    p_script_and_error_message = 'test: hola'
)
'''