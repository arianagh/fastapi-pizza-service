from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from starlette.responses import Response

from db import Session, engine
from models import Order, User
from schema import OrderModel, OrderStatus

router = APIRouter(prefix='/order', tags=['order'])


session = Session(bind=engine)


@router.post('/order', status_code=201)
async def place_an_order(order: OrderModel, authorize: AuthJWT = Depends()):
    """
    ## Placing an order
    This requires the following:
    - quantity: int
    - pizza_size: str
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')

    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size
    )
    new_order.user = user
    session.add(new_order)
    session.commit()
    result = {
        'pizza_size': new_order.pizza_size,
        'quantity': new_order.quantity,
        'id': new_order.id,
        'order_status': new_order.order_status
    }
    return result


@router.get('/orders-list')
async def list_all_orders(authorize: AuthJWT = Depends()):
    """
    ## List orders
    This returns all orders made and can be accessed only by the superuser.
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()
        return orders
    raise HTTPException(status_code=401,
                        detail='You are not a superuser!')


@router.get('/order/{order_id}')
async def get_order(order_id: int, authorize: AuthJWT = Depends()):
    """
    ## Get an order by its id
    This returns an order and can be accessed only by the superuser.
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).filter(Order.id == order_id).first()
        if orders:
            return orders
        raise HTTPException(status_code=400, detail='Order does not exist!')
    raise HTTPException(status_code=401,
                        detail='You are not a superuser!')


@router.delete('/order/{order_id}')
async def delete_order(order_id: int, authorize: AuthJWT = Depends()):
    """
    ## Delete an order
    This deletes an order and can be accessed only by superuser.
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        session.query(Order).filter(Order.id == order_id).delete()
        session.commit()
        return Response(status_code=200)
    raise HTTPException(status_code=401,
                        detail='You are not a superuser!')


@router.get('/order/users/orders')
async def get_user_orders(authorize: AuthJWT = Depends()):
    """
    ## Get a current user orders
    This return all orders made by the current user.
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    return jsonable_encoder(user.order)


@router.get('/order/users/{order_id}')
async def get_user_order(order_id: int, authorize: AuthJWT = Depends()):
    """
    ## Get a current user order
    This return an specific order by its id made by the current user.
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    user_orders = user.order
    for order in user_orders:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=400, detail='No such order!')


@router.put('/order/update/{order_id}')
def update_order(order_id: int, order: OrderModel, authorize: AuthJWT = Depends()):
    """
    ## Updating an order
    This requires the following:
    - quantity: int
    - pizza_size: str
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    order_to_update = session.query(Order).filter(Order.id == order_id).first()
    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size
    session.commit()
    return Response(status_code=202)


@router.patch('/order/update/{order_id}')
def update_order_status(order_id: int, order: OrderStatus, authorize: AuthJWT = Depends()):
    """
    ## Placing an order status
    This requires the following:
    - order_status: str
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401,
                            detail='Invalid auth token!')
    current_user = authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == order_id).first()
        order_to_update.order_status = order.order_status
        session.commit()
        response = {
            'id': order_to_update.id,
            'order_status': order_to_update.order_status
        }
        return response
    raise HTTPException(status_code=401,
                        detail='You are not a superuser!')
