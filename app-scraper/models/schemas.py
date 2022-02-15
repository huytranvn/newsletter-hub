from dataclasses import dataclass


@dataclass
class Source:
    name: str
    display_name: str


@dataclass
class Link:
    text: str
    url: str


@dataclass
class Category:
    name: str


@dataclass
class Column:
    # This is the entity for each news in an Issue.
    title: str
    link: Link
    description: str
    tags: list
    category: Category


@dataclass
class Issue:
    source: Source
    number: int
    columns: list[Column]
