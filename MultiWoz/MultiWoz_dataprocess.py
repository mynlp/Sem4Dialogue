import json

f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/data/train_dials.json', 'r')
train_data = json.load(f)
f.close()
f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/data/dev_dials.json', 'r')
dev_data = json.load(f)
f.close()
f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/data/test_dials.json', 'r')
test_data = json.load(f)
f.close()

for data_type, data in zip(['train', 'dev', 'test'], [train_data, dev_data, test_data]):
    f_src = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/MultiWoz_processed/'+data_type+'_src.txt', 'w')
    f_sys_act = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/MultiWoz_processed/'+data_type+'_act.txt', 'w')
    f_tgt = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/MultiWoz/MultiWoz_processed/'+data_type+'_tgt.txt', 'w')
    for single_data in data:
        turn_string = ''
        for turn_idx, turn in enumerate(single_data['dialogue']):
            turn_string = turn_string +' '+ turn['transcript']
            belief_states = turn['belief_state']
            concat_string = ''
            for belief_state in belief_states:
                act = belief_state['act']
                slots = belief_state['slots']
                print(slots)
                slot_string = slots[0][0].replace(' ', '-') + ': ' + slots[0][1]
                concat_string = concat_string + act + ' '+slot_string + ' ; '
            if turn['system_acts'] == []:
                system_acts = '<NoACT>'
            else:
                system_acts = ''
                for act in turn['system_acts']:
                    if type(act) == str:
                        system_acts = system_acts + ' '+act
                    elif type(act) == list:
                        for sub_act in act:
                            system_acts = system_acts+' '+sub_act
            if (concat_string == ''):
                concat_string = 'inform noMove ;'
            f_src.write(turn_string)
            f_src.write('\n')
            f_sys_act.write(system_acts)
            f_sys_act.write('\n')
            f_tgt.write(concat_string)
            f_tgt.write('\n')
    f_src.close()
    f_sys_act.close()
    f_tgt.close()

