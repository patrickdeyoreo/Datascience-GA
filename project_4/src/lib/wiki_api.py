from redis import StrictRedis
import requests
import json


def tasty_str(*values):
    return {
        0: values,
        1: values[0]
    }.get(len(values),'|'.join(values).replace(' ', '+'))

def tasty_param(prop, *values):
    return '='.join([prop, tasty_str(*values)])

def tasty_params(**params):
    return '&'.join([tasty_param(p, params[p]) for p in params])

    

class WikiApi:

    def presets(_action='query', _format='json', _limit='max', **_presets):
        presets = { 'action': _action, 'format': _format,
                    **{ p[1:]: _presets[p] for p in _presets } }
        def request(request_func):
            def execute(self, *args, **params):
                self._query = self._api + tasty_params(**presets)
                return request_func(self, *args, **params)
            return execute
        return request

    
    
    def __init__(self, redis_host, api='http://en.wikipedia.org/w/api.php?',
                 subcat_key_format='subcats_{}', page_key_format='pages_{}',
                 **redis_params):
        '''
        Initialize with the address of the API, a redis connection,
            redis key format strings for subcategory and page lists,
            and a variable to store queries.
        '''
        self._api = api
        self._query = None
        self._redis = StrictRedis(redis_host, **redis_params)
        self._subcat_key_format = subcat_key_format
        self._page_key_format = page_key_format
        

        
    @presets(_list='categorymembers', _cmtype='page')
    def pages(self, category, subcat_depth=0, **params):
        '''
        Submits request to Wikipedia for category information
        -- Parameters --
        category: Name of the to category to get pages from
        params: Any additional key-value pairs for the API request
        Returns API response in JSON format
        '''
        return self._query_category(category, self._page_key_format,**params)
        
       
        
    
    @presets(_list='categorymembers', _cmtype='subcat')
    def subcategories(self, category, subcat_depth=0, **params):
        '''
        Submits request to Wikipedia for category information
        -- Parameters --
        category: Name of the to category to get page list from
        subcat_depth: Max # of levels of subcategories to get
        params: Any additional key-value pairs for the API request
        Returns API response in JSON format
        '''
        data = self._query_category(category, self._subcat_key_format, **params)
        if subcat_depth > 0:
            for subcat in data:
                data += self.subcategories(subcat['title'], subcat_depth - 1, **params)
        return data
        

        
    @presets(_prop='revision', _rvprop='content')
    def content(self, ref_type='titles', *refs, **params):
        '''
        Submits request to Wikipedia for content of page(s)
        -- Parameters --
        ref_type: Type of page reference - either 'titles' or 'pageids'
        refs: Page title(s) or pageid(s), as strings.
        params: Any additional key-value pairs for the API request
        Returns API response in JSON format
        '''
        if ref_type != 'titles' and ref_type != 'pageids':
            raise ValueError("ref_type must be 'titles' or 'pageids'")
            
        self._query = '&'.join([
            self._query,
            tasty_params(**{ref_type: refs}, **params)
        ])
        return requests.get(self._query).json()
    
    
        
    def _query_category(self, category, key_format, **params):
        '''
        Submits request to Wikipedia and incrementally saves results in redis
        -- Parameters --
        category: Name of the to category to get page list from
        key_format: Redis key format string to format with category
        params: Any additional key-value pairs for the API request
        Returns dictionary of results.
        '''
        category = category.lower()
        self._query = '&'.join([
            self._query,
            tasty_params(cmtitle='Category:{}'.format(category), **params)
        ])

        key = key_format.format(category)
        resp = requests.get(self._query).json()
        data = resp['query']['categorymembers']
        self._redis.set(key, data)
        while 'continue' in resp.keys():
            to_append = '&cmcontinue=' + resp['continue']['cmcontinue']
            resp = requests.get(self._query + to_append).json()
            data += resp['query']['categorymembers']
            self._redis.set(key, json.dumps(data))
            
        return data
