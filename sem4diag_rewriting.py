#This is the code for transforming between languages
import re
from mo_sql_parsing import parse, parse_mysql
from pyparsing import nestedExpr, exceptions
from anytree.importer import DictImporter
from anytree import Node, RenderTree
from treelib import Node, Tree
from tqdm import tqdm
import json
import copy
from onmt.constants import DefaultTokens

def read_language(address): #use this read api if your data is txt format
    f = open(address, 'r')
    data = f.readlines()
    f.close()
    return data

def read_json(address): #use this read api if your data is json format
    data = []
    file = open(address, 'r')
    for line in file.readlines():
        dic = json.loads(line)
        data.append(dic)
    return data

#processing for SCAN
#the scan can be seen as a function and parameter, turn_left is the function turn and parameter left
def scan_processing(tgt_data):
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        tree = Tree()
        tree.create_node('ROOT',0)
        splited_list = line.split()
        count = 1
        for cmd in splited_list[1:]:
            tokens = cmd.split('_')
            if len(tokens) == 3:
                function = tokens[1]
                parameter = tokens[2]
                tree.create_node(function, count, parent=0)
                count += 1
                tree.create_node(parameter, count, parent=count-1)
                count += 1
            elif len(tokens) == 2:
                paramerter_less_function = tokens[1]
                tree.create_node(paramerter_less_function, count, parent=0)
                count += 1
                tree.create_node('None', count, parent=count - 1)
                count += 1
        #tree.show()
        new_data.append(tree)
    return new_data

def scan_processing_atomic_level(tgt_data):
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        if idx == 344:
            a=1+1
        tree=line.replace('I_', '').replace('_', ' ').replace('OUT: ', '').replace('\n', '')
        turn_splited = tree.split('TURN')
        previous = ''
        new_tree = ''
        begin_idx = 1
        if len(turn_splited)==1:
            begin_idx=0
        for idx, move in enumerate(turn_splited[begin_idx:]):
            if move.lstrip().rstrip() != previous.lstrip().rstrip():
                if idx >= 1:
                    new_tree += ' ) '
                if ('RIGHT' not in move)&('LEFT' not in move) :
                    new_tree += move
                else:
                    new_tree += 'Turn ( ' + move + ' ,'
                    if len(turn_splited[begin_idx:]) == 1:
                        new_tree += ' )'
                    if idx == len(turn_splited[begin_idx:])-1:
                        new_tree += ' )'
            else:
                if idx != len(turn_splited[begin_idx:])-1:
                    new_tree += ' '+move+' , '
                else:
                    new_tree += ' ' + move + ' )'
            previous = move
        new_tree = 'ROOT ( '+new_tree.replace('  ',' ').replace(', )', ' )')+' )'
        new_data.append(new_tree.replace('  ', ' '))
    return new_data

def scan_processing_higher_combine_level(tgt_data):
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        if idx==97:
            a =1
        tree=line.replace('I_', '').replace('OUT: ', '').replace('\n', '')
        turn_splited = tree.split()
        new_tree = ''
        if len(turn_splited) > 1:
            for idx_l in range(0, len(turn_splited), 2):
                if idx_l + 1 != len(turn_splited):
                    if turn_splited[idx_l] != turn_splited[idx_l+1]:
                        new_tree += ' '.join(turn_splited[idx_l:idx_l+2]).replace(' ', '_')+' '
                    else:
                        new_tree += turn_splited[idx_l]+' '+turn_splited[idx_l+1]+' '
                else:
                    new_tree += turn_splited[idx_l] + ' '
        else:
            new_tree += turn_splited[0] + ' '
        new_tree = new_tree.replace('  ', ' ')
        turn_splited = new_tree.split('TURN_')
        previous = ''
        renew_tree = ''
        begin_idx = 1
        if len(turn_splited) == 1:
            begin_idx = 0
        for idx, move in enumerate(turn_splited[begin_idx:]):
            if move.lstrip().rstrip().lstrip('_').rstrip('_') != previous.lstrip().rstrip():
                move = move.lstrip().rstrip().lstrip('_').rstrip('_')
                if idx >= 1:
                    renew_tree += ' ) '
                if ('RIGHT' not in move) & ('LEFT' not in move):
                    renew_tree += move
                else:
                    renew_tree += 'Turn ( ' + move + ' ,'
                    if len(turn_splited[begin_idx:]) == 1:
                        renew_tree += ' )'
                    if idx == len(turn_splited[begin_idx:]) - 1:
                        renew_tree += ' )'
            else:
                if idx != len(turn_splited[begin_idx:]) - 1:
                    renew_tree += ' ' + move + ' , '
                else:
                    renew_tree += ' ' + move + ' )'
            previous = move.lstrip().rstrip().lstrip('_').rstrip('_')
        renew_tree = 'ROOT ( '+renew_tree.replace('  ',' ').replace(', )', ' )')+' )'
        new_data.append(renew_tree.replace('  ', ' '))
    return new_data

