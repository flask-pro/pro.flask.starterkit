def test_index(init_app):
    """
    Tests endpoint '/'.
    """
    with init_app.test_client() as tc:
        get_index = tc.get('/')
        assert '<p>This is simple Flask starterkit by https://flask.pro!</p>' in get_index.get_data().decode()