for name in ['train','dev','test']:
    f = open('ATIS_SQL_Version/raw/atis.'+name,'r')
    data = f.readlines()
    f.close()
    src_write = open('ATIS_SQL_Version/atis_src_'+name+'.txt','w')
    tgt_write = open('ATIS_SQL_Version/atis_tgt_'+name+'.txt','w')
    for example in data:
       src, tgt = example.split('|||')
       src_write.write(src.lstrip().rstrip())
       src_write.write('\n')
       tgt_write.write(tgt.lstrip().rstrip())
       tgt_write.write('\n')
    src_write.close()
    tgt_write.close()