def scan_processing_higher_combine_level_new(tgt_data):
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        if idx==94:
            a =1
        tree=line.replace('I_', '').replace('OUT: ', '').replace('\n', '')
        turn_splited = tree.split()
        idx = 0
        temp = []
        flag = True
        while idx < len(turn_splited)-1:
            pre = turn_splited[idx]
            cur = turn_splited[idx+1]
            if pre == cur:
                temp.append(pre)
                idx += 1
                flag = True
            elif (pre != cur)&((pre not in ['TURN_LEFT', 'TURN_RIGHT'])|(cur not in ['TURN_LEFT', 'TURN_RIGHT'])):
                temp.append(pre+'_'+cur)
                idx += 2
                if idx == len(turn_splited)-1:
                    flag = True
                else:
                    flag = False
            else:
                temp.append(pre)
                idx += 1
                flag = True
        if flag == True:
            temp.append(turn_splited[idx])
        renew_tree = ' '.join(temp)
        temp = [[]]
        counter = 0
        no_turn = True
        for idx, move in enumerate(renew_tree.split()):
            if 'TURN' in move:
                temp[counter].append(move)
                no_turn = False
            else:
                if no_turn == False:
                    temp.append([])
                    counter += 1
                    no_turn = True
                temp[counter].append(move)
        temp_tree = 'ROOT ( '
        for move_list in temp:
            if 'TURN' in move_list[0]:
                init = 'Turn ( '
            else:
                init = ' ( '
            for single_move in move_list:
                init += single_move.replace('TURN_','') + ' '
            init += ' ) '
            temp_tree += init
        temp_tree += ' ) '
        new_data.append(temp_tree.replace('  ', ' '))
    return new_data

#processing for nlmaps
def nlmaps_processing(tgt_data):
    new_data = []
    def processing_nested_list_node(nested_list, node, parent, count=0, sub_tract=0):
        for idx, example in enumerate(nested_list):
            if type(example) == list:
                if sum([type(x) == str for x in example]) == len(example):
                    para_list = []
                    para = ''
                    for x in example:
                        if x != ',':
                            para = para + x
                        else:
                            para_list.append(para)
                            para = ''
                    para_list.append(para)
                    if len(para_list) == 2:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                        tree.create_node(para_list[1], count, parent=parent)
                        count = count + 1
                    else:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                    continue
                if node == None:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
                else:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
            else:
                if example != ',':
                    if parent == None:
                        tree.create_node(example, count)
                        parent = count
                        count += 1
                    else:
                        if example=='search':
                            a = 1+1
                        if sub_tract <=1:
                            tree.create_node(example, count, parent=parent - sub_tract)
                        else:
                            tree.create_node(example, count, parent=tree[parent].bpointer)
                        parent = count
                        count += 1
                elif example == ',':
                    sub_tract += 1
        return count
    def change_semantics(tree):
        for tree_idx, node in enumerate(tree):
            if node.tag == 'keyval':
                parent_id = node.bpointer
                child_list = tree.subtree(tree_idx).children(tree_idx)
                tree.move_node(node.identifier, tree[parent_id].bpointer)
                tree.move_node(parent_id, parent_id+1)
                #tree.remove_node(child_list[0].identifier)
                #tree.create_node(tag=child_list[0].tag,identifier=child_list[0].identifier)
                tree.move_node(child_list[0].identifier, parent_id)
            if (node.tag == 'and')|(node.tag == 'or'):
                if tree[node.fpointer[0]].tag=='keyval':
                    parent_id = tree[tree_idx].bpointer
                    tree[tree_idx].tag, tree[parent_id].tag = tree[parent_id].tag, tree[tree_idx].tag
                    child_list = tree.subtree(tree_idx).children(tree_idx)
                    nodes = tree.all_nodes()
                    nodes.reverse()
                    for update_node in nodes[:len(nodes)-child_list[1].identifier]:
                        tree.update_node(update_node.identifier, identifier=update_node.identifier+1)
                    tree.create_node(tree[tree_idx].tag, identifier=child_list[1].identifier-1, parent=parent_id)
                    tree.move_node(child_list[1].identifier, child_list[1].identifier-1)
            if tree_idx == len(tree)-1:
                break
        return tree
    for idx, line in enumerate(tgt_data):
        # if ' and ' in line:
        #     a = 1+1
        # else:
        #     continue
        try:
            list_data = nestedExpr('(', ')', ignoreExpr=None).parseString('( ' +line.replace('\n', '').replace("de ( Psy", 'de Psy')+ ' )').asList()
            tree = Tree()
            processing_nested_list_node(list_data, node=tree, parent = None)
        except exceptions.ParseException:
            print(idx)
            print(line)
        #print(tree.show())
        new_data.append(change_semantics(tree))
    return new_data
