import json
import random

f_train = open('ATIS/raw/train.json', 'r')
atis_train = json.load(f_train)['rasa_nlu_data']['common_examples']
f_train.close()
f_test = open('ATIS/raw/test.json', 'r')
atis_test = json.load(f_test)['rasa_nlu_data']['common_examples']
f_test.close()
atis_valid = random.sample(atis_train, int(len(atis_train) * 0.2))
replace_atis_train = []
for sample in atis_train:
    if sample not in atis_valid:
        replace_atis_train.append(sample)
atis_train = replace_atis_train

for type, parsed_json in zip(['train', 'valid', 'test'], [atis_train, atis_valid, atis_test]):
    data = parsed_json
    f_write_src = open('ATIS/ATIS_processed/'+type+'_src.txt', 'w')
    f_write_tgt = open('ATIS/ATIS_processed/'+type+'_tgt.txt', 'w')
    for example in data:
        utterance = example['text']
        slot_value_list = example['entities']
        tgt_string = ''
        for slot_value_pair in slot_value_list:
            slot = slot_value_pair['entity']
            value = slot_value_pair['value']
            tgt_string = tgt_string + slot + ':  '+ value +' ; '
        if tgt_string != '':
            f_write_src.write(utterance)
            f_write_src.write('\n')
            f_write_tgt.write(tgt_string)
            f_write_tgt.write('\n')
    f_write_src.close()
    f_write_tgt.close()




