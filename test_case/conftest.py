import logging
import os


def pytest_sessionstart(session):
    os.environ['WDM_LOG'] = 'true'
    os.environ['WDM_LOG_LEVEL'] = f'{logging.DEBUG}'
