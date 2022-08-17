from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash

from db import Session, engine
from models import User
from schema import SignUp, Login

router = APIRouter(prefix='/auth', tags=['auth'])

session = Session(bind=engine)


@router.get('/')
async def hello_auth(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token!')
    return {'message': 'hello_auth'}


@router.post('/signup', status_code=201)
async def sign_up_user(user: SignUp):

    """
    ## Creating a user
    This requires the following:
    - username: str
    - email: str
    - password: str
    - is_active: str
    - is_staff: str
    """
    db_user = session.query(User).filter(user.email == User.email).first()

    if db_user is not None:
        return HTTPException(status_code=400, detail='user already exists')

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()
    return new_user


@router.post('/login', status_code=200)
async def login(user: Login, authorize: AuthJWT = Depends()):
    """
    ## Login a user
    This requires the following and returns a token pair 'access' and 'refresh':
    - username: str
    - password: str
    """
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = authorize.create_access_token(subject=db_user.username)
        refresh_token = authorize.create_refresh_token(subject=db_user.username)
        result = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return jsonable_encoder(result)
    return HTTPException(status_code=400, detail='invalid user login')


@router.get('/refresh')
async def refresh_token(authorize: AuthJWT = Depends()):
    """
    ## Create a fresh token
    it requires an refresh token
    """
    try:
        authorize.jwt_refresh_token_required()
    except Exception as e:
        return HTTPException(status_code=400, detail='invalid refresh token')
    current_user = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=current_user)
    result = {
        'access_token': access_token
    }
    return jsonable_encoder(result)




