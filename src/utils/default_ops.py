'''
Place to store the default options for the app's selectors.
'''

available_workstreams = [
    'CEMI Areas',
    'CEMI Targeted Circuits',
    'AIR Areas',
    'URD Replacement',
    'Mainstem'
]

available_programs = [
    'LTIIP I',
    'LTIIP II',
    'Non-LTIIP'
]

available_segments = [
    'Aerial',
    'Distribution',
    'Both'
]

available_solid_fused = [
    'Solid',
    'Fused',
    'Both'
]

# TODO check
available_primary_solns = [
    'Replacement',
    'Armless-Bare',
    'Spacer',
    'Enhancement',
    'Recloser'
]

# TODO check
available_secondary_solns = [
    'Replacement',
    'Armless-Bare',
    'Spacer',
    'Enhancement',
    'Recloser'
]

gui_keys_to_write_to_db = [
    'Project_ID',
    'Engineer',
    'Program',
    'Workstream',
    'Project_Name',
    'PD_Number',
    'Project_Circuit',
    'Mileage',
    'Primary_Solution',
    'Secondary_Solution',
    'Pre_SolidFused',
    'Post_SolidFused',
    'Pre_Dist_Segment',
    'Post_Dist_Segment',
    'Estimated_ACI',
    'Estimated_Cost',
    'CustSpec_Circuit',
    'CustSpec_RecloserSect',
    'CustSpec_URDSect',
    'CustSpec_Trfs'
]