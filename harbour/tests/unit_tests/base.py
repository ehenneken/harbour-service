"""
Base properties for all of the unit tests that are shared between each file
"""
import testing.postgresql

from flask.ext.testing import TestCase
from harbour import app

from harbour.models import db


class TestBaseDatabase(TestCase):
    """
    Base test class for when databases are being used.
    """
    postgresql_url_dict = {
        'port': 1234,
        'host': '127.0.0.1',
        'user': 'postgres',
        'database': 'test'
    }
    postgresql_url = 'postgresql://{user}@{host}:{port}/{database}'\
        .format(
            user=postgresql_url_dict['user'],
            host=postgresql_url_dict['host'],
            port=postgresql_url_dict['port'],
            database=postgresql_url_dict['database']
        )

    def create_app(self):
        """
        Create the wsgi application
        """
        app_ = app.create_app()
        app_.config['CLASSIC_LOGGING'] = {}
        app_.config['SQLALCHEMY_BINDS'] = {}
        app_.config['ADS_CLASSIC_MIRROR_LIST'] = [
            'mirror.com', 'other.mirror.com'
        ]
        app_.config['SQLALCHEMY_BINDS']['harbour'] = \
            TestBaseDatabase.postgresql_url

        return app_

    @classmethod
    def setUpClass(cls):
        cls.postgresql = \
            testing.postgresql.Postgresql(**cls.postgresql_url_dict)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    def setUp(self):
        """
        Set up the database for use
        """
        db.create_all()
        self.stub_user_data = {
            'classic_email': 'user@ads.com',
            'classic_password': 'password',
            'classic_mirror': 'mirror.com'
        }

    def tearDown(self):
        """
        Remove/delete the database and the relevant connections
        """
        db.session.remove()
        db.drop_all()