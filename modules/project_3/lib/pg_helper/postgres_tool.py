import psycopg2 as pg2
from psycopg2.extensions import connection as pgconn_t
from psycopg2.extras import RealDictCursor as pgcurs_t


class pgConnCurs(object):

    def __init__(self, connect=False, **params):
        self._conn = None
        self._curs = None
        if connect == True:
            self.connect(**params)


    def __setattr__(self, name, value):
        if name == '_conn':
            try:
                self._conn.close()
            except AttributeError:
                pass
        super().__setattr__(name, value)
 

    def __delattr__(self, name):
        if name == '_conn':
            try:
                self._conn.close()
            except AttributeError:
                pass
        super().__delattr__(name)


    @property
    def connected(self):
        return self._conn != None and self._conn.closed != 0

    
    def connect(self, **params):
        if self._conn != None and self._conn.closed == 0:
            raise RuntimeError("Existing connection still open!")
        try:
            self._conn = pg2.connect(**params)
            self._curs = self._conn.cursor(cursor_factory=pgcurs_t)
        except:
            self.close()
            raise


    def close(self):
        self._curs = None
        self._conn = None


    def query(self, query):
        self._curs.execute(query)
        return self._curs.fetchall()




class PostgresTool(object):

    def __init__(self, connect=False, **params):
        self._pgcc = pgConnCurs(connect, **params)
    
    
    @property
    def connected(self):
        return self._pgcc.connected
    
    
    def connect(self, **params):
        self._pgcc.connect(**params)
    
    
    def close(self):
        self._pgcc.close()
    
    
    def query(self, queries):
        buffer = []
        return buffer if len(self._query(queries, buffer)) > 1 else buffer[0]
    
    
    def _query(self, queries, buffer):
        if type(queries) == list:
            for q in queries:
                self._query(q, buffer)
        elif type(queries) == str:
            buffer.append(self._pgcc.query(queries))
        else:
            raise TypeError("'queries' expects a string or a nested list of strings.")
        return buffer
