#coding=utf-8


import os
import sys

## 输入: 分词和词性标注文件 韵律标注文件 
## 输出: ps1.txt ps2.txt pw_train.txt pp_train.txt ip_train.txt
if len(sys.argv)<3:
    print("usage: %s file_wordseg_postag   file_prosody"%(sys.argv[0]));
    print("输入: 分词和词性标注文件 韵律标注文件 ");
    print("输出: ps1.txt ps2.txt pw_train.txt pp_train.txt ip_train.txt");
    sys.exit(-1);


#### step1 
#### 输入:argv1 argv2:      将不符合格式的line 输出到 ps2.txt 中
#### 输出:ps1.txt ps2.txt   符合格式的输出到 ps1.txt 中 
f_segpos = sys.argv[1];
f_prosod = sys.argv[2];

fp = open(f_segpos,'r',-1,'utf-8')
lines_segpos = fp.readlines();
fp.close();

fp = open(f_prosod,'r',-1,'utf-8')
lines_prosod = fp.readlines();
fp.close();

### 两个文件的 行数 必须相同 
len_lines = len(lines_segpos);
if len_lines != len(lines_prosod):
    print("len_segpos != len_prosod");
    sys.exit(-2);

### 符合规则的输出到 ps1.txt 中，不符合的输出到 ps2.txt 中
fp = open('ps1.txt','w',-1,'utf-8')
fp2 = open('ps2.txt','w',-1,'utf-8')

for ii in range(len_lines):
    ln = lines_segpos[ii];
    lp = ln.split();
    k = 0;
    for i in range(len(lp)):
        wd = lp[i];
        if wd.find('/')<0:
            k=1;
    if k == 0:
        fp.write(lines_prosod[ii])
        fp.write(ln);
    else:
        fp2.write(ln)

fp.close();
fp2.close()
            

### step2 
### 输入:ps1.txt:       奇数行是prosody 偶数行是 seg pos  
### 输出:pw_train.txt:  韵律词训练数据  
fp = open('ps1.txt','r',-1,'utf-8')
lines = fp.readlines();
fp.close();

fp = open('pw_train.txt','w');

len_lines = int(len(lines)/2);
for i in range(len_lines):

    # prosody
    ln1 = lines[i*2]; 
    ln1 = ln1.replace('|',' ');
    ln1 = ln1.replace('$',' ');
    ln1 = ln1.replace('  ',' ');
    ln1 = ln1.replace('  ',' ');
    ln1 = ln1.replace(' \n','\n');
    ln1 = ln1.replace('\n','');

    # seg pos  
    ln2 = lines[i*2+1]; 
    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace(' \n','\n');
    ln2 = ln2.replace('\n','');

    lp1 = ln1.split();  ##  姜 还是 老的辣
    lp2 = ln2.split();  ##  姜/nr   还/d  是/v   老/a  的/u  辣/an

    ## 韵律词的id = 0,1,2 表示第几个韵律词 
    id = -1; 
    ## 当前韵律词的长度(剩余的) = 1,2,3  减掉当前词的长度：如果刚好等于0 说明当前词处刚好是韵律词划分 
    rm = 0;  
    ## 距离韵律词首的长度: 几个基础词 当前组合起来的长度 看看够不够一个韵律词的长度 
    dist = 0;

    for j in range(len(lp2)):

        ## 前面刚好划分完韵律词 
        if rm == 0:
            id = id + 1;
            rm = len(lp1[id]);
            dist = 0;

        wdr = lp2[j]; # 姜/nr
        wd = wdr[0 : wdr.find('/')];  # 当前词 
        pos = wdr[wdr.find('/') + 1:]; # 当前词性 

        ### 当前词处  距离 韵律词首 的长度
        dist = dist + len(wd);

        ### 的 u 1 4 1
        ### 当前词 词性 长度 距离韵律词首的长度  此处是否是韵律词划分处
        fp.write(wd + ' ' + pos + ' ' + str(len(wd)) + ' ' + str(dist) + ' ');

        rm = rm - len(wd);
        if rm > 0:
            fp.write('0\n');
        else:
            fp.write('1\n');

    fp.write('\n')

fp.close()





### step3 
### 输入: ps1.txt:       
### 输出: pp_train.txt: 韵律短语 训练数据
        ## 的       u       1   1               4                       0
        ## 当前词  词性  长度  是否是韵律词  距离韵律短语首部的距离  是否是韵律短语
fp = open('ps1.txt','r',-1,'utf-8')
lines = fp.readlines();
fp.close();

