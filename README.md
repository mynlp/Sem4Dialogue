# Semantic for Dialogue
This is the repository for the paper Syntactic and Semantic Uniformity for Semantic Parsing and Task-Oriented Dialogue Systems

## Models
For now, the implemented models are Transformer model and LSTM with Copy mechanism which you can use directly to get some initial results. However, the key idea is the paper proposed a framework to unify different semantics of different machine-readable formats.
![avatar](emnlp_page-0001.jpg)
If you are interested in this paper, you can refer to the [paper](https://aclanthology.org/2022.findings-emnlp.60/) for detail.
## Datasets
Current datasets covered in the repository contains:  
1. Semantic Parsing
  - GeoQuery-FunQL Version
  - GeoQuery-SQL Version
  - SCAN-Si & Scan-Len
  - SParC
  - Spider
  - NLmaps v2
  - ATIS-SQL Version
2. Task-Oriented Dialogue
  - TreeDST
  - SMCalFlow
  - CoSQL
  - MultiWoz
  - M2M
  - DSTC2

Some datasets are beyond the limit of GitHub's storage, so I uploaded some of the datasets in the [Google Drive](https://drive.google.com/file/d/1Bxm29zjtLkLiuzMNHMUAIWmOSvBWlGu6/view?usp=sharing), you could download these datasets via this link and unzip it, then place each datasets to corresponding folder. Since some datasets has been updated, if you downloaded these datasets before 2022.02.23, you should redownload it.

## How to run the code

### File Introdocution
Each dataset folder all contains these necessary files:
  - processe_xxx.py this is the pre-process code of each dataset, since I have processed every datasets, you may not need to use this.
  - processed_xxx folder, this folder contained pre-processed datasets.
  - vocab_xxx folder, this folder contains the vocabulary file of each datasets
  - other folders besides above folders are mainly raw data of each datasets.  

Each dataset correspond a YAML configuration file like SCAN.yaml or GeoQuery.yaml, these files specify things like the parameter setting and model setting of each dataset, this YAML file is based on the [OpenNMT package](https://github.com/OpenNMT/OpenNMT-py), you should refer to this package to know how to use a YAML configuration file.

The utils folder contains necessary metric codes, which you could consider is a package of this project. The metric_test.py is built upon this folder. Current metrics contains following:
  - Word Level Exact Match
  - Sentence Level Exact Match
  - BLEU Score, BLEU metric is built upon [screbleu package](https://github.com/mjpost/sacrebleu), you should also install this package.

This repository also supports SQL execution evaluation, which is a part of the [test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval), but the code of  original repository is somehow problematic, so I modified some of the codes, therefore you should not use the code in that repository. However, to run the SQL evaluation code, you need to download SQL database for different datasets, which is at [Google Drive](https://drive.google.com/file/d/1mkCx2GOFIqNesD4y8TDAO1yX1QZORP5w/view). Download this database and unzip it into the sql_eval directory, for detail on how to use this code, please refer to the original repository. This repository is also the official metric repository for CoSQL, Sparc and Spider datasets.

For the official metric of SMCalFlow dataset, you should refer to its [repository](https://microsoft.github.io/task_oriented_dialogue_as_dataflow_synthesis/) for the detail about how to evaluate it with official metric.

train.sh contains the training script, it contains the following functions:
  - train the model
  - translate given source language
  - evaluate the model output

### Running the code
It is relatively easy to run the code, for example if you want to run a experiment in GeoQuery using Transformer and evaluate using the model trained with 10000 steps, you should use following code:

```sh train.sh GeoQuery Transformer 10000```

GeoQuery specifies the target task you want to run, for the acceptable parameter of take, you should refer to train.sh for detail.

Transformer specifies the target model you want to train, however, this parameter does not automatically choose model to run. Before you train the model, you should modify the YAML file of each task to change the model selection. For example, if you want to use LSTM model in GeoQuery, you should comment the Transformer setting in the GeoQuery.YAML and uncomment the LSTM setting. Otherwise, even if you input ```sh train.sh GeoQuery LSTM 10000```, it will still train a Transformer model. For detail about the YAML configuration, you should refer to the [OpenNMT](https://github.com/OpenNMT/OpenNMT-py) for detail.

Last numeric parameter specifies the model of particular step as the evaluation model. For the above example program, it uses Transformer trained at 10000 step as the model for evaluation. It will automatically translate the test file and evaluate the translated test file with the gold file.The results will be reported after the evaluation is finished. However, the automatic evaluation only supports Word EM, Sent EM and BLEU score, if you want to execute SQL query in database, refer to [test-suite-sql-eval](https://github.com/taoyds/test-suite-sql-eval) for detail, in conclusion, the SQL execution accuracy is not automatically reported, you should run it by yourself.

### Regarding Language Production
To achieve language rewriting into proposed format, you need to have the following additional packages:
This refers to the code `sem4diag_rewriting.py`
`mo_sql_parsing` for SQL language parsing
`pyparsing` for nested parenthesis Parsing
`anytree` and `treelib` for tree representation
`onmt` for some default use tokens  
For new task processing, you need to add your own parsing code to you data and add new code to the tree linearization. However, the tree linearization may not require to be rewritten, this is mostly case by case. This choice largely depends on the nature of your data. Therefore, use the code in the repository in a careaful manner. Since the code may not apply to your format and you may need to write your own.
