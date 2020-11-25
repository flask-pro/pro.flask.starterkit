from nucleus.controllers.directories import Directory


def get_directories() -> dict:
    return Directory.get_directories()
