from flask import Flask, request

app = Flask(__name__)
USERS = {}

@app.route("/admin/delete_user", methods=["POST"])
def delete_user():
    # VULN: no authentication / authorization check
    USERS.pop(request.form["user_id"], None)
    return "deleted"
