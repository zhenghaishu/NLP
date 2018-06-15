#代码来源 https://blog.csdn.net/wy_0928/article/details/73799825

import codecs
from gensim.models import Word2Vec
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import jieba.posseg as psg
from sklearn import cross_validation
import collections
import math

textFile = 'newsTxt.txt'
keywordsFile = 'newsKw.txt'
stopwordsFile = 'stopwords.txt'


#判断给定字符（串）是否为汉字，返回True或False
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

#利用jieba切词（只保留中文词语），传入一段中文文本，结果返回该文本的切词结果（列表形式）
def cutWords(eachTxt):
	stopList = []
	for stopWord in codecs.open(stopwordsFile, 'r', 'utf-8'):
		stopList.append(stopWord.strip())
	words = psg.cut(eachTxt)
	wordsList = []
	for w in words:
		flag = True
		for i in range(len(w.word)):
			if not is_chinese(w.word[i]):
				flag = False
				break
		if flag and len(w.word) > 1:
			wordsList.append(w.word)
	return wordsList

#随机森林决策树（Random Forest）
def RF():
    clf = RandomForestClassifier()
    return clf

#传入语料库文件路径（一行为一篇文本），计算每篇文本中每个词的tfidf值
#输出形式如下：
#[[文本编号1，文本1的词语1，该词tfidf值],[文本编号2，文本2的词语1，该词tfidf值],[文本编号3，文本3的词语1，该词tfidf值]……]
def getTFIDF(fPath):
	txtNum = len(codecs.open(fPath, 'r', 'utf-8').readlines())  #语料库的文档总数
	docCount = 0
	res = []
	for eachLine1 in codecs.open(fPath, 'r', 'utf-8'):
		docCount += 1
		lineList = cutWords(eachLine1)
		#计算一个词的tf值
		wordsNum = len(lineList)    #当前文本的总词数
		cntDict = collections.Counter(lineList)
		wordList = list(cntDict.keys())
		for i in range(len(wordList)):
			temp = []
			word = wordList[i]
			wordTF = float(cntDict[word]) / float(wordsNum)
			#计算一个词的idf值
			txtContain = 0  #统计包含该词的文档总数
			for eachLine2 in codecs.open(fPath, 'r', 'utf-8'):
				if word in eachLine2:
					txtContain += 1
			wordIDF = math.log2(float(txtNum) / float(txtContain + 1))
			temp.append(docCount)
			temp.append(word)
			temp.append(wordTF*wordIDF)
			res.append(temp)
	return res

#自动提取每篇文本的关键词
def getTxtKeyWords():
	#获取整个语料库所有文档中每个词语的tfidf权重
	wordTFIDF = getTFIDF(textFile)
	#数据结构化
	#将文本及其对应的关键词写入本地内存
	#txtList是一维数组，用于存储文本
	#kwList是二维数组，用于存储关键词，其内每个小数组都是一篇文本的关键词，与txtList一一对应
	txtList, kwList = [], []
	wholeTxt = ''   #语料库所有文本合在一起
	for eachTxt1 in codecs.open(textFile, 'r', 'utf-8'):
		wholeTxt += eachTxt1.strip()
		txtList.append(eachTxt1.strip())
		
	for eachLine1 in codecs.open(keywordsFile, 'r', 'utf-8'):
		lineList1 = eachLine1.strip().split(' ')
		tempList1 = []
		for i in range(len(lineList1)):
			tempList1.append(lineList1[i].strip())
		kwList.append(tempList1)

	#读取整个语料库中所有文本，切词，做word2vec，生成词向量
	wholeWords = cutWords(wholeTxt) #语料库所有词语
	#建模
	model = Word2Vec([wholeWords], min_count = 1)
	#存储语料库中每个词语对应的词向量
	wordVecD = {}
	uniqWords = list(frozenset(wholeWords))

	for i in range(len(uniqWords)):
		word = uniqWords[i]
		wordVecD[word] = model[word]
	reList, accuList = [], []   #用于存储每篇文本的召回率和准确率
	clf = RF()
	#依次遍历每一篇文本
	for i in range(len(txtList)):
		nowDocKw = kwList[i]    #当前文本的原始关键词列表
		nowDocWords = cutWords(txtList[i])  #当前文本的所有词语
		docWordV, docWordL = [], []
		for j in range(len(nowDocWords)):
			docWord = nowDocWords[j]
			#生成每篇文本的词向量矩阵，其中一行为一个词向量
			docWordV.append(list(wordVecD[docWord]))
			
			#生成每篇文本的类标向量，其中一个元素对应一个词语的类标，关键词类标1，非关键词类标0
			if docWord in nowDocKw:
				docWordL.append(1)
			else:
				docWordL.append(0)

		docWordM = np.array(docWordV)

		#对当前文本词语做关键词和非关键词的二分类（k折交叉验证）
		preLabel = cross_validation.cross_val_predict(clf, docWordM, docWordL, cv = 5)  #预测样本类别

		sKW = set() #用于存储当前文本预测出来的关键词并去重
		for r in range(len(preLabel)):
			if preLabel[r] == 1:
				sKW.add(nowDocWords[r])
		predictKw = list(sKW)   #预测的关键词
		#计算原始标记关键词和预测关键词之间的交集，即预测中多少个
		countKw = 0
		for k1 in range(len(nowDocKw)):
			for k2 in range(len(predictKw)):
				if nowDocKw[k1] == predictKw[k2]:
					countKw += 1
					break

		#计算召回率
		recallRate = float(countKw) / float(len(nowDocKw))
		#计算准确率
		accuracyRate = float(countKw) / float(len(predictKw) + 1)

		reList.append(recallRate)
		accuList.append(accuracyRate)
		#获取预测关键词的tfidf权重，根据权重降序排列输出预测关键词
		preKwTFIDF = []
		for p in range(len(predictKw)):
			preWord = predictKw[p]
			for t in range(len(wordTFIDF)):
				if wordTFIDF[t][0] == i + 1 and wordTFIDF[t][1] == preWord:
					preKwTFIDF.append(wordTFIDF[t][2])
					break

		wordTFIDFD = {}
		for ww in range(len(preKwTFIDF)):
			wordTFIDFD[preKwTFIDF[ww]] = predictKw[ww]
		preKwTFIDF.sort(reverse = True)
		print('---------第' + str(i + 1) + '篇文本结果---------')
		print('【一】原始标记的关键词')
		print(nowDocKw)
		print('【二】预测关键词按照tfidf权重降序排列')
		for www in range(len(preKwTFIDF)):
			print(wordTFIDFD[preKwTFIDF[www]], preKwTFIDF[www])
		print('【三】预测中几个关键词')
		print(countKw)
	#输出评估结果
	print('=======================================================================')
	print('Mean Recall Rate:', float(sum(reList)) / float(len(reList)))
	print('Mean Accuracy Rate:', float(sum(accuList)) / float(len(accuList)))

if __name__ == '__main__':
    getTxtKeyWords()