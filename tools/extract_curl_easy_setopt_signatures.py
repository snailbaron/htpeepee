#!/usr/bin/env python3

import argparse
import dataclasses
import html.parser
import re
import urllib.parse
import urllib.request
from typing import override


@dataclasses.dataclass
class OptionInfo:
    name: str
    url: str

    def __str__(self) -> str:
        return f"{self.name}: {self.url}"


class EasySetoptParser(html.parser.HTMLParser):
    def __init__(self, url: str) -> None:
        super().__init__()

        self._url = url
        self._inside_options = False
        self._inside_one_option: str | None = None

        self.options: list[OptionInfo] = []

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a" and attrs == [("name", "OPTIONS")]:
            self._inside_options = True
            return

        if tag == "a" and attrs == [("name", "PROTOCOLS")]:
            self._inside_options = False
            return

        if not self._inside_options:
            return

        attr_dict = dict(attrs)
        href = attr_dict.get("href")
        if tag == "a" and href:
            name = href.removeprefix("./").removesuffix(".html")
            url = urllib.parse.urljoin(self._url, attr_dict["href"])
            self.options.append(OptionInfo(name=name, url=url))


class OptionParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()

        self._inside_synopsis = False
        self._inside_pre = False
        self.signature = ""

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a" and attrs == [("name", "SYNOPSIS")]:
            self._inside_synopsis = True
            return

        if tag == "a" and attrs == [("name", "DESCRIPTION")]:
            self._inside_synopsis = False
            return

        if not self._inside_synopsis:
            return

        if tag == "pre":
            self._inside_pre = True

    @override
    def handle_endtag(self, tag: str) -> None:
        if self._inside_synopsis and tag == "pre":
            self._inside_pre = False

        self.signature = re.sub(r"^.*CURLcode", "CURLcode", self.signature)
        self.signature = self.signature.strip()
        self.signature = re.subn(r"\s+", " ", self.signature)[0]

    @override
    def handle_data(self, data: str) -> None:
        if self._inside_pre:
            self.signature += data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="https://curl.se/libcurl/c/curl_easy_setopt.html",
        help="URL to curl_easy_setopt documentation page",
    )
    args = parser.parse_args()

    easy_setopt_parser = EasySetoptParser(args.url)
    with urllib.request.urlopen(args.url) as f:
        easy_setopt_parser.feed(f.read().decode("utf-8"))

    for option in easy_setopt_parser.options:
        option_parser = OptionParser()
        with urllib.request.urlopen(option.url) as f:
            option_parser.feed(f.read().decode("utf-8"))

        print(option_parser.signature, flush=True)


if __name__ == "__main__":
    main()
