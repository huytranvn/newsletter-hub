import os

from typing import Optional
from urllib.request import urlopen


class Scraper:
    def __init__(self, url: str, page_name: str):
        self.url = url
        self.page_name = page_name

    def scrape(self) -> Optional[str]:
        try:
            saved_path = os.path.join(
                'archived',
                self.page_name,
            )

            # Check if file is already existed.
            if os.path.isfile(saved_path):
                print(f'{self.page_name} is already existed!')
                return saved_path

            # Go get the page content.
            response = urlopen(self.url)
            content = response.read()

            # Save content to file.
            with open(saved_path, 'wb') as f:
                f.write(content)

            return saved_path
        except Exception as ex:
            print(ex)
