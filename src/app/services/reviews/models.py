from core.db.sessions import Base
from sqlalchemy import Column, Integer, ForeignKey, String, VARCHAR
from sqlalchemy.orm import relationship


class Reviews(Base):
    __tablename__ = "review"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    title = Column(String)
    review = Column(String)

    asin = Column(VARCHAR(20), ForeignKey('product.asin', ondelete="CASCADE"))
    product = relationship("Products", back_populates="reviews")
