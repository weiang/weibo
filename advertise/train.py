#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from weibo_text import *
from svmutil import *

def train(y, x, param):
    prob = svm_problem(y, x)
    m = svm_train(prob, param)

    
