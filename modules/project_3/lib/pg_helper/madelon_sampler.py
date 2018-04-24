from numpy import random, arange
from pandas import concat, DataFrame
from lib.pg_helper.postgres_tool import PostgresTool


class MadelonSampler(object):
    
    def __init__(self):
        self.pgtool = PostgresTool()
        self.conn_params = {
            'host': '54.200.77.93',
            'port': '5432',
            'user': 'postgres',
            'database' : 'postgres',
            'password': 'postgres'
        }
        self.row_count = 220000
        self.table_list = ['madelon_data_{}'.format(i) for i in range(1,9)]
        self.target = 'madelon_target'
        self.position = 0
    
    
    def connect(self):
        self.pgtool.connect(**self.conn_params)
        return self.pgtool.connected
    
    
    def disconnect(self):
        self.pgtool.close()
        return self.pgtool.connected
    
    
    def get_sample(self, sample_size, random_state=None, drop_cols=None):
        yoda_list = self._gen_yoda_list(sample_size, random_state)
        cols_dict = self._gen_cols_dict(drop_cols) 
        feat_query_list, target_query = self._gen_queries(yoda_list, cols_dict)
        feat_df, target_df = self._get_dataframes(feat_query_list, target_query)
        
        if random_state == None:
            self.position += sample_size
        
        return feat_df, target_df
    
    
    def _get_dataframes(self, feat_query_list, target_query):
        self.connect()
        feat_df_list = [DataFrame(self.pgtool.query(query)).set_index('yoda')
                        for query in feat_query_list]
        target_df = DataFrame(self.pgtool.query(target_query)).set_index('yoda')
        self.disconnect()
        
        return concat(feat_df_list, axis=1), target_df
    
    
    def _gen_yoda_list(self, sample_size, random_state):
        if random_state == None:
            yodas = arange(self.position, self.position + sample_size, step=1)
        else:
            random.seed(random_state)
            yodas = random.randint(0, self.row_count, (sample_size,))
        
        return yodas.astype(str).tolist()
    
    
    def _gen_cols_dict(self, drop_cols):
        if drop_cols == None:
            cols_dict = {table_name: None for table_name in self.table_list}
        else:
            drop_set = {int(col.replace('feat_','')) for col in drop_cols}
            cols_dict = {
                table_name: self._gen_select_list(drop_set, table_index)
                for table_index, table_name in enumerate(self.table_list)
            }
        return cols_dict
    
    
    def _gen_select_list(self, drop_set, table_index):
        select_set = {i for i in range(625 * table_index,
                                       625 * (table_index + 1))} - drop_set
        return ['feat_' + str(col).zfill(4) for col in sorted(list(select_set))]
    
    
    def _gen_queries(self, yoda_list, cols_dict):
        feat_query_list = [self._gen_query(table, yoda_list, cols_dict[table])
                           for table in self.table_list]
        target_query = self._gen_query(self.target, yoda_list)
        
        return feat_query_list, target_query
    
    
    def _gen_query(self, table, yoda_list, cols_list=None):
        if cols_list == None:
            select = '*'
        else:
            select = ','.join(cols_list + ['yoda'])
            
        return """
            SELECT {0}
            FROM {1}
            WHERE {1}.yoda IN ({2});
        """.format(select, table, ','.join(yoda_list))
