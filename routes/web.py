from flask import Blueprint
from controllers.menu_controller import (
    get_all_menus,
    get_menu_by_id,
    create_menu,
    update_menu,
    delete_menu
)
from controllers.order_controller import create_order, get_all_orders, get_order_by_id


menu_bp = Blueprint("menus", __name__)

# Routes CRUD Menu
menu_bp.route("/", methods=["GET"])(get_all_menus)
menu_bp.route("/<int:menu_id>", methods=["GET"])(get_menu_by_id)
menu_bp.route("/", methods=["POST"])(create_menu)
menu_bp.route("/<int:menu_id>", methods=["PUT", "PATCH"])(update_menu)
menu_bp.route("/<int:menu_id>", methods=["DELETE"])(delete_menu)

order_bp = Blueprint("orders", __name__)

# Routes Order
order_bp.route("/", methods=["POST"])(create_order)
order_bp.route("/", methods=["GET"])(get_all_orders)
order_bp.route("/<int:order_id>", methods=["GET"])(get_order_by_id)