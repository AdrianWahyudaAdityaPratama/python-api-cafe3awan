from flask import Blueprint
from controllers.menu_controller import (
    get_all_menus,
    get_menu_by_id,
    create_menu,
    update_menu,
    delete_menu
)

menu_bp = Blueprint("menus", __name__)

# Routes CRUD Menu
menu_bp.route("/", methods=["GET"])(get_all_menus)
menu_bp.route("/<int:menu_id>", methods=["GET"])(get_menu_by_id)
menu_bp.route("/", methods=["POST"])(create_menu)
menu_bp.route("/<int:menu_id>", methods=["PUT", "PATCH"])(update_menu)
menu_bp.route("/<int:menu_id>", methods=["DELETE"])(delete_menu)