#processing for sql. Some datasets like SParC SQL have several problematic SQL codes, if it reports warining, you can
#add codes to skip such problematic code
def sql_processing(tgt_data):
    error_list = []
    parsed = []
    original_result = []
    def dict_parsing(result, count=1, parent=0):
        old_parent = parent
        for idx, key in enumerate(list(result.keys())):
            tree.create_node(key, count, parent=old_parent)
            parent = tree[count].identifier
            count = count + 1
            if type(result[key]) == dict:
                count = dict_parsing(result[key], count, parent=parent)
            elif type(result[key]) == list:
                for idx, sub_value in enumerate(result[key]):
                    if type(sub_value) == dict:
                        if ('value' in list(sub_value.keys())):
                            count = dict_parsing(sub_value, count, parent=parent)
                        else:
                            count = dict_parsing(sub_value, count, parent=parent)
                    else:
                        tree.create_node(str(sub_value), count, parent=parent)
                        #parent = tree[count].identifier
                        count += 1
            else:
                tree.create_node(result[key], count, parent=parent)
                #parent = tree[count].identifier
                count += 1
        return count
    def tree_cut(tree):
        for tree_idx in range(len(tree)):
            if tree[tree_idx].tag == 'value':
                parent_id = tree[tree_idx].bpointer
                child_list = tree.subtree(tree_idx).children(tree_idx)
                for child in child_list:
                    tree.move_node(child.identifier, parent_id)
                tree.remove_node(tree_idx)
        return tree
    for idx, line in tqdm(enumerate(tgt_data)):
        tree = Tree()
        tree.create_node('ROOT', 0)
        count = 1
        try:
            result = parse_mysql(line.replace('! =', '!=').replace('> =', '>=').replace('< =', '<=').replace("`` ", "'").replace(" ''", "'").replace("=' ;", "= '' ;"))
            original_result.append(result)
            dict_parsing(result, count=count, parent=0)
            #tree.show()
            parsed.append(tree)
        except:
            error_list.append(idx)
    return parsed, error_list
#dialogue state tracking processing
def dst_processing_multiwoz(tgt_data):
    new_tgt_data = []
    for line in tqdm(tgt_data):
        tree = Tree()
        tree.create_node('ROOT', 0)
        count = 1
        splited_slot = line.replace('\n', '').lstrip().rstrip().split(' ;')
        splited_slot.pop()
        for slot in splited_slot:
            if 'noMove' not in slot:
                funslot, value=slot.split(': ')
                func, slot = funslot.split()
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node('equals', count, parent=count-1) # equal is added to gurantee semantic uniformity
                count += 1
                tree.create_node(slot, count, parent=count-1)
                count += 1
                tree.create_node(value, count, parent=count-2)
                count += 1
            else:
                func, value = slot.split(':')
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node(value, count, parent=count - 1)
                count += 1
        new_tgt_data.append(tree)
    return new_tgt_data

