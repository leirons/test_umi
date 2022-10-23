from dependency_injector import containers, providers
from flask import Flask
from core.db.sessions import get_db
from dependency_injector.ext import flask


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    app = flask.Application(Flask, __name__)
    session = providers.Singleton(
        get_db,
    )
