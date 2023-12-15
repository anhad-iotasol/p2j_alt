import requests
import json
from pathlib import Path
import webbrowser
from dotenv import load_dotenv,find_dotenv
import os

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
    print(response.json())
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
