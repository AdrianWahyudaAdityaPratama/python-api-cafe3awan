from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from config.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(255), nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "items": [item.to_dict() for item in self.items]
        }
