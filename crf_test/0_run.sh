#!/bin/sh  

#LD_LIBRARY_PATH=/home/szm/tts/tools_install/hts-2.1v/CRF++-0.58/:$LD_LIBRARY_PATH  
#export LD_LIBRARY_PATH
python=python3.2

mkdir -p tmp
mkdir -p model
mkdir -p test

## 1 数据准备
## 输入: 分词和词性标注文件 韵律标注文件 
## 输出: ps1.txt ps2.txt pw_train.txt pp_train.txt ip_train.txt
$python 1_data_pro.py train_corpus_tagged.txt  train_corpus.txt
if [ $? != 0 ];then
    echo "ERROR:data_pro.py failed!"
    exit 0;
fi
echo "LOG:data_pro.py completed!"

### 2 训练model
crf_learn -c 4.0 -f 5 -t template/template_pw pw_train.txt model_pw
crf_learn -c 4.0 -f 5 -t template/template_pp pp_train.txt model_pp
crf_learn -c 4.0 -f 3 -t template/template_pp ip_train.txt model_ip
echo "LOG:crf_learn completed!"

#rm -rf model_ip model_pw model_pp

## model 拆分 
./2_split_modle.sh model_pw.txt
./2_split_modle.sh model_pp.txt
./2_split_modle.sh model_ip.txt
echo "LOG:2_split_modle.sh completed!"

$python 3_postprocess.py model_pw.txt.temp1 model_pw.txt.temp2 model_pw.txt.final
$python 3_postprocess.py model_pp.txt.temp1 model_pp.txt.temp2 model_pp.txt.final
$python 3_postprocess.py model_ip.txt.temp1 model_ip.txt.temp2 model_ip.txt.final
echo "LOG:3_postprocess.py completed!"




### 3 测试部分 
#### pw 韵律词 
test_pw=out_test.pw.v0.txt
eval_pw=out_test.pw.v0.prob.txt
crf_test -m model_pw pw_train.txt   > ${test_pw} 
###crf_test -v1 -m model_pw pw_train.txt   > ${out_v1} 
awk '\

    BEGIN{FS="\t"; total=0; ok_num=0;}

    {
        if(NF>5){
            total=total+1;
            if($5 != $6){
                ok_num=ok_num+1;
                print $0
            }
        }
    }

    END{
        printf "total_num=%d\n",total;
        printf "ok_num=%d\n",ok_num;
        printf "准确率=%4f\n",1-ok_num/total;
    }

    '   ${test_pw}  >  ${eval_pw} 


#### pp 韵律短语 
test_pp=out_test.pp.v0.txt
eval_pp=out_test.pp.v0.prob.txt
crf_test -m model_pp pp_train.txt   > ${test_pp} 
awk '\

    BEGIN{FS="\t"; total=0; ok_num=0;}

    {
        if(NF>5){
            total=total+1;
            if($6 != $7){
                ok_num=ok_num+1;
                print $0
            }
        }
    }

    END{
        printf "total_num=%d\n",total;
        printf "ok_num=%d\n",ok_num;
        printf "准确率=%4f\n",1-ok_num/total;
    }

    '   ${test_pp}  >  ${eval_pp} 


## ip 语调短语
test_ip=out_test.ip.v0.txt
eval_ip=out_test.ip.v0.prob.txt
crf_test -m model_ip ip_train.txt   > ${test_ip} 
awk '\

    BEGIN{FS="\t"; total=0; ok_num=0;}

    {
        if(NF>5){
            total=total+1;
            if($6 != $7){
                ok_num=ok_num+1;
                print $0
            }
        }
    }

    END{
        printf "total_num=%d\n",total;
        printf "ok_num=%d\n",ok_num;
        printf "准确率=%4f\n",1-ok_num/total;
    }

    '   ${test_ip}  >  ${eval_ip} 




mv ps1.txt ps2.txt pw_train.txt pp_train.txt ip_train.txt *.temp1 *.temp2 tmp
mv model_pw* model_pp* model_ip*  model
mv out_test* test

echo "LOG:$0 completed!"





