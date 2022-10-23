from core.containers import Container
from core.config import Config
from core.db.sessions import engine, Base
from core.utils.to_database import to_database
from parsers.excel_parcer import get_values
from routes import products as product_route
from core.utils.cache import cache

# Решил не использовать алембик, что бы работать автоматически с миграциями, так как не вижу смысла нагружать
# TODO ALEMBIC если будет время
if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    container = Container()
    config = Config()

    app = container.app()
    app.container = container

    products, reviews = get_values()
    to_database(products, reviews)

    cache.init_app(app, config=Config.CACHE)

    app.add_url_rule(
        '/get_product/<int:product_id>',
        view_func=product_route.index,
        methods=["GET"])
    app.add_url_rule(
        '/create_review/<int:product_id>',
        view_func=product_route.create_review,
        methods=["PUT"])

    app.run()
