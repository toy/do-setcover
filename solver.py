#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import glob
import time
import hashlib
from subprocess import Popen, PIPE

def input_problem_name(input_data):
    problem_size = '-'.join(re.split('\s+', input_data.splitlines()[0].strip()))
    problem_hash = hashlib.sha1(input_data).hexdigest()[:4]
    return problem_size + '(' + problem_hash + ')'

def solve_it(input_data):
    process = Popen(os.getenv('SOLVER', './solver'), stdin=PIPE, stdout=PIPE, shell=True)
    result = process.communicate(input=input_data)[0].strip()
    if process.returncode != 0:
        print result
        sys.exit(process.returncode)

    if result:
        directory = 'solutions'
        if not os.path.exists(directory):
            os.makedirs(directory)

        problem_name = input_problem_name(input_data)
        if result in [file(solution).read() for solution in glob.glob(directory + '/' + problem_name + '*')]:
            print '\033[33mSolution already in «' +  directory + '»!\033[0m'
        else:
            result_value = '%.2f' % float(re.split('\s+', result, 1)[0])
            current_time = time.strftime('%Y%m%d-%H%M%S')
            file_name = problem_name + '=' + result_value + '[' + current_time + ']'

            f = file(directory + '/' + file_name, 'w')
            f.write(result)
            f.close

    return result


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print 'Solving:', file_location
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)'

