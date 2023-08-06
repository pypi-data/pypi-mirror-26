from .fixtures import server, db, admin, user, bcrypt  # noqa


def pytest_addoption(parser):
    group = parser.getgroup('girder')
    group.addoption('--mock-db', action='store_true', default=False,
                    help='Whether or not to mock the database using mongomock.')
    group.addoption('--mongo-uri', action='store', default='mongodb://localhost:27017',
                    help=('The base URI to the MongoDB instance to use for database connections, '
                          'default is mongodb://localhost:27017'))
    group.addoption('--drop-db', action='store', default='pre', choices=('pre', 'post', 'never'),
                    help='When to destroy testing databases, default is pre (before running tests)')
