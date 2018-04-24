from numpy import ravel
from numpy.random import randint
from pandas import DataFrame
from sklearn.feature_selection import f_classif
from lib.pg_helper import MadelonSampler


def find_pval(feat, tar):
    anova = f_classif(feat, ravel(tar))
    feat_anova_df = DataFrame([{'f_stat': f, 'p_val': p}
                               for f, p in zip(anova[0], anova[1])])
    return feat_anova_df['p_val']


def randsample_anova_avg_pvals(sample_size=4400, n_samples=11):
    ms = MadelonSampler()
    feat_anova_res = DataFrame()
    
    for i in range(n_samples):
        print('*', end='')
        feat, tar = ms.get_sample(sample_size, random_state=randint(101092))
        feat_anova_res['test_{}'.format(i)] = find_pval(feat, tar)
    print()
    return feat_anova_res.T.mean().sort_values(ascending=False)