def dst_processing_atis(tgt_data):
    new_tgt_data = []
    for line in tqdm(tgt_data):
        tree = Tree()
        tree.create_node('ROOT', 0)
        count = 1
        splited_slot = line.replace('\n', '').lstrip().rstrip().split(' ;')
        splited_slot.pop()
        for slot in splited_slot:
            funslot, value=slot.split(': ')
            if ' ' in funslot.lstrip().rstrip():
                func, slot = funslot.lstrip().rstrip().split()
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node('equals', count, parent=count-1) # equal is added to gurantee semantic uniformity
                count += 1
                tree.create_node(slot, count, parent=count-1)
                count += 1
                tree.create_node(value, count, parent=count-2)
                count += 1
            else:
                func, value = slot.split(': ')
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node(value, count, parent=count - 1)
                count += 1
        new_tgt_data.append(tree)
    return new_tgt_data

def dst_processing_m2m(tgt_data):
    new_tgt_data = []
    for line in tqdm(tgt_data):
        tree = Tree()
        tree.create_node('ROOT', 0)
        count = 1
        splited_slot = line.replace('\n', '').lstrip().rstrip().split(' ;')
        splited_slot.pop()
        for slot in splited_slot:
            if slot !='NoSlot':
                func, value = slot.lstrip().rstrip().split(' ')[0], ' '.join(slot.lstrip().rstrip().split(' ')[1:])
                tree.create_node('equals', count, parent=0)  # equal is added to gurantee semantic uniformity
                count += 1
                tree.create_node(func, count, parent=count-1)
                count += 1
                tree.create_node(value, count, parent=count-2)
                count += 1
            else:
                func = slot
                tree.create_node(func, count, parent=0)
                count += 1
        new_tgt_data.append(tree)
    return new_tgt_data

def dst_processing_dstc(tgt_data):
    new_tgt_data = []
    for line in tqdm(tgt_data):
        tree = Tree()
        tree.create_node('ROOT', 0)
        count = 1
        splited_slot = line.replace('\n', '').lstrip().rstrip().split(' ;')
        splited_slot.pop()
        for slot in splited_slot:
            if ('noMove' not in slot)&('None' not in slot):
                try:
                    funslot, value=slot.split(': ')
                except:
                    a=1
                func, slot = funslot.split()
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node('equals', count, parent=count-1) # equal is added to gurantee semantic uniformity
                count += 1
                tree.create_node(slot, count, parent=count-1)
                count += 1
                tree.create_node(value, count, parent=count-2)
                count += 1
            else :
                func, value = slot.lstrip().rstrip().split(' ')
                tree.create_node(func, count, parent=0)
                count += 1
                tree.create_node(value, count, parent=count - 1)
                count += 1
        new_tgt_data.append(tree)
    return new_tgt_data
# funql processing
def funql_processing(tgt_data):
    def processing_nested_list_node(nested_list, node, parent, count=0, sub_tract = 0):
        for idx, example in enumerate(nested_list):
            if type(example) == list:
                if sum([type(x) == str for x in example]) == len(example):
                    para_list = []
                    para = ''
                    for x in example:
                        if x != ',':
                            para = para + x
                        else:
                            para_list.append(para)
                            para = ''
                    para_list.append(para)
                    if len(para_list) == 2:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                        tree.create_node(para_list[1], count, parent=parent)
                        count = count + 1
                    else:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                    continue
                if node == None:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
                else:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
            else:
                if example != ',':
                    if parent == None:
                        tree.create_node(example, count)
                        parent = count
                        count += 1
                    else:
                        tree.create_node(example, count, parent=parent - sub_tract)
                        parent = count
                        count += 1
                elif example == ',':
                    sub_tract += 1
        return count
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        line = line.replace('program: ', '').replace('\n', '')
        list_data = nestedExpr('(', ')').parseString(
        '( ' + line.replace('\n', '')+ ' )').asList()
        tree= Tree()
        processing_nested_list_node(list_data, node=tree, parent = None)
        new_data.append(tree)
    return new_data
