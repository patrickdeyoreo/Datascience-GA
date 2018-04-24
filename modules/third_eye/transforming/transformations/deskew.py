from scipy.stats import skew, skewtest
from multiprocessing import Pool


class Deskew(object):
    
    def __init__(self, thresh=0.75, incr=0.05, max_iter=100000):
        """Initialize parameters of the deskew process"""
        self.alphas = list()
        self.thresh = thresh
        self.incr = incr
        self.max_iter = max_iter
    
    

    def fit(self, data):
        """Compute optimal alphas"""
        with Pool() as pool:
            self.alphas = list(pool.map(self.compute_alpha,
                                        [data[col] for col in data]))
        return self.alphas
    
    

    def transform(self, data, columns=None):
        """Return new table with specified columns deskewed"""
        if self.alphas == None:
            raise ValueError("{} object must be fit before transforming"
                             .format(type(self)))
        if columns == None:
            columns = [col for col in data
                       if abs(skew(data[col])) >= self.thresh]

        return [np.log(data[col] + alpha[i])
                if col in columns and alpha[i] != None
                else data[col] for i, col in enumerate(data)]
    
    

    def fit_transform(self, data, columns=None):
        """Compute best alphas and & return transformed data"""
        self.fit(data)
        return self.transform(data, columns)
    
    

    def compute_alpha(self, column):
        """Find the best alpha attainable with the given parameters"""
        lower = -1 * column.min()
        pval_prev = 0.0
        pval = skewtest(np.log(column + lower + self.incr)).pvalue
        i = 1
        
        while i <= self.max_iter and pval > pval_prev:
            i += 1
            pval_prev = pval
            pval = skewtest(np.log(column + lower + i * self.incr)).pvalue

        if pval_prev > skewtest(column).pvalue: 
            return lower + (i - 1) * self.incr
        return None
