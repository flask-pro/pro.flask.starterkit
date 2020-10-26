from tests.config import TestConfig

MAIN_URL = TestConfig.MAIN_URL


def test_index(fx_app) -> None:
    print("\n--> test_index")
    r = fx_app.get(MAIN_URL)
    assert r.status_code == 200
    assert "Flask starterkit by https://flask.pro!" in r.data.decode()


def test_check(fx_app) -> None:
    print("\n--> test_check")
    r = fx_app.get(f"{MAIN_URL}check")
    assert r.status_code == 200


def test_collapse(fx_app) -> None:
    print("\n--> test_collapse")
    r = fx_app.get(f"{MAIN_URL}collapse")
    assert r.status_code == 500
