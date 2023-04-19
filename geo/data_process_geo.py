import json

data_type = ['train', 'dev', 'test']
for type in data_type:
    f_read = open('geo/funql/'+type+'.json', 'r')
    f_write_src = open('geo/processed_geo/'+type+'_src.txt', 'w')
    f_write_tgt = open('geo/processed_geo/'+type+'_tgt.txt', 'w')
    for line in f_read.readlines():
        json_data = json.loads(line)
        src = 'question: ' + json_data['question']
        tgt = 'program: ' + json_data['program']
        f_write_src.write(src)
        f_write_src.write('\n')
        f_write_tgt.write(tgt)
        f_write_tgt.write('\n')
    f_read.close()
    f_write_src.close()
    f_write_tgt.close()
