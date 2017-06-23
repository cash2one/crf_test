#-*- coding: utf-8 -*- 

import sys
import os
import string

if len(sys.argv)<4:
    print("usage: %s temp1 temp2 file_out"%(sys.argv[0]));
    sys.exit(-1);

temp1=sys.argv[1]
temp2=sys.argv[2]
temp3=sys.argv[3]

fp = open(temp1,'r')
lines = fp.readlines()
fp.close();

fp = open(temp2,'r')
lines2 = fp.readlines()
fp.close();

fp = open(temp3,'w');

i = 0;
for ln in lines:
    ln = ln.replace('\r\n','');
    ln = ln.replace('\n','');
    if len(ln) <= 1:
        break;
    i = i+1;
fp.write(str(i)+'\n')

i = 0;
for ln in lines:
    ln = ln.replace('\r\n','');
    ln = ln.replace('\n','');
    if len(ln) <= 1:
        break;
    lp = ln.split();
    ks = lp[1];
    fp.write(ks+'\n');

    ln2 = lines2[i];
    i = i+2;
    ln2 = ln2.replace('\r\n','');
    ln2 = ln2.replace('\n','');

    fp.write(ln2+'\n');

fp.close();



sys.exit(0);


