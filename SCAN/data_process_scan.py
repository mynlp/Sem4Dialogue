import json

data_type = 'train'
for data_type in ['train', 'test']:
    f_read = open('SCAN/length_split/tasks_'+data_type+'_length.txt', 'r')
    f_write_src = open('SCAN/processed_length_split/tasks_'+data_type+'_length_src.txt', 'w')
    f_write_tgt = open('SCAN/processed_length_split/tasks_'+data_type+'_length_tgt.txt', 'w')
    for line in f_read.readlines():
        src, tgt = line.split('OUT')
        src = src.rstrip()
        tgt = 'OUT'+tgt
        f_write_src.write(src)
        f_write_src.write('\n')
        f_write_tgt.write(tgt)
        #f_write_tgt.write('\n')
    f_read.close()
    f_write_src.close()
    f_write_tgt.close()






