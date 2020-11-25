from tests.config import TestConfig

DIRECTORIES_URL = TestConfig.DIRECTORIES_URL


def test_directories(fx_app, fx_auth_admin, fx_test_article) -> None:
    print("\n--> test_directories")

    directories = fx_app.get(DIRECTORIES_URL, headers=fx_auth_admin)
    assert directories.status_code == 200
    assert directories.json["articles"][fx_test_article["global_name"]]
