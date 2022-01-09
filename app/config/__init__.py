import os

class Config:
    ENV = os.environ.get("ENV")

    SESSION_TYPE = 'redis'

    EXTRASENSORY_COUNT = 30
    MIN_RANGE_HIDDEN_NUMBER = 10
    MAX_RANGE_HIDDEN_NUMBER = 99

    SECRET_KEY = 'R2dS*4Wqe#Q2%7mgW{seP7R?'
