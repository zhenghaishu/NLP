from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


if __name__ == "__main__":
	corpus = []
	for line in open('cut_word_result.txt', 'r').readlines():
		corpus.append(line.strip())
	#print (corpus)
	
	vectorizer = CountVectorizer()
	transformer = TfidfTransformer()  
	#第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  
	word = vectorizer.get_feature_names()	# 所有的特征词，即关键词
	#print (word)	
	weight = tfidf.toarray()  
	print(len(weight))
	print(len(weight[0]))
	print(weight[0:10, 0:30])
	print ('Features length: ' + str(len(word))) 
	
	####################聚类####################
	SSE = []
	for k in range(2, 21, 2):
		clf = KMeans(n_clusters = k)  
		s = clf.fit(weight)  
		print ("s:\n", s)  

		#中心点  
		print("center len:\n", len(clf.cluster_centers_))
		print("center len of each:\n", len(clf.cluster_centers_[0]))
		print("centers:\n", clf.cluster_centers_[0:20])  
		  
		#每个样本所属的簇  
		print("labels len:\n", len(clf.labels_))
		print(clf.labels_[0:20])  
		i = 0  
		while i <= len(clf.labels_):  
			print (i, clf.labels_[i])  
			i += 1
			if(50 == i):
				break

		#用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  
		print("inertia:\n", k, clf.inertia_)  
		SSE.append(clf.inertia_)
	
	x = range(2, 21, 2)
	plt.xlabel('k')
	plt.ylabel('SSE')
	plt.plot(x, SSE, 'o-')
	plt.show()
