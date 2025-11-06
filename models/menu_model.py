from sqlalchemy import Column, Integer, String, Float, Text
from config.database import Base  # impor Base dari config


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    imageUrl = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "imageUrl": self.imageUrl,
            "price": self.price,
            "category": self.category,
        }
