def test_index(fx_app) -> None:
    print("\n--> test_index")
    r = fx_app.get("/")
    assert r.status_code == 200
    assert "Flask starterkit by https://flask.pro!" in r.data.decode()


def test_check(fx_app) -> None:
    print("\n--> test_check")
    r = fx_app.get("/check")
    assert r.status_code == 200


def test_collapse(fx_app) -> None:
    print("\n--> test_collapse")
    r = fx_app.get("/collapse")
    assert r.status_code == 500
