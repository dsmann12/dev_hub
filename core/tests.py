
# Create your tests here.
from abc import ABC, abstractmethod
import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

class CoreE2EBaseTests(ABC):
    """Abstract class containing E2E tests for core app
    
    Inheriting classes should implement their setUpClass and tearDownClass
    methods
    """
    @classmethod
    @abstractmethod
    def setUpClass(cls):
        raise NotImplementedError("Implement setUpClass in base classes")

    @classmethod
    @abstractmethod
    def tearDownClass(cls):
        # super().tearDownClass()
        # cls.browser.close()
        # cls.playwright.stop()
        raise NotImplementedError("Implement tearDownClass in base classes")

    def test_root_url_status_is_200(self):
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

    def test_root_url_title_contains_my_name(self):
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

    def test_expected_section_headings_exist(self):
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

    def test_languages_section_contains_expected_languages(self):
        self._test_list_section_contains_values("Languages", self.get_expected_languages())

    def test_frameworks_section_contains_expected_frameworks(self):
        self._test_list_section_contains_values("Frameworks", self.get_expected_frameworks())

    def test_aws_section_contains_expected_aws_services(self):
        self._test_list_section_contains_values("AWS", self.get_expected_aws_services())

    def test_tools_section_contains_expected_tools(self):
        self._test_list_section_contains_values("Tools", self.get_expected_tools())

    def test_automation_section_contains_expected_automation_tools(self):
        self._test_list_section_contains_values("Automation", self.get_expected_automation_tools())

    def _test_list_section_contains_values(self, section_name, expected_items):
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
    def get_expected_aws_services():
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
    def get_expected_automation_tools():
        return ["Automation Anywhere", "Power Apps", "Power Automate", "Power BI"]



class CoreE2ELocalTests(CoreE2EBaseTests, StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_SETTINGS_MODULE"] = "dev_hub.settings"
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        StaticLiveServerTestCase.setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        StaticLiveServerTestCase.tearDownClass()
        cls.browser.close()
        cls.playwright.stop()


class CoreAcceptanceTests(CoreE2EBaseTests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.live_server_url = os.environ['ACCEPTANCE_TEST_SERVER_URL']

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()