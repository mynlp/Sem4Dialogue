def word_level_em_accuracy(prediction_file, target_file):
    f_pred = open(prediction_file, 'r')
    f_tgt = open(target_file, 'r')
    accuracy_list = []
    for pred_line, tgt_line in zip(f_pred.readlines(), f_tgt.readlines()):
        correct_count = 0
        for predicted_token, tgt_token in zip(pred_line.split(), tgt_line.split()):
            if predicted_token == tgt_token:
                correct_count += 1
        accuracy = correct_count/len(tgt_line.split())
        accuracy_list.append(accuracy)
    em = sum(accuracy_list)/len(accuracy_list)
    return em

def token_level_em_accuracy(predicition_file, target_file):
    f_pred = open(predicition_file, 'r')
    f_tgt = open(target_file, 'r')
    accuracy_list = []
    for pred_line, tgt_line in zip(f_pred.readlines(), f_tgt.readlines()):
        correct_count = 0
        for predicted_token, tgt_token in zip(pred_line, tgt_line):
            if predicted_token == tgt_token:
                correct_count += 1
        accuracy = correct_count / len(pred_line)
        accuracy_list.append(accuracy)
    em = sum(accuracy_list) / len(accuracy_list)
    return em

def sentence_level_em_accuracy(prediction_file, target_file):
    f_pred = open(prediction_file, 'r')
    f_tgt = open(target_file, 'r')
    accuracy_list = []
    sentence_level_count = 0
    for pred_line, tgt_line in zip(f_pred.readlines(), f_tgt.readlines()):
        correct_count = 0
        for predicted_token, tgt_token in zip(pred_line.split(), tgt_line.split()):
            if predicted_token == tgt_token:
                correct_count += 1
        try:
            accuracy = correct_count / len(tgt_line.split())
            accuracy_list.append(accuracy)
        except ZeroDivisionError:
            pass
        if correct_count == len(tgt_line.split()):
            sentence_level_count = sentence_level_count + 1
    em = sentence_level_count / len(accuracy_list)
    return em


def slot_accuracy_atis(prediction_file, target_file):
    f_pred = open(prediction_file, 'r')
    f_tgt = open(target_file, 'r')
    accuracy_list = []
    for pred_line, tgt_line in zip(f_pred.readlines(), f_tgt.readlines()):
        single_correct = 0
        joint_correct = 0

def bleu_score(prediction_file, target_file):
    pass


def denotation_accuracy():
    pass


