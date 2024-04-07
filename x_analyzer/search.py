"""Post picker that specific keyword is included."""

import argparse
import os
import pandas as pd
from twikit import Client

ATTRIBUTE = ["id", "created_at_datetime", "user", "text", "favorite_count",
             "retweet_count", "quote_count", "hashtags"]

def pick(user_name, email, password, word="ポートフォリオ", tab="Top",) -> pd.DataFrame:
    """Search module.

    Search posts with specific word.

    Args:
        user_name (str): your account name
        email (str): your email of account
        password (str): your password of account 
        word (str): keyword to search posts
        tab  (str): place of tab. default 'Top' 

    Returns:
        pandas.DataFrame: picked posts with id, created_at_datetime, user, text
                          favorite_count, retweet_count, quote_count, hashtags
    """
    client = Client('ja')
    if not os.path.isfile('cookies.json'):
        client.login(
            auth_info_1=user_name,
            auth_info_2=email,
            password=password
        )
        client.save_cookies(os.path.join(os.getcwd(), "cookies.json"))
    else:
        client.load_cookies(os.path.join(os.getcwd(), "cookies.json"))

    res = client.search_tweet(word, tab)

    df_dict = {k:list() for k in ATTRIBUTE}
    for post in res:
        for attr in ATTRIBUTE:
            df_dict[attr].append(getattr(post, attr))
    
    return pd.DataFrame.from_dict(df_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('u', help="user_name of account")
    parser.add_argument('e', help="email of account")
    parser.add_argument('p', help="password of account")
    parser.add_argument('w', help="keyword to search posts", default="ポートフォリオ")

    args = parser.parse_args()
    pick(args.u, args.e, args.p, args.w)