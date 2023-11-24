from flask_restful import Resource, reqparse
from models.orders import Order, OrderItem
from db import db
from flask import jsonify, request

class OrderResource(Resource):
    def post(self):
        data = request.get_json()

        new_order = Order(status=data['status'])
        db.session.add(new_order)

        for item in data['items']:
            new_item = OrderItem(
                item_name=item['item_name'],
                quantity=item['quantity'],
                order=new_order
            )
            db.session.add(new_item)

        db.session.commit()

        return jsonify(message='Order created successfully')

    def put(self, order_id):
        data = request.get_json()
        order = Order.query.get(order_id)

        if order:
            order.status = data['status']

            # Clear existing items
            OrderItem.query.filter_by(order_id=order.id).delete()

            # Add new items
            for item in data['items']:
                new_item = OrderItem(
                    item_name=item['item_name'],
                    quantity=item['quantity'],
                    order=order
                )
                db.session.add(new_item)

            db.session.commit()

            return jsonify(message=f'Order {order_id} updated successfully')
        else:
            return jsonify(message='Order not found'), 404


    def get(self, order_id):
        order = Order.query.get(order_id)
        items = OrderItem.query.filter(OrderItem.order_id == order.id).all()
        if order:
            order_details = {
                'id': order.id,
                'status': order.status,
                'items': [{'item_name': item.item_name, 'quantity': item.quantity} for item in items]
            }
            return jsonify(order=order_details)
        else:
            return jsonify(message='Order not found'), 404