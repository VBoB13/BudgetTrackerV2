from fastapi import APIRouter, HTTPException, Form

from api.Utils.exceptions import AuthError

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


@router.get("/get_all_users")
async def get_all_users():
    sql = User.get_all_users()
    results = query_db(sql)
    output_list = []
    for user in results:
        output_list.append(dict(User(user)))
    return {
        "users": output_list
    }


@router.post("/register", response_model=UserOut)
async def register(
        username: str = Form(..., title="Username.",
                             description="The username with which you will eventually login."),
        password: str = Form(..., title="Password.",
                             description="Password with which you will eventually login."),
        name: str = Form(
            None, title="Name.", description="Your name. Which one is up to you. This will be shown in various menus to refer to you."),
        email: str = Form(None, title="Email", description="Email to which you want to receive information from me.")):
    user = User(username=username, password=encrypt_password(
        password), name=name, email=email)
    sql = user.register()
    try:
        results = query_db(sql, True)
        if results == True:
            sql = user.get_user_by_username()
            results = query_db(sql)
            user.id = results[0][0]
    except ControllerError as err:
        raise HTTPException(500, "Could not register user!") from err
    else:
        return dict(user)


@router.post("/login", response_model=UserOut)
async def login(
    username: str = Form(..., title="Username.",
                         description="The username with which you registered."),
    password: str = Form(..., title="Password.",
                         description="The password with which you registered.")
):
    user = User(username=username, password=encrypt_password(password))
    sql = user.login()
    try:
        results = query_db(sql)
    except ControllerError as err:
        raise HTTPException(500, "SQL Error! Could not login user!")
    else:
        if len(results) > 0:
            user.id = results[0][0]
            user.username = results[0][1]
            user.name = results[0][2]
            user.email = results[0][3]
            return dict(user)
        raise HTTPException(401, "Wrong username and/or password!")
