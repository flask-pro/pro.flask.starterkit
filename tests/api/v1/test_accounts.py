from tests.config import TestConfig

ACCOUNTS_URL = TestConfig.ACCOUNTS_URL


def test_accounts__crud(fx_app, fx_auth_admin) -> None:

    r_profile = fx_app.get(f"{ACCOUNTS_URL}/profile", headers=fx_auth_admin)
    assert r_profile.status_code == 200
    assert r_profile.json
