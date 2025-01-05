from flask import Blueprint

app_router = Blueprint('menu', __name__, url_prefix="/systemManage")


@app_router.get("/list")
def getMenuList():
    pass


@app_router.post("/saveMenu")
def saveMenuInfo():
    pass