#smcalflow processing
def smcal_flow_processing(tgt_data):
    new_data = []
    cutted_new_data = []
    delete_pattern = 'Execute|Commit|Preflight|QueryEventResponse|\^|roleConstraint'
    merge_pattern = '^<Event>|Dynamic[^>]'
    constraint_pattern = '\({1}.\^[^\)]*\)[^\)]*\)'
    inside_constrain_pattern = '\({1}[^^)]*\){1}'
    equalizer_pattern = '\({1}[^=\(]*[=][^=\)]*\){1}' #match the ?~= and ?= in the expression
    apply_pattern = '\({1}[^=\(]*apply[^=\)]*\){1}' #match the .apply function
    error_list = []
    def processing_nested_list_node(nested_list, node, parent, count=0, sub_tract=0):
        for idx, example in enumerate(nested_list):
            if type(example) == list:
                if sum([type(x) == str for x in example]) == len(example):
                    para_list = []
                    para = ''
                    for x in example:
                        if x != ',':
                            para = para + x + ' '
                        else:
                            para_list.append(para)
                            para = ''
                    para_list.append(para)
                    if len(para_list) == 2:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                        tree.create_node(para_list[1], count, parent=parent)
                        count = count + 1
                    else:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                    continue
                if node == None:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
                else:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
            else:
                if example != ',':
                    if parent == None:
                        tree.create_node(example, count)
                        parent = count
                        count += 1
                    else:
                        tree.create_node(example, count, parent=parent - sub_tract)
                        parent = count
                        count += 1
                elif example == ',':
                    sub_tract += 1
        return count
    def tree_cut(tree):
        removed_before_current_node = 0
        for tree_idx in range(len(tree)):
            if 'refer' in tree[tree_idx].tag:
                tree[tree_idx].tag = tree[tree_idx].tag+"[RetrivePreviousInformation]"
            if re.search(delete_pattern, tree[tree_idx].tag) != None:
                parent_id = tree[tree_idx].bpointer
                child_list = tree.subtree(tree_idx).children(tree_idx)
                for child in child_list:
                    tree.move_node(child.identifier, parent_id)
                removed_before_current_node += 1
                tree.remove_node(tree_idx)
            elif (re.search(merge_pattern, tree[tree_idx].tag) != None):
                parent_id = tree[tree_idx].bpointer
                child_list = tree.subtree(tree_idx).children(tree_idx)
                for child in child_list:
                    tree.move_node(child.identifier, parent_id)
                if 'Event' not in tree[tree_idx].tag:
                    if tree[parent_id].tag != 'Yield': # we do not attach input constraint to Yield, since it is the root of the program, it should not have any limit in constrain
                        tree[parent_id].tag = tree[parent_id].tag + '<'+tree[tree_idx].tag.replace(' ', '')+'>'
                else:
                    tree[parent_id].tag = tree[parent_id].tag + tree[tree_idx].tag
                tree.remove_node(tree_idx)
                removed_before_current_node += 1
            else:
                removed_before_current_node = 0
        return tree
    for idx, line in tqdm(enumerate(tgt_data)):
        try:
            all_constrain = re.findall(constraint_pattern, line)
            equalizers = re.findall(equalizer_pattern, line)
            apply_matchers = re.findall(apply_pattern, line)
            constrain_type = []
            for equalizer in equalizers:
                if '(' not in equalizer.lstrip('('):
                    line = line.replace(equalizer, equalizer.replace('= " ', '= ( " ')+' ) ')
            for applly_match in apply_matchers:
                line = line.replace(applly_match, applly_match.replace('.apply " ', '.apply:[PossibleCanditateOfRetrieve] ( " ')+' ) ')
            for constrain in all_constrain:
                fine_grained_constrain = re.findall(inside_constrain_pattern, constrain)[0]
                constrain_type.append(fine_grained_constrain)
                if 'Path' in constrain:
                    line = line.replace(' ' + constrain + ' )', ' <' + fine_grained_constrain.replace('( ', '').replace(' )', '') + '>')
                elif 'Execute ( ^' in line: # if it the constraint directly attaches a Execute, we do nothing, because it will remove the whole program
                    line = line
                else:
                    line = line.replace(' '+constrain, '<'+fine_grained_constrain.replace('( ', '').replace(' )', '')+'>')
            line = line.replace('?=', 'Match.exact_:[PossibleCanditateOfRetrieve]').replace('?~=', 'Match.approx_:[PossibleCanditateOfRetrieve]')
            list_data = nestedExpr('(', ')').parseString(line.replace('\n', '')).asList()
            tree= Tree()
            processing_nested_list_node(list_data, node=tree, parent=None)
            new_data.append(copy.copy(tree))
            cutted_new_data.append(tree_cut(tree))
        except:
            error_list.append(idx)
    return cutted_new_data, error_list
