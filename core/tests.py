
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

    def test_intro_section_exists(self):
        """Test that the intro section exists."""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        intro_section = page.locator("section#intro")
        self.assertTrue(intro_section.count() > 0, "Expected an intro section with id 'intro'")
        page.close()

    def test_section_headings(self):
        """Test that required section headings exist on the page."""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        
        expected_sections = [
            "Experience", "Languages", "Frameworks", "AWS",
            "Tools", "Automation", "Contact"
        ]
        
        for section in expected_sections:
            heading = page.locator(f"h4:has-text('{section}')").first
            self.assertTrue(heading.is_visible(), f"Expected {section} heading not found")
        
        page.close()

    def test_languages_section(self):
        self._test_list_section("Languages", self.get_expected_languages())

    def test_frameworks_section(self):
        self._test_list_section("Frameworks", self.get_expected_frameworks())

    def test_aws_section(self):
        self._test_list_section("AWS", self.get_expected_aws())

    def test_tools_section(self):
        self._test_list_section("Tools", self.get_expected_tools())

    def test_automation_section(self):
        self._test_list_section("Automation", self.get_expected_automation())

    def _test_list_section(self, section_name, expected_items):
        """Helper to test list-based sections."""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        
        items = page.locator(f"h4:has-text('{section_name}') + ul li").all_inner_texts()
        self.assertListEqual(sorted(items), sorted(expected_items), f"Mismatch in {section_name} section")
        
        page.close()

    @staticmethod
    def get_expected_intro():
        return """
            My name is David Scheuermann
            I am a software developer.
        """.strip()

    @staticmethod
    def get_expected_languages():
        return ["Python", "TypeScript", "JavaScript", "C#", "HTML", "SQL"]

    @staticmethod
    def get_expected_frameworks():
        return ["React", "Django", "LangChain", "Express", "Next.js", "vite"]

    @staticmethod
    def get_expected_aws():
        return [
            "EC2", "Lambda", "API Gateway", "DynamoDB", "RDS",
            "ECS", "OpenSearch", "Bedrock", "CloudFormation"
        ]

    @staticmethod
    def get_expected_tools():
        return [
            "git", "PostgreSQL", "SQL Server", "Docker", "AWS Serverless Application Model (SAM)",
            "pytest", "Visual Studio", "Visual Studio Code", "vim"
        ]

    @staticmethod
    def get_expected_automation():
        return ["Automation Anywhere", "Power Apps", "Power Automate", "Power BI"]
