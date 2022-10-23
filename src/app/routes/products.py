from dependency_injector.wiring import inject, Provide
from flask import jsonify, request
from sqlalchemy import select, and_, update
from sqlalchemy.orm import Session
from core.containers import Container
from core.utils.query_worker import get_paginated_list
from app.services.products.models import Products
from app.services.reviews.models import Reviews

from core.utils.cache import cache


@inject
@cache.cached(timeout=10, query_string=True)
def index(product_id, session: Session = Provide[Container.session]):
    session = session.provider.provides()

    query = select(
        Products.title,
        Products.asin,
        Reviews.review,
        Reviews.title).join(Reviews).filter(
        Reviews.asin == Products.asin).where(
            Products.id == product_id)

    data = session.execute(query)
    data = data.all()
    if not data:
        return {"operation":'failed',"status":"404"}
    d = {}

    for i in data:
        if not d.get("product"):
            d.update(
                {
                    "product": {
                        "title": i[0],
                        "asin": i[1],
                        "reviews": []
                    },
                }
            )
        if d.get("product"):
            d.get('product')['reviews'].append(
                {
                    'title': i[3],
                    "review": i[2],
                }
            )
    d['product']['reviews'] = get_paginated_list(
        results=d['product']['reviews'],
        url="/product",
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 20)
    )
    return jsonify(d)


@inject
def create_review(product_id, session: Session = Provide[Container.session]):
    session = session.provider.provides()
    review = request.get_json()

    query = select(Reviews).join(Products).where(Products.id == product_id).where(
        and_(Reviews.title == review.get('title'), Reviews.asin == review.get('asin')))
    data = session.execute(query)
    instance = data.first()
    if instance:
        query = update(Reviews).where(
            and_(
                Reviews.asin == review.get('asin'),
                Reviews.title == review.get('title'))).values(
            **review)
        session.execute(query)
        session.commit()
    else:
        instance = Reviews(**review)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    return review
