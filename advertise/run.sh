#########################################################################
# File Name: run.sh
# Author: Weiang
# mail: weiang@mail.ustc.edu.cn
# Created Time: 2015年03月13日 星期五 23时34分25秒
#########################################################################

#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <train data> <test data>"
	exit -1
fi

TRAIN_DATA=$1
TEST_DATA=$2
python="/usr/bin/python"
gen_dict_script="./gen_weibo_dict.py"
gen_libsvm_script="./gen_libsvm_data.py"
train_predict_script="./tools/easy.py"

$python $gen_dict_script $TRAIN_DATA

$python $gen_libsvm_script $TRAIN_DATA "${TRAIN_DATA}.libsvm"
$python $gen_libsvm_script $TEST_DATA "${TEST_DATA}.libsvm"

$python $train_predict_script "${TRAIN_DATA}.libsvm" "${TEST_DATA}.libsvm"

