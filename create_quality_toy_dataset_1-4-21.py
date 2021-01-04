#!/usr/bin/env python
# coding: utf-8

# ## Create Quality Toy Dataset
# 
# **Author:** Jim Maddock
# 
# **Last Updated:** 1-4-21
# 
# **Description:** Filter article quality scores from entire EN dataset so they fit in memory

import pandas as pd
import csv
import numpy as np
import argparse
import os
import logging
import bz2

def process(infile,outfile,article_list,logger=None):
        rd = csv.reader(infile, delimiter="\t", quotechar='"')
        w = csv.writer(outfile, delimiter=",", quotechar='"')
        j = 0
        for i,row in enumerate(rd):
            if i == 0:
                w.writerow(row)
            else:
                if np.int64(row[0]) in article_list:
                    w.writerow(row)
                    j += 1

            if i % 100000 == 0 and i != 0 and logger:
                logger.debug('processed {0} rows, wrote {1} rows'.format(i,j))
        if logger:
            logger.debug('found {0} of {1} articles'.format(j,len(article_list)))
            
def main():
    parser = argparse.ArgumentParser(description='Create a toy dataset of quality scores based on an article list.')
    parser.add_argument('--quality_scores',
                        required=True,
                        help='a bz2 file of quality scores to process')
    parser.add_argument('--article_list',
                        required=True,
                        help='a csv of articles to include in output')
    parser.add_argument('--outfile',
                        required=True,
                        help='the path of the output csv file')
    parser.add_argument('-v','--verbose',
                        action='store_true',)
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()

    formatter = logging.Formatter(fmt='[%(levelname)s %(asctime)s] %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    article_list = pd.read_csv(args.article_list)['page_id'].values
    logger.info('loaded file {0}'.format(args.article_list))

    with bz2.open(args.quality_scores,'rt') as infile:
        with open(args.outfile,'w') as outfile:
            logger.info('processing file {0}'.format(args.quality_scores))
            process(infile=infile,
                    outfile=outfile,
                    article_list=article_list,
                    logger=logger)
            logger.info('wrote file {0}'.format(args.outfile))
    
if __name__ == "__main__":
    main()

