import os
import re

from bs4 import BeautifulSoup

from models.schemas import (
    Issue,
    Source,
    Link,
    Category,
    Column,
)
from utils.scraper import Scraper
from utils.logging import get_logger


logger = get_logger('python_weekly.py')


class PythonWeekly:
    # Homepage: https://www.pythonweekly.com/
    ANCHOR_TEXT_TITLE = '^Welcome\sto\sissue\s[0-9]{1,3}\sof\sPython\sWeekly'
    ANCHOR_TEXT_ARTICLE = 'Articles,\sTutorials\sand\sTalks'
    ANCHOR_TEXT_LIBRARY = 'Interesting\sProjects,\sTools\sand\sLibraries'
    ANCHOR_TEXT_NEW_RELEASES = 'New\sReleases'
    ANCHOR_TEXT_UPCOMING_EVENTS = 'Upcoming\sEvents\sand\sWebinars'

    PAGE_URL = 'https://www.pythonweekly.com/archive/{0}.html'
    PAGE_NAME = 'python_weekly_{0}.html'

    def __init__(self, issue_number: int):
        if issue_number is None:
            raise Exception('Issue number must not be none.')

        source = Source(
            name='python_weekly',
            display_name='Python Weekly',
        )
        self.issue = Issue(
            source=source,
            number=issue_number,
            columns=[],
        )

        # Create categories.
        self.category_article = Category(
            name='article',
        )
        self.category_library = Category(
            name='library',
        )
        self.category_new_release = Category(
            name='new_release',
        )
        self.category_upcoming = Category(
            name='upcoming',
        )

        # Init flags.
        self.column = None
        self.previous_item = None

    def run(self):
        # Scrape the page.
        logger.info(f'Scrape Python Weekly issue: {self.issue.number}')
        scraper = Scraper(
            url=self.PAGE_URL.format(self.issue.number),
            page_name=self.PAGE_NAME.format(self.issue.number),
        )

        # Scrape the webpage.
        scraper.scrape()

        # Parse content.
        self.parse_content()

        for column in self.issue.columns:
            logger.info(column.title)
            logger.info(column.link.url)
            logger.info(column.description)
            logger.info('--------------------------------------------')

        logger.info('********************************************')
        logger.info('***           END OF ISSUE               ***')
        logger.info('********************************************')

    def get_file_path(self):
        return os.path.join(
            'archived',
            f'python_weekly_{self.issue.number}.html',
        )

    def save_page_title(self, item: BeautifulSoup) -> None:
        pass

    def save_article(self, item: BeautifulSoup) -> None:
        return self.save_item(item=item, category=self.category_article)

    def save_library(self, item: BeautifulSoup) -> None:
        return self.save_item(item=item, category=self.category_library)

    def save_new_release(self, item: BeautifulSoup) -> None:
        return self.save_item(item=item, category=self.category_new_release)

    def save_upcoming_events(self, item: BeautifulSoup) -> None:
        return self.save_item(item=item, category=self.category_upcoming)

    def save_item(self, item: BeautifulSoup, category: Category) -> None:
        # Try to find a tag.
        hyperlink_tag = item.find('a')

        if hyperlink_tag and self.column is None:
            # This must be the title of the column.
            link = Link(
                text=hyperlink_tag.text.strip(),
                url=hyperlink_tag['href'],
            )
            self.column = Column(
                link=link,
                title=link.text.strip(),
                category=category,
                description=None,
                tags=[],
            )
            self.previous_item = item
        elif self.column \
                and item.name == 'div' \
                and self.previous_item.text.strip() != item.text.strip():
            # This must be the description.
            self.column.description = item.text.strip()
            self.issue.columns.append(self.column)
            self.column = None

    def parse_content(self):
        file_path = self.get_file_path()
        with open(file_path, 'r') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        items = soup.find('table', class_='backgroundTable') \
                    .find('table', id='contentTable') \
                    .find('table', class_='bodyTable') \
                    .find('td', class_='defaultText') \
                    .find_all(re.compile(r'div|p'))

        article_start = False
        article_end = False
        library_start = False
        library_end = False
        new_release_start = False
        new_release_end = False
        upcoming_start = False
        upcoming_end = False

        for item in items:
            if article_start and not article_end:
                # Getting articles.
                self.save_article(item)
            elif library_start and not library_end:
                self.save_library(item)
            elif new_release_start and not new_release_end:
                self.save_new_release(item)
            elif upcoming_start and not upcoming_end:
                self.save_upcoming_events(item)

            text = item.text.strip()
            if re.search(self.ANCHOR_TEXT_TITLE, text):
                self.save_page_title(item)
            elif re.search(self.ANCHOR_TEXT_ARTICLE, text):
                article_start = True
            elif re.search(self.ANCHOR_TEXT_LIBRARY, text):
                article_end = True
                library_start = True
            elif re.search(self.ANCHOR_TEXT_NEW_RELEASES, text):
                library_end = True
                new_release_start = True
            elif re.search(self.ANCHOR_TEXT_UPCOMING_EVENTS, text):
                new_release_end = True
                upcoming_start = True
