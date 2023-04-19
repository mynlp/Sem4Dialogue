import json

for name in ['train', 'dev']:
    f = open('Spider/'+name+'_spider.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    src_write = open('Spider/processed_spider/'+name+'_src.txt', 'w', encoding='utf-8')
    tgt_write = open('Spider/processed_spider/'+name+'_tgt.txt', 'w', encoding='utf-8')
    for example in data:
        sql_query_toks = example['query_toks']
        question_toks = example['question_toks']
        sql_query = ' '.join(sql_query_toks)
        question = ' '.join(question_toks)
        src_write.write(question)
        src_write.write('\n')
        tgt_write.write(sql_query)
        tgt_write.write('\n')
    src_write.close()
    tgt_write.close()

