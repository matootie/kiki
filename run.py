import os
from kiki import Kiki

if __name__ == "__main__":
    # Attempt to load the token from environment.
    try:
        token = os.environ["KIKI_TOKEN"]
    except KeyError:
        print("You must specify the bot token under KIKI_TOKEN.")

    # Load the optional Redis URL from environment.
    redis_url = os.environ.get("REDIS_URL")

    # Create and run Kiki.
    kiki = Kiki(redis_url=redis_url)
    kiki.run(token)
