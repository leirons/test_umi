from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session
from core.containers import Container
from app.services.products.models import Products
from app.services.reviews.models import Reviews


@inject
def to_database(products, reviews, session: Session = Provide[Container.session]):
    session = session.provider.provides()

    for product in products:
        title = product[0]
        asin = product[1]
        instance = Products(asin=asin, title=title)
        session.add(instance)
        session.commit()
        session.refresh(instance)

    for review in reviews:
        asin = review[0]
        title = review[1]
        rev = review[2]

        instance = Reviews(asin=asin, title=title, review=rev)

        session.add(instance)
        session.commit()
        session.refresh(instance)
