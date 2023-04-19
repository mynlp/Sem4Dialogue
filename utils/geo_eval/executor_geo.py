"""An executor for GeoQuery FunQL programs."""

from overrides import overrides
from pyswip import Prolog
import re

from utils.executor import Executor


@Executor.register("geo_executor")
class ProgramExecutorGeo(Executor):

    def __init__(self):
        self._prolog = Prolog()
        self._prolog.consult('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/utils/geo_eval/geobase.pl')
        self._prolog.consult('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/utils/geo_eval/geoquery.pl')
        self._prolog.consult('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/utils/geo_eval/eval.pl')

    @overrides
    def execute(self, program: str, kb_str: str = None) -> str:
        # make sure entities with multiple words are parsed correctly
        program = re.sub("' (\w+) (\w+) '", "'"+r"\1#\2"+"'", program)
        program = re.sub("' (\w+) (\w+) (\w+) '", "'" + r"\1#\2#\3" + "'", program)
        program = program.replace(' ','').replace('#',' ')

        try:
            answers = list(self._prolog.query("eval(" + '{}, X'.format(program) + ").", maxresult=1))
        except Exception as e:
            return 'error_parse: {}'.format(e)
        return str([str(answer) for answer in answers[0]['X']])


if __name__ == "__main__":
    f_gold = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/geo/processed_geo/test_tgt.txt', 'r')
    f_pred = open('/Users/chenbowen/Documents/PaperCode/Seq2SeqParingandDialogue/geo/pred_3000.txt', 'r')
    gold_programs = f_gold.readlines()
    pred_programs = f_pred.readlines()
    f_gold.close()
    f_pred.close()
    executor = ProgramExecutorGeo()
    correct_count = 0
    j = 0
    for (idx, pred_program), gold_program in zip(enumerate(pred_programs), gold_programs):
        if idx != 214:
            gold_program = gold_program.replace('program: ', '').replace('\n', '')
            pred_program = pred_program.replace('program: ', '').replace('\n', '')
            gold_denotation = executor.execute(gold_program)
            pred_denotation = executor.execute(pred_program)
            print('result of gold program:')
            print(gold_denotation)
            print('result of target program:')
            print(pred_denotation)
            if gold_denotation == pred_denotation:
                correct_count = correct_count + 1
            j = j + 1
            print(idx)
    print(correct_count/len(gold_programs))
