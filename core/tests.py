
# Create your tests here.
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

class CoreEndToEndTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_SETTINGS_MODULE"] = "dev_hub.settings"
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_root_url_status(self):
        """Test the root URL returns a successful status (200)."""
        # Arrange
        page = self.browser.new_page()

        # Act
        response = page.goto(f"{self.live_server_url}/")

        # Assert
        status = response.status
        self.assertEqual(status, 200, f"Expected status code 200 but got {status}")

        # Clean
        page.close()

    def test_root_url_title(self):
        """Test the root URL contains the correct title."""
        # Arrange
        page = self.browser.new_page()

        # Act
        page.goto(f"{self.live_server_url}/")

        # Assert
        title = page.title()
        self.assertIn("David Scheuermann", title, f"Expected title to contain 'David Scheuermann' but got {title}")

        # Clean
        page.close()