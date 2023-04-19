import json
import os
data_subdir_devtrain = os.listdir('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_traindev/data')
data_subdir_test = os.listdir('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_test/data')

f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_traindev/scripts/config/dstc2_dev.flist','r')
dev_list = f.readlines()
f.close()

f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_traindev/scripts/config/dstc2_train.flist','r')
train_list = f.readlines()
f.close()

f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_test/scripts/config/dstc2_test.flist','r')
test_list = f.readlines()
f.close()

# data_dir = os.listdir('DST2&3/dstc2_traindev/data/'+data_subdir[0])
# f = open('DST2&3/dstc2_traindev/data/'+data_subdir[0]+'/'+data_dir[0]+'/label.json', 'r')
# data_address = data_subdir[0]+'/'+data_dir[0]
# example = json.load(f)
# f.close()

train_src_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/train_src.txt', 'w')
train_tgt_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/train_tgt.txt', 'w')
dev_src_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/dev_src.txt', 'w')
dev_tgt_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/dev_tgt.txt', 'w')
test_src_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/test_src.txt', 'w')
test_tgt_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/processed_dst/test_tgt.txt', 'w')
for data_upper_dir in data_subdir_devtrain:
    if data_upper_dir == '.DS_Store':
        continue
    for data_lower_dir in os.listdir('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_traindev/data/'+data_upper_dir):
        if data_lower_dir == '.DS_Store':
            continue
        f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_traindev/data/' + data_upper_dir + '/' + data_lower_dir + '/label.json', 'r')
        example = json.load(f)
        f.close()
        data_address = data_upper_dir + '/' + data_lower_dir
        for turn in example['turns']:
            text = turn['transcription']
            semantics = turn['semantics']['cam'].replace('(',' ( ').replace(')',' ) ').replace('=',' = ').replace('|',' | ').replace('  ',' ')
            src = text + ' ; '+ semantics
            goal = turn['goal-labels']
            method = turn['method-label']
            requested_slot = turn['requested-slots']
            goal_text = 'goal : { '
            for idx, key in enumerate(list(goal.keys())):
                if (len(goal.keys())>1) & (idx<(len(goal.keys())-1)):
                    goal_text = goal_text + key +' = '+goal[key] + ' , '
                elif len(goal.keys())==1:
                    goal_text = goal_text + key +' = '+goal[key]
                else:
                    goal_text = goal_text + key +' = '+goal[key]
            goal_text = goal_text + ' } ; '
            request_text = 'requested_slots : { '
            for idx,value in enumerate(requested_slot):
                if (len(requested_slot)>1) & (idx<(len(requested_slot)-1)):
                    request_text = request_text + value + ' , '
                elif len(requested_slot)==1:
                    request_text = request_text + value
                else:
                    request_text = request_text + value
            request_text = request_text + ' } , '
            method_text = 'method : '+method
            combine = goal_text + request_text + method_text
            combine = combine.replace('  ',' ')
            if data_address+'\n' in dev_list:
                dev_src_write.write(src)
                dev_src_write.write('\n')
                dev_tgt_write.write(combine)
                dev_tgt_write.write('\n')
            elif data_address+'\n' in train_list:
                train_src_write.write(src)
                train_src_write.write('\n')
                train_tgt_write.write(combine)
                train_tgt_write.write('\n')
for data_upper_dir in data_subdir_test:
    if data_upper_dir == '.DS_Store':
        continue
    for data_lower_dir in os.listdir('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_test/data/'+data_upper_dir):
        if data_lower_dir == '.DS_Store':
            continue
        f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/DST2&3/dstc2_test/data/' + data_upper_dir + '/' + data_lower_dir + '/label.json', 'r')
        example = json.load(f)
        f.close()
        data_address = data_upper_dir + '/' + data_lower_dir
        for turn in example['turns']:
            text = turn['transcription']
            semantics = turn['semantics']['cam'].replace('(',' ( ').replace(')',' ) ').replace('=',' = ').replace('|',' | ').replace('  ',' ')
            src = text + ' ; ' + semantics
            goal = turn['goal-labels']
            method = turn['method-label']
            requested_slot = turn['requested-slots']
            goal_text = 'goal : { '
            for idx, key in enumerate(list(goal.keys())):
                if (len(goal.keys()) > 1) & (idx < (len(goal.keys()) - 1)):
                    goal_text = goal_text + key + ' = ' + goal[key] + ' , '
                elif len(goal.keys()) == 1:
                    goal_text = goal_text + key + ' = ' + goal[key]
                else:
                    goal_text = goal_text + key + ' = ' + goal[key]
            goal_text = goal_text + ' } ; '
            request_text = 'requested_slots : { '
            for idx, value in enumerate(requested_slot):
                if (len(requested_slot) > 1) & (idx < (len(requested_slot) - 1)):
                    request_text = request_text + value + ' , '
                elif len(requested_slot) == 1:
                    request_text = request_text + value
                else:
                    request_text = request_text + value
            request_text = request_text + ' } , '
            method_text = 'method : ' + method
            combine = goal_text + request_text + method_text
            combine = combine.replace('  ',' ')
            if data_address+'\n' in dev_list:
                dev_src_write.write(src)
                dev_src_write.write('\n')
                dev_tgt_write.write(combine)
                dev_tgt_write.write('\n')
            elif data_address+'\n' in train_list:
                train_src_write.write(src)
                train_src_write.write('\n')
                train_tgt_write.write(combine)
                train_tgt_write.write('\n')
            elif data_address+'\n' in test_list:
                test_src_write.write(src)
                test_src_write.write('\n')
                test_tgt_write.write(combine)
                test_tgt_write.write('\n')
train_src_write.close()
train_tgt_write.close()
dev_src_write.close()
dev_tgt_write.close()
test_src_write.close()
test_tgt_write.close()