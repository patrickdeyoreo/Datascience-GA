#! /usr/bin/python3


from numpy import logspace
from sklearn.linear_model import LogisticRegression
from pandas import DataFrame, to_pickle, read_pickle
from lib import time_format, load_sample_seq, make_groups, ColDrop1SamplesInfo
from time import time
import argparse
import sys


sample_info = ColDrop1SamplesInfo()




arg_parser = argparse.ArgumentParser("Iteratively train a dictionary of " +
                                     "Logistic Regressions indexed by unique " +
                                     "C-values of the form 1eN for -8 < N < 9.")

arg_parser.add_argument('--dict-format', nargs='?', default='assets/lrdict{}.p',
                        help="filename format to index dictionary pickles")
arg_parser.add_argument('--resume', nargs='?',
                        help="index of a dictionary pickle to resume training")
arg_parser.add_argument('--start', nargs='?', default=1, type=int,
                        help="first sample index to train on ({} samples)"
                             .format(sample_info.file_count),
                        choices=list(range(sample_info.file_count + 1)))
arg_parser.add_argument('--end', nargs='?', default=-1, type=int,
                        help="last sample index to train on ({} samples)"
                             .format(sample_info.file_count),
                        choices=list(range(sample_info.file_count + 1)))
arg_parser.add_argument('--samples-per-iter', nargs='?', default=1, type=int,
                        help="# of samples to load each iteration ({} rows " +
                             "per sample)".format(sample_info.sample_size))
args = arg_parser.parse_args()

warn_SpI_conflict = """
***  WARNING: sample range not evenly divisible by # of samples per iter.
            : extraneous sampled will be skipped.\
"""

args_summary = """
 <%>~<%>~<%>~<%>~<%>~<%>  ~++~++ SETTINGS ++~++~  <%>~<%>~<%>~<%>~<%>~<%> 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<@> SAMPLE FILENAME FORMAT ..............................................:
--- >> {}
--------------------------------------------------------------------------
<@> DICTIONARY FILENAME FORMAT ..........................................:
--- >> {}
--------------------------------------------------------------------------
<@> INDEX OF DICTIONARY FILE TO LOAD & RESUME TRAINING ..................:
--- >> {}
--------------------------------------------------------------------------
<@> INDEX OF FIRST SAMPLE TO USE ..................................:
--- >> {}
--------------------------------------------------------------------------
<@> INDEX OF LAST SAMPLE TO USE ...................................:
--- >> {}
--------------------------------------------------------------------------
<@> # OF SAMPLES TO USE IN EACH ITERATION ..............................:
--- >> {} {}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\n""".format(sample_info.p3_filename_template, args.dict_format,
           args.resume, args.start, args.end, args.samples_per_iter,
           '' if (args.end - args.start + 1) % args.samples_per_iter == 0
              else warn_SpI_conflict)

sys.stdout.write(args_summary)

with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
    log.write(args_summary)

del args_summary




sample_index_list = sample_info.index_list(args.start, args.end)
sample_index_groups = make_groups(sample_index_list, args.samples_per_iter)

n_sample_groups = len(sample_index_groups)
n_samples = n_sample_groups * args.samples_per_iter


if args.resume != None:
    logreg_dict = read_pickle(args.dict_format.format(resume))
    C_list = sorted(logreg_dict.keys())
else:
    C_list = logspace(-7, 8, 16)
    logreg_dict = {
        C: LogisticRegression(C=C, penalty='l2', max_iter=1000,
                                      warm_start=True) for C in C_list  
    }
    
    
training_info="""
\n<#> Logistic Regression Iterative Training Info <#>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  * Sample Size .........: {:>4} rows per sample
  * Selected Samples ....: [{:>2}, {:>2}] inclusive
  * % of Samples ........: {:>4.3} % of total samples
  * # of Samples / Iter. : {:>4} samples per iteration
  * # of Iterations .....: {:>4} iterations
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  * Logistic Regression C-values ~
  * >> {}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\n""".format(sample_info.sample_size, args.start,
             args.start + n_samples - 1,
             n_samples / sample_info.file_count,
             args.samples_per_iter, n_sample_groups,
             ', '.join(['{:>4.0E}'.format(C) for C in C_list]))

sys.stdout.write(training_info)

with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
    log.write(training_info)

del training_info




for g, g_num in zip(sample_index_groups, range(1, n_sample_groups + 1)):
    with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
        log.write("\n^^^^^^^^^^^^^^^^^^^^^^^^\n" +
                  "\n~+~ Sample Group {:>02} ~+~\n".format(g_num) +
                  " (Samples {:>02}-{:>02} of {:>02})\n".format(
                      g[0], g[-1], n_samples) +
                  "~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
    data = load_sample_seq(g[0], n_files=args.samples_per_iter,
                           filepath_format=sample_info.p3_filename_template)
    y = data['target']
    data.drop('target', axis=1, inplace=True)
    
    with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
        log.write("\n<{:>02}> Fitting Models...\n".format(g_num) +
                  "~++~~++~~++~~++~~++~~++~\n")
          
    group_timer = time()
    for C, log_reg in sorted(logreg_dict.items()):
        mod_timer = time()
        log_reg.fit(data, y)
        mod_timer = time() - mod_timer
        with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
            log.write("<{:>02}> C = {:>4.0E}\n".format(g_num, C) +
                      "  * > Fit Time: {}\n".format(time_format(mod_timer)) +
                      "........................\n\n")

    group_timer = time() - group_timer
    with open('./log/gen_samples1_trained_lr_dict.log', mode='a') as log:
        log.write("<{:>02}> Group Complete\n".format(g_num) +
                  "  * > Fit Time: {}\n".format(time_format(group_timer)) +
                  "~~~~~~~~~~~~~~~~~~~~~~~~\n\n")

    dict_name = args.dict_format.format(str(args.start) + '-' + str(g[-1]))
    to_pickle(logreg_dict, dict_name)
