'''
An app to enable data entry and data retrieval into a SQLite database.
'''

__author__ = 'Liam Heisler'
__date__ = 'Jan 2023'
__version__ = 'DEV'


# imports
from pathlib import Path
import PySimpleGUI as sg
import pandas as pd

# local imports
from utils.definitions import *
from utils.default_ops import *

# database management
from utils.database import Database

db = Database()

# Add some color to the window
sg.theme('DarkTeal9')

current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
EXCEL_FILE = current_dir / 'Data_Entry.xlsx'

# Load the data if the file exists, if not, create a new DataFrame
if EXCEL_FILE.exists():
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame()

# window config helping
rowitem_descriptor_box_size = (25, 1)
rowitem_entry_box_size = (30, 1)

# can i get the engineer's ID from host?
nameplate_frame = [
    [sg.Text('Engineer (Last, First)', size=rowitem_descriptor_box_size), sg.InputText(key='Engineer')],
    [sg.Text('Program', size=rowitem_descriptor_box_size), 
     sg.Combo(available_programs, readonly=True, key='Program', size=rowitem_entry_box_size)],
    [sg.Text('Workstream', size=rowitem_descriptor_box_size), 
     sg.Combo(available_workstreams, readonly=True, key='Workstream', size=rowitem_entry_box_size)],
    [sg.Text('Project Name', size=rowitem_descriptor_box_size), sg.InputText(key='Project_Name')],
    [sg.Text('PD Number', size=rowitem_descriptor_box_size), sg.InputText(key='PD_Number')]
]

project_spec_frame = [
    [sg.Text('Target Completion Date', size=rowitem_descriptor_box_size), sg.Text('--- fill with calendar selector ---', size=rowitem_descriptor_box_size)],
    [sg.Text('Circuit(s) (separate by comma)', size=rowitem_descriptor_box_size), sg.InputText(key='Project_Circuit')],
    [sg.Text('Mileage', size=rowitem_descriptor_box_size), sg.InputText(key='Mileage')],
    [sg.Text('Primary Solution', size=rowitem_descriptor_box_size),
     sg.Combo(available_primary_solns, readonly=True, key='Primary_Solution', size=rowitem_entry_box_size)],
    [sg.Text('Secondary Solution', size=rowitem_descriptor_box_size),
     sg.Combo(available_secondary_solns, readonly=True, key='Secondary_Solution', size=rowitem_entry_box_size)],
    [sg.Text('Solid or Fused | Pre-Period', size=rowitem_descriptor_box_size),
     sg.Combo(available_solid_fused, readonly=True, key='Pre_SolidFused', size=rowitem_entry_box_size)],
    [sg.Text('Solid or Fused | Post-Period', size=rowitem_descriptor_box_size),
     sg.Combo(available_solid_fused, readonly=True, key='Post_SolidFused', size=rowitem_entry_box_size)],
    [sg.Text('Distribution Segment | Pre-Period', size=rowitem_descriptor_box_size),
     sg.Combo(available_segments, readonly=True, key='Pre_Dist_Segment', size=rowitem_entry_box_size)],
    [sg.Text('Distribution Segment | Post-Period', size=rowitem_descriptor_box_size),
     sg.Combo(available_segments, readonly=True, key='Post_Dist_Segment', size=rowitem_entry_box_size)],
]

# use a multi line for transformers? or just 1 line withi commas?
customer_spec_frame = [
    [sg.Text('by Circuit', size=rowitem_descriptor_box_size), sg.InputText(key='CustSpec_Circuit')],
    [sg.Text('by Recloser Section', size=rowitem_descriptor_box_size), sg.InputText(key='CustSpec_RecloserSect')],
    [sg.Text('by URD Section', size=rowitem_descriptor_box_size), sg.InputText(key='CustSpec_URDSect')],
    [sg.Text('by Transformers', size=rowitem_descriptor_box_size), sg.InputText(key='CustSpec_Trfs')]
]

financial_and_rel_spec_tab = [
    [sg.Text('Estimated ACI', size=rowitem_descriptor_box_size), sg.InputText(key='Estimated_ACI')],
    [sg.Text('Estimated Cost', size=rowitem_descriptor_box_size), sg.InputText(key='Estimated_Cost')]
]

submit_project_tab_layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Frame('Project Nameplate', nameplate_frame)],
    [sg.Frame('Project Specification', project_spec_frame)],
    [sg.Frame('Reliability & Financial Specification', financial_and_rel_spec_tab)],   
    [sg.Frame('Customer Specification', customer_spec_frame)],
    [sg.Submit(), sg.Button('Clear')]
]

# ---- Edit Projects ----

edit_projects_tab_layout = [
    [sg.Button('Fetch Projects', key='fetch_projects'), sg.Button('Edit Selected Project', key='edit_selected_project')],
    [sg.Listbox(values=[], size=(75, 10), key='listbox_select_projects')]
]

# ---- Query Projects ----

query_projects_tab_layout = [
    [sg.Multiline('blah', size=(15, 15))]
]

layout = [
    # format is sg.TabGroup([[tab1, tab2]]). kinda ugly
    [sg.TabGroup([[
        sg.Tab('Submit Projects', submit_project_tab_layout, key="tab_submitProjs"),
         sg.Tab('Edit Projects', edit_projects_tab_layout, key="tab_editProjs"),
            sg.Tab('Query Projects', query_projects_tab_layout, key="tab_queryProjs")
    ]], key="tab_group")],
    [sg.Exit()]
]

window = sg.Window('Project Effectiveness Database', layout)

def clear_input():
    for key in values:
        window[key]('')
    return None


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        # archaic method -- more for testing or lazily setting up the table... i know :(
        #df = pd.DataFrame(values, index=[0])
        #df.to_sql('projects', con=db.connection, if_exists='replace')
        
        # insert new row
        insert_row_check = db.insert_row(values)

        # if we actually submitted the row, throw a pop up
        if insert_row_check: sg.popup('Project submitted.')

        # once submitted, get rid of the data in the boxes
        clear_input()
    
    if event == 'fetch_projects':
        display_list = db.get_project_data_for_lbox()
        window['listbox_select_projects'].update(display_list)

window.close()
db.disconnect()