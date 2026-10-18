import os
import subprocess
from flask import request

def ping():
    host = request.args.get("host")
    # VULN: shell injection from unvalidated input
    return subprocess.check_output("ping -c 1 " + host, shell=True)

def read_file():
    name = request.args.get("name")
    # VULN: path traversal
    return open(os.path.join("/var/data", name)).read()

def calc():
    # VULN: eval of user input
    return str(eval(request.args.get("expr")))
