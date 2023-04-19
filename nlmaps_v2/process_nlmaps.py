def detok(query):
    tok = query.replace('(',' ( ').replace(')',' ) ').replace("'"," ' ").replace(',',' , ')
    tok = tok.replace('  ', ' ')
    tok = tok.rstrip()
    tok = tok.lstrip()
    return tok
for name in ['train', 'dev', 'test']:
    f = open('nlmaps_v2/split_1_train_dev_test/nlmaps.v2.'+name+'.en')
    src = f.readlines()
    f = open('nlmaps_v2/split_1_train_dev_test/nlmaps.v2.'+name+'.mrl')
    tgt = f.readlines()
    src_write = open('nlmaps_v2/nlmaps_v2_processed/'+name+'_src.txt', 'w')
    tgt_write = open('nlmaps_v2/nlmaps_v2_processed/'+name+'_tgt.txt', 'w')
    for src_example, tgt_example in zip(src, tgt):
        query = src_example
        program = tgt_example
        program = detok(program)
        src_write.write(query)
        tgt_write.write(program)
        tgt_write.write('\n')
    src_write.close()
    tgt_write.close()

