


class ConnectionError(Exception):
    '''
    Unable to connect to the api server 
        - wrong internet connection, server is down,...
    '''
    pass



class UnsupportedCurrencyError(Exception):
    '''
    Currency code or symbol is not supported
    '''
    pass