#treedst processing
def treedst_processing(tgt_data):
    def processing_nested_list_node(nested_list, node, parent, count=0, sub_tract=0):
        for idx, example in enumerate(nested_list):
            if type(example) == list:
                if sum([type(x) == str for x in example]) == len(example):
                    para_list = []
                    para = ''
                    for x in example:
                        if x != ',':
                            para = para + x + ' '
                        else:
                            para_list.append(para)
                            para = ''
                    para_list.append(para)
                    if len(para_list) == 2:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                        tree.create_node(para_list[1], count, parent=parent)
                        count = count + 1
                    else:
                        tree.create_node(para_list[0], count, parent=parent)
                        count = count + 1
                    continue
                if node == None:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
                else:
                    count = processing_nested_list_node(example, node, parent=parent, count=count)
            else:
                if example != ',':
                    if parent == None:
                        tree.create_node(example, count)
                        parent = count
                        count += 1
                    else:
                        tree.create_node(example, count, parent=parent - sub_tract)
                        parent = count
                        count += 1
                elif example == ',':
                    sub_tract += 1
        return count
    def change_semantics(tree):
        for tree_idx, node in enumerate(tree):
            if (node.tag == 'greaterThanOrEquals')|(node.tag == 'lessThanOrEquals')|(node.tag == 'notEquals'):
                parent_id = node.bpointer
                child_list = tree.subtree(tree_idx).children(tree_idx)
                if len(child_list)==1:
                    tree.move_node(node.identifier, tree[parent_id].bpointer)
                    tree.move_node(parent_id, parent_id+1)
            elif (node.tag == 'equals'):
                parent_id = node.bpointer
                if tree[parent_id].tag == 'object':
                    node.tag = '&'
                    continue
                child_list = tree.subtree(tree_idx).children(tree_idx)
                if len(child_list) == 1:
                    tree.move_node(node.identifier, tree[parent_id].bpointer)
                    tree.move_node(parent_id, parent_id + 1)
            if tree_idx == len(tree)-1: #seems the enumerate will continue to iterate even in the end of tree, seems to be the problem of the tree package, we need to terminate the iter manully
                break
        return tree
    new_data = []
    for idx, line in tqdm(enumerate(tgt_data)):
        print(idx)
        line = line.replace('\n', '')
        list_data = nestedExpr('(', ')', ignoreExpr=None).parseString(line).asList()
        tree = Tree()
        processing_nested_list_node(list_data, node=tree, parent=None)
        new_data.append(change_semantics(tree))
    return new_data

#to add your dataset, you should write your own parsing code in above area.

