
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
    
    def test_work_experience_section_contains_expected_values(self):
        """Helper to test the work experience section."""
        # Arrange
        expected_experience = self.get_expected_work_experience()
        page = self.browser.new_page()

        # Act
        page.goto(f"{self.live_server_url}/")
        
        # Assert
        work_experience_sections = page.locator(".work_history_item").all()
        extracted_experience = []
        
        for section in work_experience_sections:
            job_title = section.locator("h4").inner_text()
            timeline = section.locator("div").inner_text()
            bullets = section.locator("+ section ul li").all_inner_texts()
            extracted_experience.append((job_title, timeline, bullets))
        
        self.assertListEqual(sorted(extracted_experience), sorted(expected_experience), "Mismatch in work experience section")
        
        # Cleanup
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
        # Arrange
        page = self.browser.new_page()

        ## act
        page.goto(f"{self.live_server_url}/")
        
        # Assert
        items = page.locator(f"h4:has-text('{section_name}') + ul li").all_inner_texts()
        self.assertListEqual(sorted(items), sorted(expected_items), f"Mismatch in {section_name} section")
        
        # Cleanup
        page.close()
    
    def test_contact_section_contains_expected_links(self):
        # Arrange
        expected_contact_links = self.get_expected_contact_links()
        page = self.browser.new_page()

        # Act
        page.goto(f"{self.live_server_url}/")
        
        # Assert
        # Locate the entire CONTACT section
        contact_section = page.locator("section:has(h4:has-text('CONTACT'))")

        # Get all anchor elements within the CONTACT section
        contact_links = contact_section.locator("a").all()
        extracted_links = [(link.inner_text(), link.get_attribute("href")) for link in contact_links]
        
        self.assertListEqual(sorted(extracted_links), sorted(expected_contact_links), "Mismatch in contact section")
        
        # Cleanup
        page.close()
    
    def test_cv_section_contains_expected_link(self):
        # Arrange
        expected_link = self.get_expected_cv_link()
        page = self.browser.new_page()

        # Act
        page.goto(f"{self.live_server_url}/")
        
        # Assert
        # Locate the C.V. section and extract the href
        cv_link = page.locator("section#cv a")
        extracted_link = cv_link.get_attribute("href")
        
        self.assertEqual(extracted_link, expected_link, "C.V. link mismatch")
        
        # Cleanup
        page.close()

    @staticmethod
    def get_expected_intro():
        return """
            My name is David Scheuermann
            I am a software developer.
        """.strip()

    @staticmethod
    def get_expected_work_experience():
        return [
            (
                "AI Software Engineer III", "[2024-Present]",
                [
                    "Led development of a chatbot utilizing Retrieval Augmented Generation (RAG) and Agentic AI to answer questions about company policies and information. Developed on AWS with Python and React.",
                    "Built the CI/CD pipeline for the project utilizing GitHub Actions with thorough automated testing through multi-stage deployments. Shared knowledge of CI/CD and testing with my department.",
                    "Responsible for building and managing the infrastructure through Infrastructure as Code (IaC) with AWS Serverless Application Model (SAM) and CloudFormation.",
                    "Minor contributions to the frontend developed with React and TypeScript",
                    "Empowered new and junior developers to safely contribute through pair programming sessions",
                ]
            ),
            (
                "Automation Analyst III", "[2022-2024]",
                [
                    "Developed 5 applications to capture Nuclear regulatory data, track their approvals, and automatically release a mandatory monthly report to all stakeholders, saving over $1 million annually.",
                    "Developed applications using Microsoft Power Apps to supply an intuitive UI quickly. Created and managed a Microsoft SQL Server database to store and serve complex relational data for the applications and reports. Developed notification and approval systems using Microsoft Power Automate.",
                    "Heavily involved in client discussions when gathering requirements and project management",
                ]
            ),
            (
                "Automation Analyst II", "[2020-2022]",
                [
                    "Developed a .NET DLL allowing Automation Anywhere RPA bots to programmatically interact with Microsoft Excel files for various tasks, allowing RPA developers to develop more quickly and reliably.",
                    "Instrumental in initiating development of a shared library of automation code for various applications within the company. Led monthly meetings to foster discussion and track progress of development",
                ]
            ),
            (
                "RPA Developer Intern", "[2018-2020]",
                [
                    "Developed multiple RPA bots using Automation Anywhere and .NET to automate various tasks within the company, saving multiple FTEs worth of time annually and freeing employees for higher priority work",
                ]
            ),
        ]


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

    @staticmethod
    def get_expected_contact_links():
        return [
            ("GITHUB", "https://github.com/dsmann12"),
            ("LINKEDIN", "https://www.linkedin.com/in/david-scheuermann-a5332148/"),
            ("EMAIL", "mailto:david.scheuermann3@gmail.com"),
            ("MASTODON", "https://fosstodon.org/@dsmann"),
            ("TWITTER", "https://twitter.com/dsmann1212")
        ]

    @staticmethod
    def get_expected_cv_link():
        return "https://drive.google.com/file/d/1MwEGpyhif-bm99qETTHrDYSVexKZcABH/view?usp=drive_link"


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