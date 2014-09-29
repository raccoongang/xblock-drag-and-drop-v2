# Imports ###########################################################

from workbench import scenarios
from workbench.test.selenium_test import SeleniumTest

from tests.utils import load_scenarios_from_path


# Classes ###########################################################

class BaseIntegrationTest(SeleniumTest):

    def setUp(self):
        super(BaseIntegrationTest, self).setUp()

        self.browser.get(self.live_server_url)  # Needed to load scenarios once
        scenarios.SCENARIOS.clear()
        for identifier, title, xml in self._get_scenarios_for_test():
            scenarios.add_xml_scenario(identifier, title, xml)
            self.addCleanup(scenarios.remove_scenario, identifier)

        self.browser.get(self.live_server_url)

        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock scenarios')

    def _get_scenarios_for_test(self):
        return load_scenarios_from_path('integration/data')

    def go_to_page(self, page_name, css_selector='section.xblock--drag-and-drop'):
        """
        Navigate to the page `page_name`, as listed on the workbench home
        Returns the DOM element on the visited page located by the `css_selector`
        """
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text(page_name).click()
        return self.browser.find_element_by_css_selector(css_selector)

    def get_element_html(self, element):
        return element.get_attribute('innerHTML').strip()


class SingleScenarioIntegrationTest(BaseIntegrationTest):
    def setUp(self):
        super(SingleScenarioIntegrationTest, self).setUp()

    def _get_scenarios_for_test(self):
        identifier, title, scenario = self._get_scenario_for_test()
        self._page_title = title
        return [(identifier, title, scenario)]