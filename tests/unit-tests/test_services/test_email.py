import unittest

from fastapi_mail import ConnectionConfig

from server.core.config import settings
from server.services.email import get_mail_config


class TestGetMailConfig(unittest.TestCase):
    def test_get_mail_config(self):
        conf = get_mail_config()

        # Verify that the function returns a valid ConnectionConfig object
        self.assertIsInstance(conf, ConnectionConfig)

        # Verify that the ConnectionConfig object has the correct values
        self.assertEqual(conf.MAIL_USERNAME, settings.MAIL_USERNAME)
        self.assertEqual(conf.MAIL_PASSWORD, settings.MAIL_PASSWORD)
        self.assertEqual(conf.MAIL_FROM, settings.MAIL_FROM)
        self.assertEqual(conf.MAIL_PORT, settings.MAIL_PORT)
        self.assertEqual(conf.MAIL_SERVER, settings.MAIL_SERVER)
        self.assertEqual(conf.MAIL_FROM_NAME, settings.MAIL_FROM_NAME)
        self.assertEqual(conf.MAIL_STARTTLS, settings.MAIL_STARTTLS)
        self.assertEqual(conf.MAIL_SSL_TLS, settings.MAIL_SSL_TLS)
        self.assertEqual(conf.USE_CREDENTIALS, settings.USE_CREDENTIALS)

    def test_get_mail_config_missing_settings(self):
        with self.assertRaises(Exception):
            settings.MAIL_USERNAME = None
            get_mail_config()
