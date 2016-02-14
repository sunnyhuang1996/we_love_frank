#!/bin/sh
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train3.arff -T vali3.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train4.arff -T vali4.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train5.arff -T vali5.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train6.arff -T vali6.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train7.arff -T vali7.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train8.arff -T vali8.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train9.arff -T vali9.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train10.arff -T vali10.arff >> 3.4output.txt


java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train1.arff -T vali1.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train2.arff -T vali2.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train3.arff -T vali3.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train4.arff -T vali4.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train5.arff -T vali5.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train6.arff -T vali6.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train7.arff -T vali7.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train8.arff -T vali8.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train9.arff -T vali9.arff >> 3.4output.txt
java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 —S -o -t train10.arff -T vali10.arff >> 3.4output.txt

