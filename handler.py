import json
from exampleco.models.database import Session
from exampleco.models.database.orders import Order, OrderSchema, StatusType, OrderItem
from exampleco.models.database.services import Service, ServiceSchema
import datetime


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).filter(Order.status != StatusType.deleted)  # exclude deleted
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


def filter_orders(event, context):
    params = event.get("pathParameters", {})
    filter_type = params.get("filter_type")
    if filter_type == "THIS_WEEK":
        start_date = datetime.timedelta(weeks=1)
    elif filter_type == "THIS_MONTH":
        start_date = datetime.timedelta(months=1)
    elif filter_type == "THIS_YEAR":
        start_date = datetime.timedelta(years=1)
    else:
        start_date = datetime.datetime.now()  # no results if range option doesnt match
    orders_schema = OrderSchema(many=True)
    orders = Session.query(Order).filter(Order.created_on > start_date,
                                         Order.status != StatusType.deleted)  # exclude deleted
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


def create_new_order(event, context):
    request_data = json.loads(event.get("body"))
    order_description = request_data.get("description", "")
    service_ids = request_data.get("services", [])

    # matching services
    services = Session.query(Service).filter(Service.id.in_(service_ids))

    # make order first
    order = Order(description=order_description, status=StatusType.active)
    Session.add(order)

    # add order items
    total_order_price = 0
    for service in services:
        order_item = OrderItem(
            order=order,
            service=service,
            price=service.price,
            quantity=1,  # assuming fixed 1 quantity for the service
            discount=0,  # assuming 0 discount
        )
        print(service.price)
        total_order_price += service.price
        Session.add(order_item)

    # set order price
    order.total = total_order_price
    Session.commit()
    # response
    order_schema = OrderSchema()
    response_data = order_schema.dump(order)
    response = {"statusCode": 201, "body": json.dumps(response_data)}
    return response


def update_an_order(event, context):
    request_data = json.loads(event.get("body"))
    order_id = request_data.get("id")
    order_description = request_data.get("description", "")
    service_ids = request_data.get("services", [])

    order = Session.query(Order).filter(Order.status != StatusType.deleted, Order.id == order_id).first()

    if order_description:
        order.description = order_description
    if service_ids:
        # remove existing items
        existing_items = Session.query(OrderItem).filter(OrderItem.order_id == order_id)
        existing_items.delete()

        # add new order items
        services = Session.query(Service).filter(Service.id.in_(service_ids))
        total_order_price = 0
        for service in services:
            order_item = OrderItem(
                order=order,
                service=service,
                price=service.price,
                quantity=1,  # assuming fixed 1 quantity for the service
                discount=0,  # assuming 0 discount
            )
            print(service.price)
            total_order_price += service.price
            Session.add(order_item)

        # set order price
        order.total = total_order_price

    Session.commit()

    # response
    order_schema = OrderSchema()
    response_data = order_schema.dump(order)
    response = {"statusCode": 200, "body": json.dumps(response_data)}
    return response


def delete_an_order(event, context):
    request_data = json.loads(event.get("body"))
    order_id = request_data.get("id")

    order = Session.query(Order).get(order_id)
    order.status = StatusType.deleted
    Session.commit()

    response = {"statusCode": 204, "body": None}
    return response


def get_all_services(event, context):
    service_schema = ServiceSchema(many=True)
    services = Session.query(Service).all()
    results = service_schema.dump(services)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


def get_service_by_id(event, context):
    params = event.get("pathParameters", {})
    service_id = params.get("id")

    service_schema = ServiceSchema()
    service = Session.query(Service).get(service_id)
    result = service_schema.dump(service)

    response = {"statusCode": 200, "body": result}

    return response
