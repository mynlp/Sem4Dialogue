from utils.seq2seq_metric import word_level_em_accuracy, token_level_em_accuracy, sentence_level_em_accuracy
import argparse

parser = argparse.ArgumentParser(description='metric')
parser.add_argument('--prediction_file', type=str, default='Spider/LSTM_pred_10000.txt')
parser.add_argument('--target_file', type=str, default='Spider/processed_spider/dev_tgt.txt')
parser.add_argument('--dataset', type=str, default='Spider')
args = parser.parse_args()

#tgt_file = 'SCAN/processed_simple_split/tasks_train_simple_tgt.txt'
word_level_em = word_level_em_accuracy(args.prediction_file, args.target_file)
token_level_em = token_level_em_accuracy(args.prediction_file, args.target_file)
sentence_level_em = sentence_level_em_accuracy(args.prediction_file, args.target_file)
print('Sentence-level EM Accuracy for '+args.dataset+':'+str(sentence_level_em*100)+'%')
print('Word-level EM Accuracy for '+args.dataset+':'+str(word_level_em*100)+'%')
print('Character-level EM Accuracy for '+args.dataset+':'+str(token_level_em*100)+'%')


