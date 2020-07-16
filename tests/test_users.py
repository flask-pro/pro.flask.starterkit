def test_users__crud(fx_app):
    print('\n--> test_users__crud')
    new_user = {'username': 'test_user'}

    r_create = fx_app.post('/users', json=new_user)
    assert r_create.status_code == 201
    assert 'id' in r_create.json
    assert r_create.json['username'] == new_user['username']

    r_get = fx_app.get(f'/users/{r_create.json["id"]}')
    assert r_get.status_code == 200
    assert r_get.json['id'] == r_create.json['id']
    assert r_get.json['username'] == r_create.json['username']

    updated_user = {'id': r_create.json["id"], 'username': 'updated_test_user'}
    r_update = fx_app.put(f'/users/{r_create.json["id"]}', json=updated_user)
    assert r_update.status_code == 200
    assert r_update.json['id'] == r_create.json['id']
    assert r_update.json['username'] == updated_user['username']

    r_delete = fx_app.delete(f'/users/{r_create.json["id"]}')
    assert r_delete.status_code == 204
    assert not r_delete.json
