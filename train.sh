#!/bin/bash
#SBATCH -J TreeDST
#SBATCH -o TreeDST.out
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH -t 72:00:00
#SBATCH --gres=gpu:tesla_v100s-pcie-32gb:1

source ~/.bashrc

SCAN='SCAN'
GeoQuery='GeoQuery'
SMCalFlow='SMCalFlow'
TreeDST='TreeDST'
ATIS='ATIS'
Sparc='Sparc'
CoSQL='CoSQL'
Clevr='Clevr'
MultiWoz='MultiWoz'
Spider='Spider'
Nlmaps='Nlmaps'
M2M='M2M'
echo "You put $1 as the target task"
echo "You use $2 as the training model"
echo "You evaluate $3 as the evaluation step"
if [ $1 == ${SCAN} ]
then
  #onmt_train -config SCAN.yaml
  onmt_translate -model SCAN/run/${2}_model_step_${3}.pt -src SCAN/processed_length_split/tasks_test_length_src.txt -output SCAN/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file SCAN/${2}_pred_${3}.txt --target_file SCAN/processed_length_split/tasks_test_length_tgt.txt --dataset $1
  cat SCAN/${2}_pred_${3}.txt | sacrebleu  SCAN/processed_length_split/tasks_test_length_tgt.txt -m bleu -b -w 4
elif [ $1 == ${GeoQuery} ]
then
  #onmt_train -config GeoQuery.yaml
  #onmt_translate -model geo/run/${2}_model_step_${3}.pt -src geo/processed_geo/test_src.txt -output geo/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 1
  python metric_test.py --prediction_file geo/${2}_pred_${3}.txt --target_file geo/processed_geo/test_tgt.txt --dataset $1
  cat geo/${2}_pred_${3}.txt | sacrebleu  geo/processed_geo/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${SMCalFlow} ]
then
  onmt_train -config SMCalFlow.yaml
  onmt_translate -model SMCalFlow/run/${2}_model_step_${3}.pt -src SMCalFlow/smcal_flow/valid.src_tok.txt -output SMCalFlow/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 1
  python metric_test.py --prediction_file SMCalFlow/${2}_pred_${3}.txt --target_file SMCalFlow/smcal_flow/valid.tgt.txt --dataset $1
  cat SMCalFlow/${2}_pred_${3}.txt | sacrebleu  SMCalFlow/smcal_flow/valid.tgt.txt -m bleu -b -w 4
elif [ $1 == ${TreeDST} ]
then
  onmt_train -config TreeDST.yaml
  onmt_translate -model TreeDST/run/${2}_model_step_10000.pt -src TreeDST/processed_data/test/test_src_user_utterance.txt -output TreeDST/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 5
  python metric_test.py --prediction_file TreeDST/${2}_pred_${3}.txt --target_file TreeDST/processed_data/test/test_tgt.txt --dataset $1
  cat TreeDST/${2}_pred_${3}.txt | sacrebleu  TreeDST/processed_data/test/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${ATIS} ]
then
  onmt_train -config ATIS.yaml
  onmt_translate -model ATIS/run/${2}_model_step_${3}.pt -src ATIS/ATIS_processed/test_src.txt -output ATIS/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file ATIS/${2}_pred_${3}.txt --target_file ATIS/ATIS_processed/test_tgt.txt --dataset $1
  cat ATIS/${2}_pred_${3}.txt | sacrebleu  ATIS/ATIS_processed/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${Clevr} ]
then
  onmt_train -config Clevr.yaml
  onmt_translate -model Clevr/run/${2}_model_step_${3}.pt -src Clevr/processed_clevr/test_src.txt -output Clevr/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file Clevr/${2}_pred_${3}.txt --target_file Clevr/processed_clevr/test_tgt.txt --dataset $1
  cat Clevr/${2}_pred_${3}.txt | sacrebleu  Clevr/processed_clevr/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${Sparc} ]
then
  #onmt_train -config Sparc.yaml
  #onmt_translate -model Sparc/run/${2}_model_step_${3}.pt -src Sparc/processed_sparc/dev_src.txt -output Sparc/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file Sparc/${2}_pred_${3}.txt --target_file Sparc/processed_sparc/dev_tgt.txt --dataset $1
  cat Sparc/${2}_pred_${3}.txt | sacrebleu  Sparc/processed_sparc/dev_tgt.txt -m bleu -b -w 4
elif [ $1 == ${Spider} ]
then
  #onmt_train -config Spider.yaml
  onmt_translate -model Spider/run/${2}_model_step_${3}.pt -src Spider/processed_spider/dev_src.txt -output Spider/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file Spider/${2}_pred_${3}.txt --target_file Spider/processed_spider/dev_tgt.txt --dataset $1
  cat Spider/${2}_pred_${3}.txt | sacrebleu  Spider/processed_spider/dev_tgt.txt -m bleu -b -w 4
elif [ $1 == ${Nlmaps} ]
then
  #onmt_train -config Nlmaps.yaml
  onmt_translate -model nlmaps_v2/run/${2}_model_step_${3}.pt -src nlmaps_v2/nlmaps_v2_processed/test_src.txt -output nlmaps_v2/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file nlmaps_v2/${2}_pred_${3}.txt --target_file nlmaps_v2/nlmaps_v2_processed/test_tgt.txt --dataset $1
  cat nlmaps_v2/${2}_pred_${3}.txt | sacrebleu  nlmaps_v2/nlmaps_v2_processed/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${MultiWoz} ]
then
  #onmt_train -config MultiWoz.yaml
  onmt_translate -model MultiWoz/run/${2}_model_step_${3}.pt -src MultiWoz/MultiWoz_processed/test_src.txt -output MultiWoz/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5
  python metric_test.py --prediction_file MultiWoz/${2}_pred_${3}.txt --target_file MultiWoz/MultiWoz_processed/test_tgt.txt --dataset $1
  cat MultiWoz/${2}_pred_${3}.txt | sacrebleu  MultiWoz/MultiWoz_processed/test_tgt.txt -m bleu -b -w 4
elif [ $1 == ${M2M} ]
then
  #onmt_train -config M2M.yaml
  onmt_translate -model M2M/run/${2}_model_step_${3}.pt -src M2M/m2m_gen_processed/test_src.txt -output M2M/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file M2M/${2}_pred_${3}.txt --target_file M2M/m2m_gen_processed/test_tgt.txt --dataset $1
  cat M2M/${2}_pred_${3}.txt | sacrebleu  M2M/m2m_gen_processed/test_tgt.txt -m bleu -b -w 4
else [ $1 == ${CoSQL} ]
  #onmt_train -config CoSQL.yaml
  onmt_translate -model CoSQL/run/${2}_model_step_${3}.pt -src CoSQL/processed_CoSQL_dst/dev_src.txt -output CoSQL/${2}_pred_${3}.txt -gpu 0 -verbose -beam_size 5 -min_length 3
  python metric_test.py --prediction_file CoSQL/${2}_pred_${3}.txt --target_file CoSQL/processed_CoSQL_dst/dev_tgt.txt --dataset $1
  cat CoSQL/${2}_pred_${3}.txt | sacrebleu  CoSQL/processed_CoSQL_dst/dev_tgt.txt -m bleu -b -w 4
fi
