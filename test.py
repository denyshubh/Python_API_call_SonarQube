#!/usr/bin/env python3

'''
This module creates a Quality Gate, adds conditions to and Set the Quality Gate as Default.
It needs admin user privilages
You can either use Token or use your username and password
To use Token add token in the user prompt and leave password field empty
'''

import os
import requests
from requests.exceptions import HTTPError
from getpass import getpass

TOKEN = os.environ['SONAR_AUTH_TOKEN']
# should be replaced by sonarqube Jenking configuration's fields/variables
SONARQUBE_URL = os.environ['SONAR_HOST_URL']
#input("SonarQube URL like http://localhost:9000: ")
SONARQUBE_QUALITYGATE_API = SONARQUBE_URL+"/api/qualitygates"
SONARQUBE_QUALITYPROFILE_API = SONARQUBE_URL+"/api/qualityprofiles"
# should be replaced by sonarqube Jenking configuration's fields/variables
#USER = input('User: ')
#PASS = getpass()
# The new name of QG of on-boarding team. Should 'Lean SDLC_<TeamName>'
QUALITY_GATE_NAME = "Lean SDLC_HITT_EXTENDED_New2"
#input("Quality Gate Name: ")
# Default Name of Sonar plus Mutation Quality Profile created by HITT as the DEFAULT
QUALITY_PROFILE_NAME_FROM = "Sonar+Mutation" 
# The new name of profile on-boarding team wants. Should HITT the DEFAULT + _<TeamName>
QUALITY_PROFILE_NAME_TO = "Sonar+Mutation_HITT_EXTENDED_New2"

CONDITIONS = {
    0: ["coverage", "LT", "100"],
    1: ["dc5_mutationAnalysis_mutations_coverage", "LT", "100"],
    2: ["sqale_rating", "GT", "1"],
    3: ["reliability_rating", "GT", "1"],
    4: ["code_smells", "GT", "1"],
    5: ["security_rating", "GT", "1"],
    6: ["blocker_violations", "GT", "0"],
    7: ["critical_violations", "GT", "0"],
    8: ["major_violations", "GT", "0"],
    9: ["minor_violations", "GT", "0"],
}

def create_quality_gate(quality_gate_name):
    '''
    This function creates a Quality Gate
    '''
    print('In Create')
    try:
        res = requests.post(
            '{}/create'.format(SONARQUBE_QUALITYGATE_API),
            params={'name':quality_gate_name},
            auth=(TOKEN, '')
            )
        res.raise_for_status()
        print(
            'Quality Gate Creation Successfull\n status: {}\n response:{}'
            .format(res.status_code, res.text)
            )
        return res.json()['id']
    except HTTPError as http_error:
        print(
            'Quality Gate creation failed. It can be due to duplicate quality \
gate name or invalid credentials. It throws the following HTTP Error : {}'
            .format(http_error)
            )
    except Exception as err:
        print("Error in the Code", err)

    return None

def add_conditions(gate_id, metric, operator, error):
    '''
    This function adds condition to our quality gate
    '''
    print('In Add Condition')
    res = requests.post(
        '{}/create_condition'.format(SONARQUBE_QUALITYGATE_API),
        params=[('gateId', gate_id), ('metric', metric), ('op', operator), ('error', error)],
        auth=(TOKEN, '')
        )
    print(res.text)
    return res.status_code

def set_qg_default(gate_id):
    '''
    This function makes our quality gate as default
    '''
    res = requests.post(
        '{}/set_as_default'.format(SONARQUBE_QUALITYGATE_API),
        params={'id':gate_id},
        auth=(TOKEN, '')
        )
    print(res.text)  
    return res.status_code
    
def search_qprofile(qp_name):
    '''
    This function searches for the ID of QP for a given QP Name
    '''
    try:
        res = requests.get(
            '{}/search'.format(SONARQUBE_QUALITYPROFILE_API),
            params={'qualityProfile':qp_name},
            auth=(TOKEN, '')
            )
        res.raise_for_status()
        print(
            '\nQuality Profile {} found\n status: {}\n response:{}'
            .format(qp_name, res.status_code, res.text)
            )
        return res.json()['profiles'][0]['key']
    except HTTPError as http_error:
        print(
            'Quality Profile not found : {}'
            .format(http_error)
            )
    except Exception as err:
        print("Error in the Code", err)

    return None
    
def copy_qprofile(qp_id, newProfileName):
    '''
    This function will copy the SonarAndMutation profile for an on boarding team into a provide QP name
    '''
    print(
        '\nCopying {} to {}\n'
        .format(qp_id, newProfileName)
        )
    res = requests.post(
        '{}/copy'.format(SONARQUBE_QUALITYPROFILE_API),
        params=[('fromKey', qp_id), ('toName', newProfileName)],
        auth=(TOKEN, '')
        )
    print(res.text)  
    return res.status_code
    
'''
def delete_qprofile(profileName):
    
    print(
        'Deleting {}\n'
        .format(profileName)
        )
    res = requests.post(
        '{}/delete'.format(SONARQUBE_QUALITYPROFILE_API),
        params={'profileKey': profileName},
        auth=(TOKEN, '')
        )
    print(res.text)  
    return res.status_code
'''
def _main_() :
    print(
        'In Main\n{}\n{}'
        .format(SONARQUBE_URL, TOKEN)
         )
    try:
        gate_id = create_quality_gate(QUALITY_GATE_NAME)
        
        if gate_id:
            for _, val in CONDITIONS.items():
                result = add_conditions(gate_id, val[0], val[1], val[2])
                if result & 200 != 200:
                    raise ValueError('Quality Gate Condition creation failed {}'.format(val))
            print(
                'Conditions added successfully to Quality Gate'
                )
            '''result = set_qg_default(gate_id)'''
            qp_id = search_qprofile(QUALITY_PROFILE_NAME_FROM)
            result = copy_qprofile(qp_id, QUALITY_PROFILE_NAME_TO)
            if result & 200 != 200:
                raise ValueError('Error while making the quality gate as default')
            print(
                'Quality Profile with Name {} is copied from default one - {}'
                .format(QUALITY_PROFILE_NAME_TO, qp_id)
                )
            #delResult = delete_qprofile('AXRx4ln2plT98XS9cSoM')
    except ValueError as error:
        print(error)
        
_main_()
