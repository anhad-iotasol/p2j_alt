import os
import json
import requests
import webbrowser
from pathlib import Path
from dotenv import load_dotenv,find_dotenv
from services.llm_parser import form_template_single
#from services.Frappe.schema_parser import get_schema

_ = load_dotenv(find_dotenv())

BASE_URL = os.environ['FRAPPE_BASE_URL']
auth_header = f"token {os.environ['FRAPPE_KEY']}:{os.environ['FRAPPE_SECRET']}"

request_body = json.loads(Path('./json_output.json').read_text())

def publish_form(request_body):
    response = requests.post(f"{BASE_URL}/api/resource/DocType/",json=request_body,headers={
        "Authorization" : auth_header
    })
    return response

def delete_form(name):
    requests.delete(f"{BASE_URL}/api/resource/DocType/{name}", headers={
        "Authorization" : auth_header
    })
    return

def publish_and_preview(request_body):
    response = publish_form(request_body)
    #print(response.json())
    webbrowser.open(f"{BASE_URL}/app/doctype/{request_body['name']}")
    return response

def update_and_preview(request_body):
    response = requests.put(f"{BASE_URL}/api/resource/DocType/{request_body['name']}", json=request_body,headers={
        "Authorization" : auth_header
    })
    #webbrowser.open(f"{BASE_URL}/app/doctype/{request_body['name']}")
    return response

def submit_form(request_body):
    #request_body = json.loads(Path('./json_output.json').read_text())
    checkResponse = requests.get(f"{BASE_URL}/api/resource/DocType/{request_body['name']}",headers={
        "Authorization" : auth_header
    })
    docExists = checkResponse.ok

    if not docExists: publish_and_preview(request_body)
    else: update_and_preview(request_body)
    return

def frappe_login():
    response = requests.get(f"{BASE_URL}/api/method/login",json={
        "usr" : os.environ['FRAPPE_USERID'],
        "pwd" : os.environ['FRAPPE_PWD']
    })
    sid = response.cookies['sid']
    return sid

def testfrappe():
    response = requests.get(f"{BASE_URL}/api/resource/DocType",cookies={

    })
    return response

def get_schema(doctype:str):
    response = call_endpoint_get(f"/api/resource/DocType/{doctype}")['data']
    schema = dict({
        "schema" : {
            "properties" :{}
        }
    })
    schema['name'] = response['name']
    for field in response['fields']:
        schema['schema']['properties'][field['fieldname']] = {
            "fieldtype" : field['fieldtype']
            #"default" : ("" if not 'default' in field.keys() else field['default'])
        }
        if 'default' in field.keys():
            schema['schema']['properties'][field['fieldname']]['default'] = field['default']
    return schema

def insert_data(req_body:dict,doctype:str):
    response = requests.post(f"{BASE_URL}/api/resource/Suppliers",json=req_body,
                             headers={
                                 "Authorization" : auth_header
                             })
    record_id = json.loads(response.content)['data']['name']
    return record_id

def onPublish(text:str,form_name:str):
    form_schema = get_schema(form_name)
    req_body = form_template_single(text,form_schema)
    record_id = insert_data(req_body,form_name)
    webbrowser.open(f"{BASE_URL}/app/{form_name.lower()}/{record_id}")
    return

def call_endpoint_get(endpoint:str):
    #print(f"{BASE_URL}{endpoint}")
    response = requests.get(f"{BASE_URL}{endpoint}",headers={
        "Authorization" : auth_header
    })
    return json.loads(response.content)