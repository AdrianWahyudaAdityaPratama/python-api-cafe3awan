from flask import request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.menu_model import Menu


def get_all_menus():
    db: Session = next(get_db())
    query = db.query(Menu)

    # Ambil query parameters
    search = request.args.get('search')  
    category = request.args.get('category')  

    # Tambahkan filter jika ada
    if search:
        query = query.filter(Menu.name.ilike(f"%{search}%"))  # case-insensitive
    if category:
        query = query.filter(Menu.category == category)

    menus = query.all()
    db.close()

    return jsonify({
        "message": "Success get all menus",
        "data": [menu.to_dict() for menu in menus]
    }), 200


def get_menu_by_id(menu_id):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    db.close()

    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    return jsonify({
        "message": "Success get menu detail",
        "data": menu.to_dict()
    }), 200


def create_menu():
    db: Session = next(get_db())
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    name = data.get("name")
    price = data.get("price")
    category = data.get("category")

    if not name or price is None or not category:
        return jsonify({"error": "name, price, and category are required"}), 400

    new_menu = Menu(
        name=name,
        imageUrl=data.get("imageUrl"),
        price=float(price),
        category=category
    )

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    db.close()

    return jsonify({
        "message": "Menu created successfully",
        "data": new_menu.to_dict()
    }), 201


def update_menu(menu_id):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if not menu:
        db.close()
        return jsonify({"error": "Menu not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    for key in ["name", "imageUrl", "price", "category"]:
        if key in data:
            setattr(menu, key, data[key])

    db.commit()
    db.refresh(menu)
    db.close()

    return jsonify({
        "message": "Menu updated successfully",
        "data": menu.to_dict()
    }), 200


def delete_menu(menu_id):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if not menu:
        db.close()
        return jsonify({"error": "Menu not found"}), 404

    db.delete(menu)
    db.commit()
    db.close()

    return jsonify({
        "message": "Menu deleted successfully"
    }), 200
