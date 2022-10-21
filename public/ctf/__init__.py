import json

def save_accounts(theaccounts):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            # Store account state
            _data = {}
            for _a in theaccounts:
                _data[str(_a)] = _a.nonce
            open('.state', 'w').write(json.dumps(_data))
            return result
        return wrapper
    return decorator

def restrict_accounts(restricted=[]):
    def decorator(function):
        def wrapper(*args, **kwargs):
            _data = json.loads(open('.state', 'r').read())
            for _account in restricted:
                _old_nonce = _data.get(_account, 0)
                if _account.nonce > _old_nonce:
                    return False, 'Restricted accounts usage: {}'.format(_account)
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator