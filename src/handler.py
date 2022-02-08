"""
Lambda function to publish dev.to articles.
"""
import json
import os

import requests

def get_unpublished_articles(api_key):
    """
    Returns the unpublished articles for the api keys user.
    """

    url = "https://dev.to/api/articles/me/unpublished"

    response = requests.get(
        url,
        headers={"api-key": api_key},
        params={"page": 1, "per_page": 10_000}
    )

    return response.json()

def filter_list_of_articles(list_of_articles):
    """
    Reduces the amount of attributes in a list of articles.
    """

    keep_keys = ["id", "title", "published", "published_at", "path", "url"]

    return [
        {key: article[key] for key in keep_keys}
         for article in list_of_articles
    ]

def get_filtered_list_of_unpublished_articles(api_key):
    """
    Returns a list of unpublished articles with limited attributes.
    """

    list_of_articles = get_unpublished_articles(api_key=api_key)

    return filter_list_of_articles(list_of_articles)

def get_article_id_by_preview_url(preview_url, api_key):
    """
    Returns the article id for a given preview_url.
    """

    for article in get_filtered_list_of_unpublished_articles(api_key):

        # Preview URLs have a weird suffix, it is what it is...
        if article["url"] in preview_url:
            return article["id"]

    return None

def publish_article_by_id(article_id, api_key):
    """
    Publish an article given its id and api_key
    """

    url = f"https://dev.to/api/articles/{article_id}"

    print(f"Publishing article {article_id}")

    response = requests.put(
        url=url,
        json={
            "article": {
                "published": True
            }
        },
        headers={
            "api-key": api_key
        }
    )

    assert response.json()["published_at"] is not None

def lambda_handler(api_event, __unused):
    """
    Handles incoming requests from the API Gateway.
    """

    payload = json.loads(api_event["body"])

    assert "PostURL" in payload, "PostURL needs to be present"
    assert "ApiKey" in payload, "ApiKey needs to be present"

    post_url = payload["PostURL"]
    api_key = payload["ApiKey"]

    print(f"Got PostURL {post_url}")
    # We don't want to show the whole API key that wouldn't be great.
    print(f"Got API Key {api_key[0]}{ '*' * (len(api_key) - 2)}{api_key[-1]}")

    article_id = get_article_id_by_preview_url(
        preview_url=post_url,
        api_key=api_key
    )

    if article_id is not None:
        publish_article_by_id(article_id=article_id, api_key=api_key)

    return {}

def test():
    """Tests the lambda using the sample event"""
    path_to_sample_event = os.path.join(os.path.dirname(__file__), "sample_event.json")
    with open(path_to_sample_event, encoding="utf-8") as file_handle:
        file_content = file_handle.read()

    event = json.loads(file_content)

    lambda_handler(event, {})

if __name__ == "__main__":

    test()
