#########################################################################
# File Name: run.sh
# Author: Weiang
# mail: weiang@mail.ustc.edu.cn
# Created Time: 2015年03月13日 星期五 23时34分25秒
#########################################################################

#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <train data> <test data dir>"
	exit -1
fi

TRAIN_DATA=$1
TEST_DATA_DIR=$2
python="/usr/bin/python"
gen_dict_script="./gen_weibo_dict.py"
gen_libsvm_script="./gen_libsvm_data.py"
train_predict_script="./tools/easy.py"

$python ./parse_json_weibo.py $TEST_DATA_DIR ./data/user.txt
$python ./gen_test_weibo.py ./data/user.txt ./data/weibo.txt

$python $gen_dict_script $TRAIN_DATA

$python $gen_libsvm_script $TRAIN_DATA "${TRAIN_DATA}.libsvm"
$python $gen_libsvm_script "./data/weibo.txt" "./data/weibo.txt.libsvm"

$python $train_predict_script "${TRAIN_DATA}.libsvm" "./data/weibo.txt.libsvm"

$python ./gen_adv_users.py ./data/user.txt ./data/weibo.txt ./weibo.txt.libsvm.predict
