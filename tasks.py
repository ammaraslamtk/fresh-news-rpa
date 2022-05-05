import logging
import os
import time
from typing import List
from urllib.parse import urlparse

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from selenium.common.exceptions import NoSuchElementException

from utils import configure, get_date_range, search_currency

console_handler = logging.StreamHandler()
logger = logging.getLogger("nytimes")
logger.addHandler(console_handler)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)

browser_lib = Selenium()
excel = Files()

WORKBOOK_NAME = "workbook.xlsx"
SHEET_NAME = "Sheet1"
WEBSITE_URL = "https://nytimes.com"
CONFIG_FILE = "config.json"


def open_excel_book() -> None:
    """
    Open WORKBOOK_NAME if exists or create new workbook
    Use SHEET_NAME
    """
    try:
        excel.open_workbook(WORKBOOK_NAME)
    except FileNotFoundError:
        path = f"{os.path.abspath(os.path.dirname(__file__))}\\{WORKBOOK_NAME}"
        excel.create_workbook(path)
    try:
        excel.set_active_worksheet(SHEET_NAME)
    except ValueError as e:
        if "Unknown worksheet" in e.args[0]:
            excel.create_worksheet(SHEET_NAME)
            excel.set_active_worksheet(SHEET_NAME)


def open_the_website(url: str) -> None:
    """
    Open Website

    Args:
        url: The url to open
    """
    logger.info(f"Opening {url}")
    browser_lib.open_available_browser(url, maximized=True)


def click_search_button() -> None:
    """
    Click the search icon
    """
    search_button = 'css:button[data-test-id="search-button"]'
    browser_lib.click_button(search_button)


def search_for(term: str) -> None:
    """
    Search for a specific term

    Args:
        term: The term to search for
    """
    logger.info(f"Searching {term}")
    click_search_button()
    input_field = "css:input"
    browser_lib.input_text(input_field, term)
    browser_lib.press_keys(input_field, "ENTER")


def click_date_range() -> None:
    """
    Click date range dropdown
    """
    button = 'css:button[data-testid="search-date-dropdown-a"]'
    browser_lib.click_button(button)


def click_section() -> None:
    """
    Click section dropdown
    """
    button = 'css:button[data-testid="search-multiselect-button"]'
    browser_lib.click_button(button)


def select_section(section: str) -> None:
    """
    Select the particular section

    Args:
        section: Section to select
    """
    logger.info(f"Setting section to {section}")
    click_section()
    button = f'css:button[value^="{section}"], input[value^="{section}"]'
    try:
        browser_lib.click_button_when_visible(button)
    except AssertionError:
        logging.error(
            f"Section {section} was not found for filteration, skipping section"
        )


def select_date_range(months: int) -> None:
    """
    Enter the date range back to the given number of
    months from today

    Args:
        months: The number of months to look back for
    """
    click_date_range()
    button = 'css:button[value="Specific Dates"]'
    input_start, input_end = "id:startDate", "id:endDate"
    browser_lib.click_button(button)
    start_date, end_date = get_date_range(months)
    logger.info(f"Searching from {start_date} to {end_date}")
    browser_lib.input_text(input_start, start_date)
    browser_lib.input_text(input_end, end_date)
    browser_lib.press_keys(input_end, "ENTER")


def store_excel(news: List[tuple]) -> None:
    """
    Store list of items in excel sheet

    Args:
        news: List of news to store
    """
    excel.append_rows_to_worksheet(news)
    excel.save_workbook()


def get_news_lists(phrase: str) -> None:
    """
    Get the list of news items

    Args:
        phrase: The phrase that is being searched

    Returns:
        List of news items
    """
    http = HTTP()
    # Wait for the filter to fetch new data
    # There was no apparent function available to detect DOM changes
    time.sleep(2)
    phrase = phrase.lower()
    li_select = 'css:li[data-testid="search-bodega-result"]'
    date_select = 'span[data-testid="todays-date"]'
    elements = browser_lib.find_elements(li_select)
    news = []
    for element in elements:
        title = element.find_element_by_tag_name("h4").text
        date = element.find_element_by_css_selector(date_select).text
        try:
            description = (
                element.find_element_by_tag_name("a").find_element_by_tag_name("p").text
            )
        except NoSuchElementException:
            description = None
        try:
            image = element.find_element_by_tag_name("img").get_attribute("src")
            path = urlparse(image).path.rsplit("/", 1)[-1]
            http.download(image, path)
        except NoSuchElementException:
            image, path = None, None
        title_count, desc_count = title.lower().count(
            phrase
        ), description.lower().count(phrase)
        has_money = bool(search_currency(title) or search_currency(description))
        item = title, date, description, image, title_count, desc_count, has_money, path
        news.append(item)
    return news


def main():
    """
    The main function
    """
    search_phrase, section, months = configure(CONFIG_FILE)
    open_excel_book()
    try:
        open_the_website(WEBSITE_URL)
        search_for(search_phrase)
        select_date_range(months)
        select_section(section)
        news = get_news_lists(search_phrase)
        store_excel(news)
    finally:
        browser_lib.close_all_browsers()
        excel.close_workbook()


if __name__ == "__main__":
    main()
