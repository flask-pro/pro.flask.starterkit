import time

from tests.config import TestConfig

FILES_URL = TestConfig.FILES_URL
ARTICLES_URL = TestConfig.ARTICLES_URL
SEARCH_URL = TestConfig.SEARCH_URL


def test_articles__crud(
    fx_app, fx_auth_admin, fx_test_file_non_deleted, fx_comparing_keys_values
) -> None:
    new_article_data = {
        "title": "test_article_title",
        "announce": "test_article_announce",
        "content": "test_article_content",
        "main_picture_id": fx_test_file_non_deleted()["id"],
        "main_video_id": fx_test_file_non_deleted()["id"],
        "author": "test_article_author",
        "author_picture_id": fx_test_file_non_deleted()["id"],
        "global_name": "test_article_global_name",
    }

    new_article = fx_app.post(ARTICLES_URL, headers=fx_auth_admin, json=new_article_data)
    assert new_article.status_code == 201
    assert "id" in new_article.json
    fx_comparing_keys_values(
        new_article_data,
        new_article.json,
        exclude_keys=["main_picture_id", "main_video_id", "author_picture_id"],
    )
    assert new_article.json["main_picture"]["id"] == new_article_data["main_picture_id"]
    assert new_article.json["main_video"]["id"] == new_article_data["main_video_id"]
    assert new_article.json["author_picture"]["id"] == new_article_data["author_picture_id"]
    assert new_article.json["datetime_created"]

    article = fx_app.get(f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin)
    assert article.status_code == 200
    assert article.json["id"] == new_article.json["id"]
    fx_comparing_keys_values(
        new_article_data,
        article.json,
        exclude_keys=["main_picture_id", "main_video_id", "author_picture_id"],
    )
    assert article.json["main_picture"]["id"] == new_article_data["main_picture_id"]
    assert article.json["main_video"]["id"] == new_article_data["main_video_id"]
    assert article.json["author_picture"]["id"] == new_article_data["author_picture_id"]
    assert new_article.json["datetime_created"]

    updated_article_data = {
        "id": new_article.json["id"],
        "title": "test_updated_article_title",
        "announce": "test_updated_article_announce",
        "content": "test_updated_article_content",
        "main_picture_id": fx_test_file_non_deleted()["id"],
        "main_video_id": fx_test_file_non_deleted()["id"],
        "author": "test_updated_article_author",
        "author_picture_id": fx_test_file_non_deleted()["id"],
        "global_name": "test_updated_article_global_name",
    }
    updated_article = fx_app.put(
        f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin, json=updated_article_data
    )
    assert updated_article.status_code == 200
    fx_comparing_keys_values(
        updated_article_data,
        updated_article.json,
        exclude_keys=["main_picture_id", "main_video_id", "author_picture_id"],
    )
    assert updated_article.json["main_picture"]["id"] == updated_article_data["main_picture_id"]
    assert updated_article.json["main_video"]["id"] == updated_article_data["main_video_id"]
    assert updated_article.json["author_picture"]["id"] == updated_article_data["author_picture_id"]
    assert updated_article.json["datetime_created"]

    deleted_article = fx_app.delete(
        f'{ARTICLES_URL}/{new_article.json["id"]}', headers=fx_auth_admin
    )
    assert deleted_article.status_code == 204
    assert not deleted_article.data
    for file_id in [
        updated_article.json["main_picture"]["id"],
        updated_article.json["main_video"]["id"],
        updated_article.json["author_picture"]["id"],
    ]:
        assert fx_app.get(f"{FILES_URL}/{file_id}", headers=fx_auth_admin).status_code == 404
        assert (
            fx_app.get(f"{FILES_URL}/download/{file_id}", headers=fx_auth_admin).status_code == 404
        )


def test_articles__filter(fx_app, fx_auth_admin, fx_test_article) -> None:
    result_filter_by_author = fx_app.get(
        ARTICLES_URL, headers=fx_auth_admin, query_string={"author": fx_test_article["author"]}
    )
    assert result_filter_by_author.status_code == 200
    assert len(result_filter_by_author.json["items"]) == 1


def test_articles__search(fx_app, fx_auth_admin, fx_test_article) -> None:
    # Нужно дождаться пока индекс инициализируется.
    time.sleep(1)

    search_result = fx_app.get(
        f"{SEARCH_URL}", query_string={"scope": "articles", "q": "article"}, headers=fx_auth_admin
    )
    assert search_result.status_code == 200
    assert search_result.json
    assert len(search_result.json["items"]) == 1
    assert search_result.json["items"][0]["id"]
    assert search_result.json["items"][0]["title"] == fx_test_article["title"]
