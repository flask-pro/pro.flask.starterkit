def test_hello(init_app):
    """
    Tests cli command 'about'.
    """
    runner = init_app.test_cli_runner()
    result = runner.invoke(args=['about'])
    assert 'This is template "flask_simple"!' in result.output
