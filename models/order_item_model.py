from sqlalchemy import Column, Integer, Float, ForeignKey
from config.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # price per item

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "menu_id": self.menu_id,
            "quantity": self.quantity,
            "price": self.price,
        }
