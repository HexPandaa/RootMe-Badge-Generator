# -*- coding: utf-8 -*-
# Author: HexPandaa

from re import findall
from requests import Session
from requests.utils import quote
from time import sleep
from random import randrange


class RootMe:
    """
    A class to retrieve data from the Root-Me website.
    """

    BASE = "https://www.root-me.org/"
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 32

    def __init__(self):
        self.sess = Session()
        self.sess.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
                "Referer": self.BASE
            }
        )

    def get_session(self) -> Session:
        return self.sess

    @staticmethod
    def __check_username(self, username: str) -> bool:
        """
        Checks if the username is valid and does not contains strange characters (like slashes, just in case...).

        :param username: the username to check
        :type username: str
        :return: True if the username seems valid, False otherwise
        :rtype: bool
        """

        # First, we check if the given username is a string
        if not isinstance(username, str):
            return False

        regex = r"^[\w-.]{3,32}$"
        return len(findall(regex, username)) == 1

    def __sanitize_username(self, username: str) -> str:
        """
        Tries to sanitize the username.

        :param username: the username to check
        :type username: str
        :return: The hopefully sanitized username
        :rtype: str
        """

        # First, we check if the given username is a string
        assert isinstance(username, str), "The username must the a `str`"
        # Then we check if the username has a valid length
        assert self.USERNAME_MIN_LENGTH <= len(username) <= self.USERNAME_MAX_LENGTH, \
            f"The username must be between {self.USERNAME_MIN_LENGTH} and {self.USERNAME_MAX_LENGTH} characters long"
        # And finally we return the URL-encoded username, encoding slashes as well
        return quote(username, safe="", encoding="utf-8")

    @staticmethod
    def __is_profile_page(page: str) -> bool:

        # Should I check more thoroughly here?
        return "<title>Profil of " in page[:200]

    def __extract_user_info(self, page: str) -> dict:
        """
        Extract the user's info from the 'info' page
        """

        d = dict()

        # Extracting the user's username (with case)
        regex = r"<meta\s+name=\"author\"\s+content=\"(.*)?\""
        m = findall(regex, page)
        d["username"] = m[0] if len(m) == 1 else ""

        # Extracting the user's profile picture URL
        regex = r"<h1\s+itemprop=\"givenName\">\n<img .*?logo_auteur.*?src=\"(.*?)\""
        m = findall(regex, page)
        d["avatar_url"] = self.BASE + m[0] if len(m) == 1 else ""

        # Extract the 'informations' block so that we reduce our search space
        regex = r"(?s)<h3>informations.*?<\/ul>"
        m = findall(regex, page)
        if len(m) != 1:
            return d
        infos = m[0].replace("&nbsp;", " ")  # Replacing &nbsp; html entities with spaces as it will be easier to match

        # The model is as follow:
        # dict_key: (regex, default_value)
        regexes = {
            "lang": (r"<li>Lang.*?alt=\"(\w+)", ""),
            "status": (r"<li>Status\s*:\s*(.*)(?=<\/li>)", ""),
            "score": (r"<li>Score.*?<span>(\d+)(?=<\/span>)", 0),
            "posts": (r"<li>Posts.*?<span>(\d+)(?=<\/span>)", 0),
            "chatbox": (r"<li>ChatBox\s*:\s*(.*)(?=<\/li>)", 0)
        }

        for key, (regex, default) in regexes.items():
            m = findall(regex, infos)
            d[key] = m[0] if len(m) == 1 else default

        return d

    @staticmethod
    def __extract_user_score(page: str) -> dict:
        """
        Extract the user's info from the 'score' page
        """

        d = dict()

        # Extracting the ratio of completed challenges
        regex = r"(?s)<b .*?>Challenges :</b>.*?<span.*?(\d+)/(\d+)"
        m = findall(regex, page)
        d["challenges_completed"], d["challenges_total"] = m[0] if len(m) == 1 else (0, 0)

        # Extracting the ranking of the user
        regex = r"(?s)<b [\w=\"]*?>Place :</b>.*?<span.*?(\d+)<span.*?/(\d+)<\/"
        m = findall(regex, page)
        d["ranking"], d["total_users"] = m[0] if len(m) == 1 else (0, 0)

        # Extracting the user's rank
        regex = r"(?s)<b [\w=\"]*?>Rank :</b>\s*<span.*?>\s*(\w+)"
        m = findall(regex, page)
        d["rank"] = m[0] if len(m) == 1 else ""

        #Extracting the user's score
        regex = r"(?s)<b [\w=\"]*?>Challenges :</b>.*?<span.*?(\d+)&nbsp;Points"
        m = findall(regex, page)
        d["score"] = m[0] if len(m) == 1 else ""

        return d

    def get_user_stats(self, username: str) -> dict:
        """
        Returns a dict representing a user.

        :param username: the username of the user
        :type username: str
        :return:
        """

        infos = dict()

        try:
            user = self.__sanitize_username(username)
        except AssertionError as e:
            raise ValueError(str(e))

        url = f"{self.BASE}/{user}?lang=en&inc={{page}}"

        funcs = {
            "info": self.__extract_user_info,
            "score": self.__extract_user_score
        }

        for page, func in funcs.items():
            response = self.sess.get(url.format(page=page))

            if response.status_code != 200:
                raise UserNotFoundError("This user does not exist")

            if not self.__is_profile_page(response.text):
                continue

            infos.update(func(response.text))
            sleep(randrange(3, 16) / 10)

        return infos


class UserNotFoundError(Exception):
    pass


if __name__ == '__main__':
    from pprint import pprint
    rm = RootMe()
    data = rm.get_user_stats("HexPandaa")
    pprint(data)
