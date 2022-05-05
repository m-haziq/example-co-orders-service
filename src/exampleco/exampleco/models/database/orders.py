from sqlalchemy import Column, Float, Integer, text, TEXT, TIMESTAMP
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from .services import ServiceSchema


# TODO: can use enum as well
class StatusType:
    active = 1
    completed = 2
    deleted = 3


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    description = Column(TEXT, nullable=True)
    status = Column(Integer)
    total = Column(Float, nullable=True)
    order_items = relationship("OrderItem", back_populates="order")
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self) -> str:
        return "<Order(total='{}', is_completed='{}', created_on='{}')>".format(
            self.total, self.is_completed, self.created_on
        )


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = fields.Integer()
    description = fields.String()
    status = fields.Integer(validate=validate.OneOf([StatusType.active, StatusType.deleted, StatusType.completed]))
    total = fields.Float()
    order_items = fields.Nested("OrderItemSchema", many=True)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="order_items")
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Service")
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text(
            'CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )


class OrderItemSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItem
        load_instance = True

    id = fields.Integer()
    price = fields.Float()
    discount = fields.Float()
    quantity = fields.Integer()
    service = fields.Nested(ServiceSchema)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()
