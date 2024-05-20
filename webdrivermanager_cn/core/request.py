from requests import Session


class Request(Session):
    __obj = None

    def __new__(cls, *args, **kwargs):
        if not cls.__obj:
            cls.__obj = super().__new__(cls)
        return cls.__obj
