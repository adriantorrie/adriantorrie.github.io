from collections import OrderedDict
import json
import os
import pandas as pd
import requests as r
import xml.etree.cElementTree as etree

class Client():
    # class variables
    _web_service = 'http://ws.eoddata.com/data.asmx'
    _namespace ='http://ws.eoddata.com/Data'
    
    def __init__(self, username=None, password=None):
        # instance variables
        self._session = r.Session()
        self._token = self._get_token(username, password)
        self._exchange_codes = self._get_exchange_codes()
        
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        self._session.close()
        
    def _web_call(self, call, kwargs, pattern=None):
        url = '/'.join((self._web_service, call))
        response = self._session.get(url, params=kwargs, stream=True)

        if response.status_code == 200:
            if pattern==None:
                return etree.parse(response.raw).getroot()
            else:
                root = etree.parse(response.raw).getroot()
                elements = root.findall(pattern % (self._namespace))
                items = [element.items() for element in elements]
                
                temp = []
                for item in items:
                    temp.append(OrderedDict(item))
                
                return pd.DataFrame(temp)
    
    def _get_token(self, username=None, password=None):
        # get credentials from file if none are passed in
        if username == None and password == None:
            credentials_file_path = os.path.join(os.path.expanduser('~'), '.eoddata', 'credentials')
            
            # test permissions are 0600 (ONLY user can read/write)
            if (os.path.exists(credentials_file_path) and
                oct(os.stat(credentials_file_path).st_mode)[-3:] == '600'):
                try:
                    with open(credentials_file_path) as f:    
                        credentials = json.load(f)
                        username = credentials['username']
                        password = credentials['password']
                finally:
                    del credentials
        
        # login to return token 
        try:
            call = 'Login'
            kwargs = {'Username': username, 'Password': password}
        finally:
            del username
            del password

        root = self._web_call(call, kwargs)
        return root.get('Token')
    
    def _get_exchange_codes(self):
        return list(self.get_exchange_list()['Code'])

    # -------------------------------------------------------------------------
    # external functions for accessing fields
    def close_session(self):
        self._session.close()
        
    def get_session(self):
        return self._session
    
    def get_web_service(self):
        return self._web_service
        
    def get_namespace(self):
        return self._namespace
            
    def get_token(self):
        return self._token
    
    def get_exchange_codes(self):
        return self._exchange_codes
      
    # -------------------------------------------------------------------------
    # external functions for the client
    def get_exchange_list(self):
        call = 'ExchangeList'
        kwargs = {'Token': self._token,}
        pattern = ".//{%s}EXCHANGE"
        
        return self._web_call(call, kwargs, pattern)
