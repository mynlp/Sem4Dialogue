import json
from treelib import Node, Tree
from anytree.importer import DictImporter
from anytree import RenderTree, AsciiStyle, PreOrderIter, LevelOrderGroupIter
from flatten_dict import flatten

def dfs(target_dialog_state):
    name = target_dialog_state['name']
    children = target_dialog_state['children']
    if len(children) == 0:
        return '({name})'.format(name=name)
    return '('+'{name}'.format(name=name)+''.join(['({name})'.format(name=dfs(c)) for c in children])+')'

dict_flatten = lambda root: '('+'{name}'.format(name=root['name'])+''.join(['{name}'.format(name=dict_flatten(c)) for c in root['children']])+')'

train_file = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/TreeDSTSourceData/train_dst.json', 'r')
dev_file = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/TreeDSTSourceData/dev_dst.json', 'r')
test_file = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/TreeDSTSourceData/test_dst.json', 'r')
train_data = []
dev_data = []
test_data = []
for line in train_file.readlines():
    dic = json.loads(line)
    train_data.append(dic)
for line in dev_file.readlines():
    dic = json.loads(line)
    dev_data.append(dic)
for line in test_file.readlines():
    dic = json.loads(line)
    test_data.append(dic)
for data_type, type in zip([train_data, dev_data, test_data], ['train', 'test', 'valid']):
    train_src_user_utterance = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/processed_data/'+type+'/'+type+'_src_user_utterance.txt', 'w')
    train_src_input_dialog_state = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/processed_data/'+type+'/'+type+'_src_input_dialog_state.txt', 'w')
    train_src_input_system_acts = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/processed_data/'+type+'/'+type+'_src_input_system_state.txt', 'w')
    train_target = open('/Users/chenbowen/Documents/PaperCode/ToyNMT/TreeDST/processed_data/'+type+'/'+type+'_tgt.txt', 'w')
    for data in data_type:
        user_symbol = '<User>'
        speaker_utterance = ''
        End_symbol = '<EndofSpeaking>'
        for turn_idx, turn in enumerate(data['turns']):
            utterance = turn['utterance']
            if turn_idx > 1:
                input_dialog_state = dict_flatten(turn['input_dialog_state']).replace('(', ' ( ').replace(')', ' ) ').replace('  )  ', ' ) ').replace('  ( ', ' ( ').lstrip().rstrip()
                input_system_acts = dict_flatten(turn['input_system_acts'][0]['paths']).replace('(', ' ( ').replace(')', ' ) ').replace('  )  ', ' ) ').replace('  ( ', ' ( ').lstrip().rstrip()
            else:
                input_dialog_state = 'None'
                input_system_acts = 'None'
            target_dialog_state = turn['target_dialog_state']
            speaker_utterance = speaker_utterance +' '+ user_symbol +' '+utterance+'.'
            tgt = dict_flatten(target_dialog_state).replace('(', ' ( ').replace(')', ' ) ').replace('  )  ', ' ) ').replace('  ( ', ' ( ').lstrip().rstrip()
        train_src_user_utterance.write(speaker_utterance.lstrip())
        train_src_user_utterance.write('\n')
        train_src_input_dialog_state.write(input_dialog_state)
        train_src_input_dialog_state.write('\n')
        train_src_input_system_acts.write(input_system_acts)
        train_src_input_system_acts.write('\n')
        train_target.write(tgt)
        train_target.write('\n')
    train_src_user_utterance.close()
    train_src_input_dialog_state.close()
    train_src_input_system_acts.close()
    train_target.close()




#
# importer = DictImporter()
# root = importer.import_(target_dialog_state)
# pre_order = [node.name for node in PreOrderIter(root)]
# level_order = [[node.name for node in children] for children in LevelOrderGroupIter(root)]
# text = ''
# for node in pre_order:
#    # for node_depth, level_node in enumerate(level_order):
#    #     if node in level_node:
#    #         node_level = node_depth
#     text = text + '(' + node + ')'
#
# for node in level_order:
#
#
# print(RenderTree(root))