from datetime import datetime
from flask import Flask, jsonify
from . import app
from .functions import *

# 
@app.route("/")
def index():
    return "Registry Active"

@app.route("/debug")
def debug():
    return f"Flask debug mode: {app.debug}"

# Service discovery 
@app.route("/.well-known/terraform.json")
def get_service_discovery():
    response = jsonify(get_service())
    return response

# List versions available for specific module
@app.route("/terraform/modules/v1/<namespace>/<name>/<system>/versions")
def get_list_versions(namespace, name, system):
    response = jsonify(get_versions(namespace, name, system))

    if response is None:
        abort(404)
    
    return response

# Get download location for specific module version
@app.route("/terraform/modules/v1/<namespace>/<name>/<system>/<version>/download")
def get_version_download(namespace, name, system, version):
    response = get_download(namespace, name, system, version)
    return response

# Download archive for a specific module version
@app.route("/terraform/modules/v1/<namespace>/<name>/<system>/<version>/module.zip")
def get_module_file(namespace, name, system, version):
    response = get_module(namespace, name, system, version)

    if response is None:
        abort(404)
    
    return response