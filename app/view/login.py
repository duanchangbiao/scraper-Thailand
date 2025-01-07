import requests
from flask import Blueprint, request

from app.utils.response import success_api

app_router = Blueprint('auth', __name__, url_prefix='/auth')


@app_router.route('/login', methods=['POST'])
def login_required():
    username = request.get_json().get('userName')
    password = request.get_json().get('password')
    print(username, password)
    data = {
        "token": 123456,
        "refresh_token": 123456
    }
    return success_api(data=data)


@app_router.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    data = {
        "userId": "0",
        "userName": "Soybean",
        "roles": [
            "R_SUPER"
        ],
        "buttons": [
            "B_CODE1",
            "B_CODE2",
            "B_CODE3"
        ]
    }
    return success_api(data=data)
