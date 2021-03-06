import contextlib
import os

import pytest
from flask import Response, _app_ctx_stack, _request_ctx_stack, json
from sqlalchemy import event
from sqlalchemy.pool import Pool
from werkzeug import cached_property

from diilikone import Application, load_models
from diilikone.extensions import db


class DatabaseGuard(object):

    def __init__(self, enabled=True):
        self.enabled = True
        event.listen(Pool, 'connect', self.on_connect)

    def on_connect(self, dbapi_connection, connection_record):
        if self.enabled:
            raise Exception(
                'Test cases that are not marked that they use database '
                'should not use database.'
            )

    @contextlib.contextmanager
    def disabled(self):
        was_enabled = self.enabled
        self.enabled = False
        yield
        self.enabled = was_enabled


@pytest.fixture(scope='session', autouse=True)
def database_guard():
    """
    Prevent database access from tests not marked to use database

    We want to do this as otherwise our connection pool is not disposed
    and connection to database server stays alive and may cause
    problems.
    """
    return DatabaseGuard()


def _get_process_number(config):
    SLAVE_ID_PREFIX_LENGTH = 2
    try:
        slaveid = config.slaveinput['slaveid']
    except AttributeError:
        zero_based_process_number = 0
    else:
        zero_based_process_number = int(slaveid[SLAVE_ID_PREFIX_LENGTH:])
    return zero_based_process_number + 1


def _set_process_number_to_env(config):
    number = _get_process_number(config)
    os.environ['TEST_PROCESS_NUMBER'] = '' if number == 1 else str(number)


def pytest_configure(config):
    _set_process_number_to_env(config)


class TestResponse(Response):
    @cached_property
    def json(self):
        return json.loads(self.data)


@pytest.fixture(scope='session')
def app(request):
    app = Application('test')
    app.response_class = TestResponse

    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@pytest.fixture
def app_ctx(request, app):
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)
    return ctx


@pytest.fixture(scope='class')
def app_ctx_in_class_scope(request, app):
    return app_ctx(request, app)


@pytest.yield_fixture
def request_ctx(request, app):
    ctx = app.test_request_context()
    ctx.push()
    yield ctx
    if _request_ctx_stack.top and _request_ctx_stack.top.preserved:
        _request_ctx_stack.top.pop()
    ctx.pop()


@pytest.fixture
def logged_in_user():
    return None


@pytest.fixture
def client(request, app, database):
    return app.test_client()


@pytest.yield_fixture(scope='session')
def database_schema(request, app, database_guard):
    with database_guard.disabled(), app.app_context():
        load_models()
        db.create_all()

    yield

    with database_guard.disabled(), app.app_context():
        db.drop_all()


def _database(database_guard):
    with database_guard.disabled():
        yield

        db.session.remove()

        # Delete all data from tables.
        tables = reversed(db.metadata.sorted_tables)
        for table in tables:
            db.session.execute(table.delete())
        db.session.commit()

        db.session.close_all()
        db.engine.dispose()

    _app_ctx_stack.top.sqlalchemy_queries = []


@pytest.yield_fixture
def database(database_schema, database_guard, app_ctx):
    for x in _database(database_guard):
        yield x


@pytest.yield_fixture(scope='class')
def database_in_class_scope(
    database_schema, database_guard, app_ctx_in_class_scope
):
    for x in _database(database_guard):
        yield x


@pytest.yield_fixture(scope='module')
def database_in_module_scope(
    database_schema, database_guard, app_ctx_in_module_scope
):
    for x in _database(database_guard):
        yield x
