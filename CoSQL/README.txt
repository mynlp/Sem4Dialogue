This folder contains the CoSQL training and dev data sets for our EMNLP 2019 paper "CoSQL: A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases".

It contains the following files:

- cosql_all_info_dialogs.json: the CoSQL dataset of raw dialogs between SQL experts and DB users (MTurkers). This file contains all info for all 3 tasks.
- tables.json: the file including all DB schema info such as table and column names.
- sql_state_tracking/: contains tain and dev data for the SQL-grounded dialog state tracking task.
- system_response_generation/: contains tain and dev data for the system response generation task.
- user_intent_prediction/: contains tain and dev data for the user intent prediction task.
- database/: each folder for each database which contains the [db_name].sqlite and schema.sql files.
- README.txt

For the format of each JSON file, please refer to our Github page: https://github.com/taoyds/cosql.
For the details of the CoSQL, A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases, please refer to our task page: https://yale-lily.github.io/cosql


If you use the dataset, please cite the following papers:

@InProceedings{yu2019cosql,
  author =  {Tao Yu and Rui Zhang and He Yang Er and Suyi Li and Eric Xue and Bo Pang and Xi Victoria Lin and Yi Chern Tan and Tianze Shi and Zihan Li and Youxuan Jiang and Michihiro Yasunaga and Sungrok Shim and Tao Chen and Alexander Fabbri and Zifan Li and Luyao Chen and Yuwen Zhang and Shreya Dixit and Vincent Zhang and Caiming Xiong and Richard Socher and Walter Lasecki and Dragomir Radev},
  title =   {CoSQL: A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases},
  year =    {2019},
  booktitle =   {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and 9th International Joint Conference on Natural Language Processing},
  publisher = {Association for Computational Linguistics},
}

@inproceedings{Yu&al.18c,
  title     = {Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task},
  author    = {Tao Yu and Rui Zhang and Kai Yang and Michihiro Yasunaga and Dongxu Wang and Zifan Li and James Ma and Irene Li and Qingning Yao and Shanelle Roman and Zilin Zhang and Dragomir Radev}
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
  address   = "Brussels, Belgium",
  publisher = "Association for Computational Linguistics",
  year      = 2018
}


Reference links:

CoSQL task link: https://yale-lily.github.io/cosql
CoSQL Github page: https://github.com/taoyds/cosql
SParC task link: https://yale-lily.github.io/sparc
SParC Github page: https://github.com/taoyds/sparc
Spider task link: https://yale-lily.github.io/spider
Spider Github page: https://github.com/taoyds/spider