def test_index(fx_app):
    print('\n--> test_index')
    r = fx_app.get('/')
    assert r.status_code == 200


def test_check(fx_app):
    print('\n--> test_check')
    r = fx_app.get('/check')
    assert r.status_code == 200
