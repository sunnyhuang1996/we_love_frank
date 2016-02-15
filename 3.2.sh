#!/bin/sh

python buildarff0.py train.twt train.arff 2500
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt
python buildarff0.py train.twt train.arff 3000
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt
python buildarff0.py train.twt train.arff 3500
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt
python buildarff0.py train.twt train.arff 4000
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt
python buildarff0.py train.twt train.arff 4500
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt
python buildarff0.py train.twt train.arff
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff -o >> 3.2output.txt