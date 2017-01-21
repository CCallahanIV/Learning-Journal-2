"""This module configures a twitter API object to be used to send tweets."""

import twitter
import os


def include_me():
    """Create a twitter api object for use in tweeting posts."""
    twitter_api = twitter.Api(
        consumer_key=os.environ.get("TWITTER_CONSUMER_KEY", None),
        consumer_secret=os.environ.get("TWITTER_SECRET", None),
        access_token_key=os.environ.get("TWITTER_ACCESS_TOKEN", None),
        access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", None)
    )
