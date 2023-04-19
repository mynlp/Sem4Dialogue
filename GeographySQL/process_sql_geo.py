# whole = []
# for name in ['train','dev','test']:
#     f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.'+name,'r')
#     data = f.readlines()
#     f.close()
#     whole.extend(data)
# test = []
# f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/geo.txt','r')
# data = f.readlines()
# f.close()
# test.extend(data)
#
# f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.test', 'w')
# for example in test:
#     f.write(example)
# f.close()
#
# over_lap = []
# non_over_lap = []
# count = 0
# for example in test:
#     if example in whole:
#         over_lap.append(example)
#         count+=1
#         print(count)
#     else:
#         non_over_lap.append(example)
for name in ['train','dev','test']:
    f = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/raw/geography.'+name,'r')
    data = f.readlines()
    f.close()
    src_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/processed_geographysql/src_'+name+'.txt','w')
    tgt_write = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/GeographySQL/processed_geographysql/tgt_'+name+'.txt','w')
    for example in data:
        try:
           src, tgt = example.split('|||')
           src_write.write(src.lstrip().rstrip())
           src_write.write('\n')
           tgt_write.write(tgt.lstrip().rstrip())
           tgt_write.write('\n')
        except ValueError:
            print(name)
    src_write.close()
    tgt_write.close()
