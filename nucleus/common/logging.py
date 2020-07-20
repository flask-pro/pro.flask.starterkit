logging_configuration = {
    'version': 1,
    'formatters': {
        'default': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s'
        },
        'long_formatter': {
            'class': 'logging.Formatter',
            'format': '%(levelname)s | %(module)s:%(funcName)s:%(lineno)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'long_formatter',
        }
    },
    'loggers': {
        'nucleus': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'connexion': {
            'handlers': ['console']
        },
    }
}