# this is to linearize the tree to linearized format
def tree_to_linearize_format(tree_data, task='TreeDST'): # acceptes tree_data and corresponding task,notice that this is the code that you have to modify if you want to implement on new data.
    def dict_traverse(tree_dict, linearize_string='', close=True, task=task):
        if type(tree_dict)==dict:
            for key in list(tree_dict.keys()):
                if key !='children':
                    if task != 'SCAN':
                        linearize_string += key + ' ( '
                    else:
                        linearize_string += key + ' ' + DefaultTokens.PAD + ' '
                if type(tree_dict[key]) == dict:
                    linearize_string = dict_traverse(tree_dict[key], linearize_string, task=task)
                if type(tree_dict[key]) == list:
                    linearize_string = dict_traverse(tree_dict[key], linearize_string, task=task)
        elif type(tree_dict) == list:
            for idx, sub_dict in enumerate(tree_dict):
                if type(sub_dict) == dict:
                    if (len(tree_dict)>1)&(idx<len(tree_dict)-1):
                        close=False
                    else:
                        close=True
                        if (linearize_string.split()[-1] != ',')*(linearize_string.split()[-1] != '('):
                            linearize_string += ' , '
                    linearize_string = dict_traverse(sub_dict, linearize_string, close=close, task=task)
                elif type(sub_dict) == str:
                    if (idx == 0):
                        linearize_string += ' '+ sub_dict + ' '
                    elif idx >= 1:
                        linearize_string += ' , '+ sub_dict + ' '
            key = sub_dict
        if (key != 'children')&(type(key)!=dict)&(close != False):
            if task != 'SCAN':
                return linearize_string + ' )'
            else:
                return linearize_string + ' ' + DefaultTokens.PAD + ' '
        elif (close==False)&(task != 'TreeDST'):
            return linearize_string + ' , '
        elif (close==False)&(task == 'SCAN'):
            return linearize_string + ' ' + DefaultTokens.PAD + ' '
        elif (close==False)&(task == 'TreeDST'):
            return linearize_string + ' ) ( '
        else:
            return linearize_string
    linearize_list = []
    error_list = []
    for idx, tree in tqdm(enumerate(tree_data)):
        if idx == 82:
            a = 1
        tree_dict = tree.to_dict(sort=False)
        linearize_string=dict_traverse(tree_dict, '( ', task=task)
        linearize_list.append(linearize_string.replace('   ', ' ').replace('  ',' '))
    return linearize_list, error_list

# I don't think following code should be modified if you want to use for you own task, this writes linearized tree or text data, just for writing, and no data processing happened in here.
# this writes linearized tree data
def write_tree_data(tree_list, address_tgt, src_data, address_src, task):
    f_tgt = open(address_tgt, 'w')
    f_src = open(address_src, 'w')
    linearize_string_list, error_list = tree_to_linearize_format(tree_list, task)
    for x in error_list:
        del src_data[x]
    print(len(linearize_string_list))
    for linearize_string, src_string in zip(linearize_string_list, src_data):
        f_tgt.write(linearize_string)
        f_tgt.write('\n')
        f_src.write(src_string)
    f_tgt.close()
    f_src.close()
# this writes txt data
def write_text_data(tree_list, address_tgt, src_data, address_src, task):
    f_tgt = open(address_tgt, 'w')
    f_src = open(address_src, 'w')
    for linearize_string, src_string in zip(tree_list, src_data):
        f_tgt.write(linearize_string)
        f_tgt.write('\n')
        f_src.write(src_string)
    f_tgt.close()
    f_src.close()
#below reads the data from train, valid and test. If you data's test set is on a remote server, you can only transform train and valid
task='M2M' # defiens which task you want to rewrite
train_src_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/train_src.txt') # a api that is designed to read data
train_tgt_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/train_tgt.txt')# as semantic parsing always have a src (human utterance) and tgt (parsed output)
valid_src_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/valid_src.txt')
valid_tgt_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/valid_tgt.txt')
test_src_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/test_src.txt')# comment this if your data does not have test set
test_tgt_data = read_language('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/ATIS_processed/test_tgt.txt')# comment this if your data does not have test set
# We do not want to modify the user input, which is the src data, we only want to transform tgt data
new_train_tgt_data = dst_processing_m2m(train_tgt_data) # use the api for your data to process train, valid, and test
new_valid_tgt_data = dst_processing_m2m(valid_tgt_data)
new_test_tgt_data = dst_processing_m2m(test_tgt_data)
write_tree_data(new_train_tgt_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/train_tgt.txt', train_src_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/train_src.txt', task)
write_tree_data(new_valid_tgt_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/valid_tgt.txt', valid_src_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/valid_src.txt', task)
write_tree_data(new_test_tgt_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/test_tgt.txt', test_src_data, '/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/ATIS/tree_processed_atis/test_src.txt', task) # comment if your data does not have test set
