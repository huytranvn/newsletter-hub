import os
import re

from typing import Optional
from urllib.request import urlopen

from bs4 import BeautifulSoup

from models.schemas import (
    Issue,
    Source,
    Link,
    Category,
    Column,
)

from utils.scraper import Scraper


class PythonWeekly:
    # Homepage: https://www.pythonweekly.com/
    ANCHOR_TEXT_TITLE = '^Welcome\sto\sissue\s[0-9]{1,3}\sof\sPython\sWeekly'
    ANCHOR_TEXT_ARTICLE = 'Articles,\sTutorials\sand\sTalks'
    ANCHOR_TEXT_LIBRARY = 'Interesting\sProjects,\sTools\sand\sLibraries'

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
        self.category_article = Category(
            name='article',
        )

        # Scrape the page.
        scraper = Scraper(
            url=self.PAGE_URL.format(issue_number),
            page_name=self.PAGE_NAME.format(issue_number),
        )

        # Init flags.
        self.column = None

        # Scrape the webpage.
        scraper.scrape()

        # Parse content.
        self.parse_content()

    def get_file_path(self):
        return os.path.join(
            'archived',
            f'python_weekly_{self.issue.number}.html',
        )

    def save_page_title(self, item: BeautifulSoup) -> None:
        pass

    def save_article(self, item: BeautifulSoup) -> None:
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
                category=self.category_article,
                description=None,
                tags=[],
            )
        elif self.column:
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
                    .find_all('div')

        article_start = False
        article_end = False
        library_start = False
        library_end = False

        for item in items:
            if article_start and not article_end:
                # Getting articles.
                self.save_article(item)

            text = item.text.strip()
            if re.search(self.ANCHOR_TEXT_TITLE, text):
                self.save_page_title(item)
            elif re.search(self.ANCHOR_TEXT_ARTICLE, text):
                article_start = True
            elif re.search(self.ANCHOR_TEXT_LIBRARY, text):
                article_end = True
