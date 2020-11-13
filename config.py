class Config:
    accounts = [
        {'name':'admin', 'passwd':'admin'}
    ]

try:
    from local_config import Config
except:
    ...
