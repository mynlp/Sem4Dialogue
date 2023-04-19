# NLmapsv2
All files pertaining to the NLmapsv2 corpus.

The corresponding website may be found here: http://www.cl.uni-heidelberg.de/statnlpgroup/nlmaps

To learn how to obtain the gold answers from the MRL formulae please follow the instructions here: https://github.com/carhaas/overpass-nlmaps

If you use this corpus in your work please cite (Lawrence & Riezler, 2018): http://www.cl.uni-heidelberg.de/statnlpgroup/nlmaps/LawrenceRiezler2018.txt

# File Endings
*en: Original English question
*mrl: Correct original semantic parse
*lin: Linearised version of the semantic parse (see Haas & Riezler, 2016)
*gold_may16: Gold answers obtained from executing the *mrl file against a OSM dump from May 2016
*loc*: Files where locations are masked as _LOCATION and POIs are masked as _POI

# Split 1: 
Training Set: *train*, 16,172 instances
Development Set: *dev*, 1,843 instances
Test Set: *test*, 10,594 instances

# Split 2:
Training Set: *log.train*, 2,000 instances (top 2k from *train* of Split 1)
Development Set: *dev*, 1,843 instances (identical to Split 1)
Test Set: *log.test*, 2,000 instances (top 2k from *test* of Split 1)
Log Set: *log.log*, 22,766 instances (remainder of *train* and *test* of Split 1)
