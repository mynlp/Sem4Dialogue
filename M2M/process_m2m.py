import json
dtype = 'gen'
for name in ['train', 'dev', 'test']:
    f = open('M2M/sim-GEN/data/'+name+'.json')
    data = json.load(f)
    f_src = open('M2M/m2m_gen_processed/' + name + '_src.txt', 'w')
    f_sys_act = open('M2M/m2m_gen_processed/' + name + '_act.txt', 'w')
    f_tgt = open('M2M/m2m_gen_processed/' + name + '_tgt.txt', 'w')
    for example in data:
        turn_string = ''
        for turn_idx, turn in enumerate(example['turns']):
            if dtype == 'gen':
                turn_string = turn_string +' '+ turn['user_utterance']
                dialogue_state = turn['dialogue_state']
                dst = ''
                for key in dialogue_state.keys():
                    dst = dst + key + ' ' + dialogue_state[key] + ' ;'
                if dst == '':
                    dst = 'NoSlot ;'
                sys_act = ''
                for act in turn['system_acts']:
                    move = act['name']
                    if 'slot_values' in act.keys():
                        value = act['slot_values']
                        for act_key in value.keys():
                            sys_act = sys_act + move + ' ; ' + act_key + value[act_key] +' ;'

                    else:
                        sys_act = sys_act + move + ' ;'
            else:
                turn_string = turn_string + ' ' + turn['user_utterance']['text']
                dialogue_state = turn['dialogue_state']
                dst = ''
                for state in dialogue_state:
                    dst = dst + state['slot'] + ' ' + state['value'] + ' ;'
                if dst == '':
                    dst = 'NoSlot ;'
                sys_act = ''
                # for act in turn['system_acts']:
                #     move = act['name']
                #     if 'slot_values' in act.keys():
                #         value = act['slot_values']
                #         for act_key in value.keys():
                #             sys_act = sys_act + move + ' ; ' + act_key + value[act_key] + ' ;'
                #
                #     else:
                #         sys_act = sys_act + move + ' ;'
            f_src.write(turn_string.lstrip())
            f_src.write('\n')
            f_sys_act.write(sys_act)
            f_sys_act.write('\n')
            f_tgt.write(dst)
            f_tgt.write('\n')
    f_src.close()
    f_sys_act.close()
    f_tgt.close()



