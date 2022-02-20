from fastapi import APIRouter, HTTPException, Form

from ..objects.users import User
from ..typing.models import UserOut
from ..Utils.tokens import encrypt_password
from ..db.controller import query_db, ControllerError

router = APIRouter(
    prefix='/auth',
    tags=["auth"],
    dependencies=[],
    responses={404: {"detail": "Not found."}},
)

@router.post("/register", response_model=UserOut)
async def register(
    username: str = Form(..., title="Username.", description="The username with which you will eventually login."),
    password: str = Form(..., title="Password.", description="Password with which you will eventually login."),
    name: str = Form(None, title="Name.", description="Your name. Which one is up to you. This will be shown in various menus to refer to you."),
    email: str = Form(None, title="Email", description="Email to which you want to receive information from me.")):
    user = User(username=username, password=encrypt_password(password), name=name, email=email)
    sql = user.register()
    try:
        results = query_db(sql, True)
    except ControllerError as err:
        raise HTTPException(500, "Could not register user!") from err
    else:
        if results == True:
            return dict(user)
        raise HTTPException(500, "Something went wront when trying to register user!")

@router.post("/login", response_model=UserOut)
async def login(
    username: str = Form(..., title="Username.", description="The username with which you registered."),
    password: str = Form(..., title="Password.", description="The password with which you registered.")
):
    user = User(username=username, password=encrypt_password(password))
    sql = user.login()
    try:
        results = query_db(sql)
    except ControllerError as err:
        raise HTTPException(500, "SQL Error! Could not login user!")
    else:
        user.name = results[0][1]
        user.email = results[0][2]
    
    return dict(user)
    