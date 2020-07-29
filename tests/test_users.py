import pytest


def test_users__crud(fx_app, fx_auth_admin):
    print('\n--> test_users__crud')
    new_user = {'username': 'test_crud_user', 'password': 'test_password', 'role': 'user'}

    r_create = fx_app.post('/v1/users', headers=fx_auth_admin, json=new_user)
    assert r_create.status_code == 201
    assert 'id' in r_create.json
    assert r_create.json['username'] == new_user['username']

    r_get = fx_app.get(f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_get.status_code == 200
    assert r_get.json['id'] == r_create.json['id']
    assert r_get.json['username'] == r_create.json['username']

    updated_user = {'id': r_create.json["id"], 'username': 'updated_test_user'}
    r_update = fx_app.put(f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin,
                          json=updated_user)
    assert r_update.status_code == 200
    assert r_update.json['id'] == r_create.json['id']
    assert r_update.json['username'] == updated_user['username']

    r_delete = fx_app.delete(f'/v1/users/{r_create.json["id"]}', headers=fx_auth_admin)
    assert r_delete.status_code == 204
    assert not r_delete.data


@pytest.mark.parametrize('page', [1, None])
@pytest.mark.parametrize('per_page', [1, None])
@pytest.mark.parametrize('include_metadata', [True, None])
def test_users__list(fx_app, fx_auth_admin, page, per_page, include_metadata):
    print('\n--> test_users__list')

    query_string = {}
    if page:
        query_string['page'] = page
    if per_page:
        query_string['per_page'] = per_page
    if include_metadata:
        query_string['include_metadata'] = include_metadata

    r_get = fx_app.get('/v1/users', headers=fx_auth_admin, query_string=query_string)
    assert r_get.status_code == 200
    assert r_get.json
    assert r_get.json['items']
    if include_metadata:
        assert r_get.json['_metadata']


@pytest.mark.parametrize('page', ['BAD_VALUE', None])
@pytest.mark.parametrize('per_page', ['BAD_VALUE', None])
@pytest.mark.parametrize('include_metadata', ['BAD_VALUE', None])
def test_users__list__error_400(fx_app, fx_auth_admin, page, per_page, include_metadata):
    print('\n--> test_users__list__error_400')

    query_string = {}
    if page:
        query_string['page'] = page
    if per_page:
        query_string['per_page'] = per_page
    if include_metadata:
        query_string['include_metadata'] = include_metadata

    r_get = fx_app.get('/v1/users', headers=fx_auth_admin, query_string=query_string)
    if page or per_page or include_metadata:
        assert r_get.status_code == 400
    else:
        assert True


def test_users__bad_id(fx_app, fx_auth_admin):
    print('\n--> test_users__bad_id')

    r_get = fx_app.get('/v1/users/1234567890', headers=fx_auth_admin)
    assert r_get.status_code == 404

    updated_user = {'id': 1234567890, 'username': 'updated_test_user'}
    r_update = fx_app.put('/v1/users/1234567890', headers=fx_auth_admin, json=updated_user)
    assert r_update.status_code == 404

    r_delete = fx_app.delete('/v1/users/1234567890', headers=fx_auth_admin)
    assert r_delete.status_code == 404
