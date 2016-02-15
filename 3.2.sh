#!/bin/sh

python buildarff0.py train.twt train.arff 500
sh /u/cs401/WEKA/infogain.sh > 3.2output.txt
python buildarff0.py train.twt train.arff 1000
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 1500
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 2000
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 2500
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 3000
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 3500
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 4000
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 4500
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff 5000
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt
python buildarff0.py train.twt train.arff
sh /u/cs401/WEKA/infogain.sh >> 3.2output.txt