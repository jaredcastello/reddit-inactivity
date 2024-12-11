""" 
Script to find inactive subreddits
"""

import argparse
import webbrowser
from datetime import datetime, timezone
from string import Template
from typing import Tuple
from urllib.error import HTTPError
import toml
from dateutil.relativedelta import relativedelta as rdelta
from praw import Reddit
from praw.models.reddit.subreddit import Subreddit

URL = Template("https://www.reddit.com/$sub/")


class SubredditInactivity:
    """Checks if followed subreddits have been inactive"""

    delta: datetime
    reddit: Reddit
    browser: bool
    results: dict

    def __init__(self, threshold: int, browser: bool = False):
        print(f"Finding subreddits inactive for more than {threshold} months")
        self.delta = (datetime.now(timezone.utc) - rdelta(months=threshold)).timestamp()
        self.reddit = self._init_praw()
        self.browser = browser
        self.subs = list(self.reddit.user.subreddits(limit=1000))
        self.results = {}

    def _init_praw(self) -> Reddit:
        """Initializes the praw session"""
        config = toml.load("./pyproject.toml")["reddit"]["config"]
        return Reddit(**config)

    def _get_posts(self, subreddit: Subreddit) -> Tuple[str, str]:
        """Returns most recent posts for the subreddit"""
        if subreddit.display_name[0:2] == "u_":
            name = subreddit.display_name.split("u_", 1)[-1]
            posts = self.reddit.redditor(name).submissions.new(limit=5)
            url = URL.substitute(sub=f"user/{name}")
        else:
            posts = subreddit.new(limit=5)
            url = URL.substitute(sub=f"r/{subreddit.display_name}")

        return posts, url

    def _ts_to_strftime(self, timestamp: int) -> str:
        """Converts the timestamp to a formatted date string"""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

    def print(self):
        """prints results"""
        for result in self.results.values():
            if result["error"]:
                message = f"Error: {result['error']}"
            else:
                message = f"Last Post: {result['date']}"

            print(f"{result['url']} | {message}")

    def open_browser(self):
        """prints results"""
        for result in self.results.values():
            webbrowser.open(result["url"], new=2, autoraise=False)

    def execute(self):
        """Execute the script"""
        for subreddit in self.subs:
            try:
                posts, url = self._get_posts(subreddit)
                dates = sorted([post.created_utc for post in posts])

                if not dates or dates[-1] < self.delta:
                    self.results[subreddit.display_name] = {
                        "url": url,
                        "date": self._ts_to_strftime(dates[-1]) if dates else None,
                        "error": None,
                    }

            except HTTPError as e:
                self.results[subreddit.display_name] = {
                    "url": url,
                    "date": None,
                    "error": e,
                }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="reddit-inactivity app")
    parser.add_argument("inactivity", help="Filter by # of months inactive")
    parser.add_argument(
        "-b",
        "--browser",
        action="store_true",
        help="Launch result in browser",
    )

    args = parser.parse_args()
    activity = SubredditInactivity(int(args.inactivity), args.browser)
    activity.execute()
    activity.print()

    if args.browser:
        activity.open_browser()
