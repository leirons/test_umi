from core.db.sessions import Base
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.orm import relationship


class Products(Base):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    asin = Column(VARCHAR(20), unique=True)
    title = Column(String)

    reviews = relationship(
        "Reviews",
        back_populates='product',
        cascade="all,delete")
