from flask import request, jsonify
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from models.order_model import Order
from models.order_item_model import OrderItem
from models.menu_model import Menu

def create_order():
    db: Session = next(get_db())
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    customer_name = data.get("customer_name")
    items_data = data.get("items")

    if not customer_name or not items_data or not isinstance(items_data, list):
        return jsonify({"error": "customer_name and items (list) are required"}), 400

    total_price = 0
    order_items = []

    for item in items_data:
        menu_id = item.get("menu_id")
        quantity = item.get("quantity")

        if not menu_id or not quantity:
            db.close()
            return jsonify({"error": "menu_id and quantity are required for each item"}), 400

        # Ambil harga dari menu
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            db.close()
            return jsonify({"error": f"Menu with id {menu_id} not found"}), 404

        item_price = menu.price
        total_price += quantity * item_price

        order_item = OrderItem(menu_id=menu_id, quantity=quantity, price=item_price)
        order_items.append(order_item)

    # Buat order
    new_order = Order(customer_name=customer_name, total_price=total_price, items=order_items)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # --- Eager load items sebelum session close ---
    order_with_items = db.query(Order)\
                         .options(joinedload(Order.items))\
                         .filter(Order.id == new_order.id)\
                         .first()

    response = order_with_items.to_dict()
    db.close()

    return jsonify({
        "message": "Order created successfully",
        "data": response
    }), 201


def get_all_orders():
    db: Session = next(get_db())
    orders = db.query(Order).options(joinedload(Order.items)).all()
    db.close()
    return jsonify({
        "message": "Success get all orders",
        "data": [o.to_dict() for o in orders]
    }), 200


def get_order_by_id(order_id):
    db: Session = next(get_db())
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    db.close()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "message": "Success get order detail",
        "data": order.to_dict()
    }), 200
