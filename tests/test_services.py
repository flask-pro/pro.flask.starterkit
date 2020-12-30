from tests.config import TestConfig

MAIN_URL = TestConfig.MAIN_URL


def test_check(fx_app) -> None:
    r = fx_app.get(f"{MAIN_URL}check")
    assert r.status_code == 200


def test_collapse(fx_app) -> None:
    r = fx_app.get(f"{MAIN_URL}collapse")
    assert r.status_code == 500


def test_metrics(fx_app) -> None:
    r = fx_app.get(f"{MAIN_URL}metrics")
    assert r.status_code == 200
    assert "python_gc_objects_collected_total" in r.data.decode()


def test_CORS(fx_app) -> None:
    r = fx_app.get(f"{MAIN_URL}check")
    assert r.status_code == 200
    for header in [
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
        "Access-Control-Expose-Headers",
        "Content-Security-Policy-Report-Only",
    ]:
        assert header in r.headers
