import pickle
import json

f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/sql_eval/classical_test.pkl','rb')
data = pickle.load(f)
f.close()
gold_dicts = [d for d in data if d['db_path'] == 'database/{db_id}/{db_id}.sqlite'.format(db_id='geography')]

orig_dataset = json.load(open('/Users/chenbowen/Documents/PaperCode/text2sql-data/data/%s.json' % 'geography'))

f_train = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.train', 'w')
f_dev = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.dev', 'w')
f_test = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.test', 'r')
test = []
test.extend(f_test.readlines())
f_test.close()
count = 0
for data in gold_dicts:
    if data['text']+' ||| ' +data['query']+'\n' in test:
        count += 1
    else:
        print(data['text'])


train = []
dev = []
test = []
for data in orig_dataset:
    # if data['query-split'] == 'train':
    #     for sub_data in data['sentences']:
    #         for sql in data['sql']:
    #             f_train.write(sub_data['text']+ ' ||| '+sql)
    #             f_train.write('\n')
    # elif data['query-split'] == 'dev':
    #     for sub_data in data['sentences']:
    #         for sql in data['sql']:
    #             f_dev.write(sub_data['text']+ ' ||| '+sql)
    #             f_dev.write('\n')
    if data['query-split'] == 'test':
        for sub_data in data['sentences']:
            try:
                test.append(sub_data['text'].replace(list(sub_data['variables'].keys())[0], list(sub_data['variables'].values())[0]))
            except IndexError:
                test.append(sub_data['text'])
f_train.close()
f_dev.close()
for data in gold_dicts:
    f_test.write()