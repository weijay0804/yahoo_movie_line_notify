"""
Author: weijay
Date: 2023-01-26 14:46:21
LastEditors: weijay
LastEditTime: 2023-01-26 21:51:14
Description: 取得 yahoo 電影
"""

import re
from typing import Tuple, Union, List

import bs4

from .helper import RequestHelper, Bs4Helper


class Movie:
    def __init__(
        self,
        poster_link: str,
        title_ch: str,
        title_en: str,
        rate: float,
        want_watch: int,
        release_date: str,
        info_text: str,
        movie_link: str,
    ):
        """初始化

        Args:
            poster_link (str): 電影海報連結
            title_ch (str): 中文電影標題
            title_en (str): 英文電影標題
            rate (float): 評分
            want_watch (str): 想看的比例
            release_date (str): 上映日期
            info_text (str): 電影說明
            movie_link (str): 電影詳細頁面連結
        """

        self.poster_link = poster_link
        self.title_ch = title_ch
        self.title_en = title_en
        self.rate = rate if rate is not None else "無"
        self.want_watch = str(want_watch) + "%" if want_watch is not None else "無"
        self.release_date = release_date
        self.info_text = info_text
        self.movie_link = movie_link

    def __repr__(self) -> str:

        return f"{self.title_ch}"


class YahooMovie:
    def __init__(self, url: str, page: int):
        """init

        Args:
            url (str): Yahoo 電影頁面 url (不包含 ? 後的參數)
            page (int): 想要爬取的頁面數量
        """

        self.url = url
        self.page = page

    def _get_html_soup(self, url) -> bs4.BeautifulSoup:
        """取得電影頁面 HTML

        Returns:
            bs4.BeautifulSoup: BeautifulSoup 實例
        """

        response = RequestHelper.get(url)

        soup = Bs4Helper.parse_html(response.text)

        return soup

    def run(self) -> List[Movie]:
        """爬取電影頁面

        Returns:
            List[Movie]: 每個電影都實例化成一個 Movie 類別，並用 list 存起來
        """

        r = []

        for i in range(1, self.page + 1):

            url = f"{self.url}?page={i}"

            soup = self._get_html_soup(url)

            li_tag = soup.find("ul", class_="release_list").find_all("li")

            if li_tag == []:
                break

            for li in li_tag:

                movie_tag = MovieTag(li)

                title_tuple = movie_tag.get_title()

                movie = Movie(
                    movie_tag.get_poster_link(),
                    title_tuple[0],
                    title_tuple[1],
                    movie_tag.get_rate(),
                    movie_tag.get_want_to_watch(),
                    movie_tag.get_release_date(),
                    movie_tag.get_info_text(),
                    movie_tag.get_info_link(),
                )

                r.append(movie)

        return r


class MovieTag:
    def __init__(self, li: bs4.element.Tag):

        self._li = li
        self._info_black = self._get_info_black()
        self._title_info_black = self._get_title_black()

    def _get_info_black(self) -> bs4.element.Tag:
        """取得電影資訊區塊 tag

        Returns:
            bs4.element.Tag: 電影資訊 div tag
        """

        return self._li.find("div", class_="release_info")

    def _get_title_black(self) -> bs4.element.Tag:
        """取得電影標題區塊 tag

        Returns:
            bs4.element.Tag: 電影標題 div tag
        """

        return self._info_black.find("div", class_="release_movie_name")

    def get_poster_link(self) -> str:
        """取得電影海報超連結

        Returns:
            str: 海報超連結
        """

        return self._li.find("img", class_="lazy-load").get("data-src")

    def get_title(self) -> Tuple[str]:
        """取得電影標題

        Returns:
            str: 電影標題，回傳為 tuple，其中第一個是`中文標題`，第二個為`英文標題`
        """

        title = (
            m.text.replace("\n", "").replace(" ", "")
            for m in self._title_info_black.find_all("a")
        )

        return tuple(title)

    def get_info_link(self) -> str:
        """取得電影詳細頁面連結

        Returns:
            str: 頁面超連結
        """

        return self._title_info_black.find("a").get("href")

    def get_rate(self) -> Union[float, None]:
        """取得電影評分

        Returns:
            Union[float, None]: 評分，如果沒有則為 None
        """

        rate_black = self._title_info_black.find("dl", class_="levelbox")

        rate = rate_black.find("dd")

        if rate is not None:

            rate = rate.find("div", class_="leveltext").find("span").get("data-num")
            rate = float(rate)

        return rate

    def get_want_to_watch(self) -> Union[int, None]:
        """取得想看的比例

        Returns:
            Union[str, None]: 想看的比例，如果沒有則為 None
        """

        rate_black = self._title_info_black.find("dl", class_="levelbox")

        want_to_watch = rate_black.find("dt")

        if want_to_watch is not None:
            want_to_watch = (
                want_to_watch.find("div", class_="leveltext").find("span").text
            )
            want_to_watch = want_to_watch.replace("%", "")
            want_to_watch = int(want_to_watch)

        return want_to_watch

    def get_release_date(self) -> str:
        """取得上映日期

        Returns:
            str: 上映日期 (YYYY-MM-DD)
        """

        release_time = self._info_black.find("div", class_="release_movie_time").text
        m = re.search(r"\d+-\d+-\d+", release_time)

        return m.group(0)

    def get_info_text(self) -> str:
        """取得電影說明

        Returns:
            str: 電影說明
        """

        info_text = (
            self._info_black.find("div", class_="release_text").find("span").text
        )

        return info_text.replace("\n", "").replace("\r", "").replace(" ", "")