len_lines = int(len(lines)/2);
fp = open('pp_train.txt','w');
for i in range(len_lines):
    ln1 = lines[i*2];
    ln3 = ln1;

    ## ln3 韵律短语用|表示  韵律词用空格表示 
    ln3 = ln3.replace('$','|');
    ln3 = ln3.replace('  ',' ');
    ln3 = ln3.replace('  ',' ');
    ln3 = ln3.replace(' \n','\n');
    ln3 = ln3.replace('\n','');

    ln2 = lines[i*2+1];
    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace(' \n','\n');
    ln2 = ln2.replace('\n','');

    ## 韵律短语和韵律词 全用空格表示 
    ln1 = ln3;
    ln1 = ln1.replace('|',' '); 

    ##  韵律词的空格去掉 只保留韵律短语用空格表示 
    ln3 = ln3.replace(' ','');
    ln3 = ln3.replace('|',' ');


    ## 韵律词划分
    lp1 = ln1.split();
    ## 单个词的词性 
    lp2 = ln2.split();
    ## 韵律短语划分 
    lp3 = ln3.split();

    id = -1;
    id2 = -1;
    rm = 0;
    rm2 = 0;
    dist = 0;
    for j in range(len(lp2)):
        if rm == 0:
            id = id + 1;
            ## 韵律词的长度 (剩余的)
            rm = len(lp1[id]);
        if rm2 == 0:
            id2 = id2+1;
            ## 韵律短语的长度 （剩余的）
            rm2 = len(lp3[id2]);
            dist = 0;

        wdr = lp2[j];
        wd = wdr[0:wdr.find('/')];
        pos = wdr[wdr.find('/')+1:];
        dist = dist + len(wd);

        ## 的       u       1   1               4                       0
        ## 当前词  词性  长度  是否是韵律词  距离韵律短语首部的距离  是否是韵律短语
        fp.write(wd + ' ' + pos + ' ' + str(len(wd)) + ' ');

        ##  是否是韵律词
        rm = rm - len(wd);
        if rm > 0:
            fp.write('0 ');
        else:
            fp.write('1 ');

        fp.write(str(dist) + ' ');

        ##  是否是韵律短语
        rm2 = rm2 - len(wd);
        if rm2>0:
            fp.write('0\n');
        else:
            fp.write('1\n');

    fp.write('\n')

fp.close();



### step4 
### 输入: ps1.txt:       
### 输出: ip_train.txt: 韵律短语 训练数据
        ## 的       u       1   1               7                       0
        ## 当前词  词性  长度  是否是韵律词  距离语调短语首部的距离  是否是语调短语

fp = open('ps1.txt','r',-1,'utf-8')
lines = fp.readlines();
len_lines = int(len(lines)/2);
fp.close();

fp = open('ip_train.txt','w');
for i in range(len_lines):
    ln1 = lines[i*2];
    ln2 = lines[i*2+1];

    ## 韵律短语的|变成空格  用|表示语调短语
    ln3 = ln1;
    ln3 = ln3.replace('|',' ');
    ln3 = ln3.replace('$','|');
    ln3 = ln3.replace('  ',' ');
    ln3 = ln3.replace('  ',' ');
    ln3 = ln3.replace(' \n','\n');
    ln3 = ln3.replace('\n','');

    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace('  ',' ');
    ln2 = ln2.replace(' \n','\n');
    ln2 = ln2.replace('\n','');

    ## 韵律词
    ln1 = ln3;
    ln1 = ln1.replace('|',' ');

    ## 语调短语 
    ln3 = ln3.replace(' ','');
    ln3 = ln3.replace('|',' ');

    ## 韵律词划分
    lp1 = ln1.split();
    ## 单个词的词性 
    lp2 = ln2.split();
    ## 韵律短语划分 
    lp3 = ln3.split();

    id=-1;
    id2=-1;
    rm = 0;
    rm2 = 0;
    dist = 0;
    for j in range(len(lp2)):

        if rm == 0:
            id = id+1;
            rm = len(lp1[id]);

        if rm2 == 0:
            id2 = id2+1;
            rm2 = len(lp3[id2]);
            dist = 0;

        wdr = lp2[j];
        wd = wdr[0:wdr.find('/')];
        pos = wdr[wdr.find('/')+1:];

        dist = dist + len(wd);

        fp.write(wd+' '+pos+' '+str(len(wd))+' ');
        rm = rm - len(wd);
        rm2 = rm2 - len(wd);

        if rm>0:
            fp.write('0 ');
        else:
            fp.write('1 ');

        fp.write(str(dist)+' ');

        if rm2>0:
            fp.write('0\n');
        else:
            fp.write('1\n');

    fp.write('\n')

fp.close();




sys.exit(0);
