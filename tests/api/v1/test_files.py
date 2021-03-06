import os

import pytest

from tests.config import TestConfig

BASE_DIR = TestConfig.BASE_DIR
FILES_BASE_DIR = TestConfig.FILES_BASE_DIR
FILES_URL = TestConfig.FILES_URL
CDN_SECRET = TestConfig.CDN_SECRET

IMAGE_JPG = os.path.join(BASE_DIR, "content", "floppy.jpg")
TEST_TXT = os.path.join(BASE_DIR, "content", "non_image_file.txt")


@pytest.mark.parametrize("file_path", [IMAGE_JPG, TEST_TXT])
def test_files_crud(fx_app, fx_auth_admin, file_path):
    # Upload file.
    r_post = fx_app.post(
        FILES_URL,
        headers={
            "Content-Type": "multipart/form-data",
            "Authorization": fx_auth_admin["Authorization"],
        },
        data={"file": open(file_path, "rb")},
    )
    assert r_post.status_code == 201
    assert r_post.json
    for key in ["id", "length", "mime_type", "url"]:
        assert key in r_post.json
    assert r_post.json["length"] > 0

    # Get file.
    r_get = fx_app.get(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json
    for key in ["id", "length", "mime_type", "url", "thumbnail"]:
        assert key in r_get.json
    assert r_get.json["length"] > 0

    # Download file.
    r_get = fx_app.get(f'{FILES_URL}/download/{r_post.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.data
    assert isinstance(r_get.data, bytes)

    # Download thumbnail
    r_get = fx_app.get(f'{FILES_URL}/download/{r_post.json["id"]}/thumbnail', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.data

    # Delete file.
    r_del = fx_app.delete(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin)
    assert r_del.status_code == 204
    assert fx_app.get(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin).status_code == 404
    assert (
        fx_app.get(f'{FILES_URL}/download/{r_post.json["id"]}', headers=fx_auth_admin).status_code
        == 404
    )

    assert os.path.isfile(file_path)


@pytest.mark.parametrize("content", [None, b""])
def test_files_empty_file(fx_app, fx_auth_admin, content):
    # Upload file.
    r_post = fx_app.post(
        FILES_URL,
        headers={
            "Content-Type": "multipart/form-data",
            "Authorization": fx_auth_admin["Authorization"],
        },
        data={"file": content},
    )

    assert r_post.status_code == 422


def test_files_cdn_secret(fx_app, fx_test_file):
    r_get = fx_app.get(fx_test_file["url"], headers={"X-CDN-Secret": CDN_SECRET})
    assert r_get.status_code == 200
    assert r_get.data
    assert isinstance(r_get.data, bytes)


def test_files_thumbnail_cdn_secret(fx_app, fx_test_file):
    r_get = fx_app.get(fx_test_file["thumbnail"], headers={"X-CDN-Secret": CDN_SECRET})
    assert r_get.status_code == 200
    assert r_get.data
    assert isinstance(r_get.data, bytes)


def test_files_bad_cdn_secret(fx_app, fx_test_file):
    r = fx_app.get(fx_test_file["url"], headers={"X-CDN-Secret": "BAD_CDN_Secret"})
    assert r.status_code == 401


def test_files_non_cdn_secret(fx_app, fx_test_file):
    r = fx_app.get(fx_test_file["url"])
    assert r.status_code == 401
