from pandas import DataFrame, read_pickle, concat
import warnings
import sys


def suppress_warnings():
    warnings.filterwarnings('ignore')

    
    
def get_usage(globals_dict, dir_list):
    ipython_vars = ['In', 'Out', 'exit', 'quit',
                    'get_ipython', 'ipython_vars']
    return sorted([(x, sys.getsizeof(globals_dict.get(x)) / 1024)
                   for x in dir_list if not x.startswith('_')
                   and x not in sys.modules
                   and x not in ipython_vars],
                  key=lambda x: x[1], reverse=True)
    
    
def mem_usage(globals_dict, dir_list, display_thresh=1):
    total = 0
    convert = lambda b: (b / 1024, 'M') if b >= 1024 else (b, 'K')
    print('{:24} | {:9}'.format('Object', 'Memory Use'))
    print('-' * 25 + ' ' + '-' * 14)
    for obj in get_usage(globals_dict, dir_list):
        if obj[1] >= display_thresh:
            print('{:24} : {:<9.5} {}iB'.format(obj[0], *convert(obj[1])))
        total += obj[1]
    print('-' * 25 + ' ' + '-' * 14)
    print('{:24} | {:<9.5} {}iB'.format('Total', *convert(total)))
    
    
def time_format(s):
        s = int(s)
        h = s // 3600 
        m = s // 60
        return "{}:{}:{}".format(str(h // 10) + str(h % 10),
                                 str(m % 60 // 10 % 6) + str(m % 10),
                                 str(s % 60 // 10) + str(s % 10))
    
    
def load_sample_seq(start_index, n_files, filepath_format):
    samples = DataFrame()
    for i in range(start_index, start_index + n_files):
        try:
            sample = read_pickle(filepath_format.format(i))
        except:
            return samples
        else:
            samples = concat([samples, sample])
    return samples


def make_groups(list_to_group, group_size, order_inner=True):
    list_size = len(list_to_group)
    n_groups = list_size // group_size
    if order_inner:
        return list(zip(*[[list_to_group[j % list_size]
                           for j in range(i, i + list_size,
                                          list_size // n_groups)]
                          for i in range(group_size)]))
    else:
        return list(zip(*[list_to_group[i * n_groups : (i + 1) * n_groups]
                          for i in range(group_size)]))


