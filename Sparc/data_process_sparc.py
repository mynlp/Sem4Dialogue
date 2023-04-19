import json

for name in ['train', 'dev']:
    f = open('sparc/raw/'+name+'.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    src_write = open('sparc/processed_sparc/'+name+'_src.txt', 'w', encoding='utf-8')
    tgt_write = open('sparc/processed_sparc/'+name+'_tgt.txt', 'w', encoding='utf-8')
    for example in data:
        utterance = ''
        for inter_example in example['interaction']:
            sql = inter_example['query'].replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace('  ', ' ')
            tgt_write.write(sql)
            tgt_write.write('\n')
            utterance = utterance + ' ' + ' '.join(inter_example['utterance_toks'])
            src_write.write(utterance.lstrip())
            src_write.write('\n')
        sql = example['final']['query']
        tgt_write.write(sql.replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').replace('  ', ' '))
        tgt_write.write('\n')
        utterance = utterance + ' ' + example['final']['utterance']
        src_write.write(utterance.lstrip())
        src_write.write('\n')
    src_write.close()
    tgt_write.close()