import os

from .config import TestConfig

BASE_DIR = TestConfig.BASE_DIR
FILES_BASE_DIR = TestConfig.FILES_BASE_DIR
FILES_URL = TestConfig.FILES_URL


def test_files_crud(fx_app, fx_auth_admin):
    print("--> test_files_upload:")

    file_path = os.path.join(BASE_DIR, "content", "floppy.jpg")

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
    assert os.path.isfile(os.path.join(FILES_BASE_DIR, str(r_post.json["id"])))

    # Get file.
    r_get = fx_app.get(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin)

    assert r_get.status_code == 200
    assert r_get.json
    for key in ["id", "length", "mime_type", "url"]:
        assert key in r_get.json
    assert r_get.json["length"] > 0 and not None

    # Download file.
    r_get = fx_app.get(r_post.json["url"], headers=fx_auth_admin)

    assert r_get.status_code == 200
    assert isinstance(r_get.data, bytes)
    assert r_get.data

    # Delete file.
    r_del = fx_app.delete(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin)

    assert r_del.status_code == 204

    assert fx_app.get(f'{FILES_URL}/{r_post.json["id"]}', headers=fx_auth_admin).status_code == 404

    assert (
        fx_app.get(f'{FILES_URL}/download/{r_post.json["id"]}', headers=fx_auth_admin).status_code
        == 404
    )

    assert not os.path.isfile(os.path.join(FILES_BASE_DIR, str(r_post.json["id"])))
