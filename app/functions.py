import json
import os
import pathlib
from flask import make_response, send_file, abort
import zipfile
from io import BytesIO
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

module_path = os.environ.get('YATR_MODULE_PATH')

def get_service():
    res = {'modules.v1':'/terraform/modules/v1/'}

    return res

def get_folders(path):
    list = []
    
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            list.append(dir)

    return list

def get_versions(namespace, name, system):
    path = os.path.join(
            module_path,
            system,
            namespace,
            name
        )
    
    if not os.path.exists(path):
        return None
    
    folders = get_folders(path)

    _r = '{"modules": [{"versions": []}]}'
    res = json.loads(_r)

    for module in res['modules']:
        for folder in folders:
            module['versions'].append({'version': folder})
    
    return res

def get_download(namespace, name, system, version):
    path = os.path.join(
            ".",
            "module.zip"
        )
    res = make_response('', 204)
    res.headers['X-Terraform-Get'] = path
    
    return res

def get_module(namespace, name, system, version):
    _p = os.path.join(
            module_path,
            system,
            namespace,
            name,
            version
        )
    
    if not os.path.exists(_p):
        return None
    
    directory = pathlib.Path(_p)
    filestream = BytesIO()

    with zipfile.ZipFile(filestream, 'w', compression=zipfile.ZIP_DEFLATED) as zipObject:
        for file_path in directory.rglob("*"):
            zipObject.write(file_path, arcname=file_path.relative_to(directory))
        zipObject.close()

    filestream.seek(0)
    return send_file(filestream, mimetype='application/zip', as_attachment=True, download_name="module.zip")

