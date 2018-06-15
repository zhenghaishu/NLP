from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.cluster import KMeans


if __name__ == "__main__":
	corpus = []
	for line in open('cut_word_result.txt', 'r').readlines():
		corpus.append(line.strip())
	#print (corpus)
	
	vectorizer = CountVectorizer()
	X = vectorizer.fit_transform(corpus)
	word = vectorizer.get_feature_names()	# 所有的特征词，即关键词
	#print (word)	
	#print(X)
	analyze = vectorizer.build_analyzer()  
	weight = X.toarray()  
	print(weight)
	

	import numpy as np
	import lda
	
	# 训练模型
	model = lda.LDA(n_topics = 10, n_iter = 500, random_state = 1)
	model.fit(np.asarray(weight))
	
	# 主题-词分布
	topic_word = model.topic_word_	#生成主题以及主题中词的分布
	print("topic-word:\n", topic_word)
	
	# 计算topN关键词
	topicN = 10
	for i, word_weight in enumerate(topic_word):  
		#print("word_weight:\n", word_weight)
		distIndexArr = np.argsort(word_weight)
		#print("distIndexArr:\n", distIndexArr)
		topN_index = distIndexArr[:-(topicN+1):-1]
		#print("topN_index:\n", topN_index) # 权重最大的n个
		topN_words = np.array(word)[topN_index]    
		print(u'*Topic {}\n- {}'.format(i, ' '.join(topN_words))) 
	
	# 绘制主题-词分布图
	import matplotlib.pyplot as plt  
	f, ax= plt.subplots(5, 1, figsize=(7, 7), sharex=True)  
	for i, k in enumerate([0, 2, 4, 6, 8]):         #两个主题
		ax[i].stem(topic_word[k,:1000], linefmt='b-',  
				   markerfmt='bo', basefmt='w-') 
		ax[i].set_xlim(0,1000) 
		ax[i].set_ylim(0, 0.012) 
		ax[i].set_ylabel("Prob")  
		ax[i].set_title("topic {}".format(k))  
	ax[i].set_xlabel("word")  
	plt.tight_layout()  
	plt.show()
	
    # 文档-主题分布  
	doc_topic = model.doc_topic_ 
	print("type(doc_topic): {}".format(type(doc_topic)))  
	print("shape: {}".format(doc_topic.shape)) 
	label = []        
	for i in range(10):  
		print(doc_topic[i])
		topic_most_pr = doc_topic[i].argmax()  
		label.append(topic_most_pr)  
		print("doc: {} topic: {}".format(i, topic_most_pr))  
	print("前10篇文档对应的主题列表：", label)	# 前10篇文档对应的主题列表
	
	# 绘制文档-主题分布图  
	import matplotlib.pyplot as plt    
	f, ax= plt.subplots(5, 1, figsize=(7, 7), sharex=True)    
	for i, k in enumerate([0, 1, 2, 3, 4]):    
		ax[i].stem(doc_topic[k,:], linefmt='r-',    
				   markerfmt='ro', basefmt='w-')    
		ax[i].set_xlim(-1, 10)     	#x坐标 
		ax[i].set_ylim(0, 1.1)  	#y坐标 
		ax[i].set_ylabel("Probability")    
		ax[i].set_title("Document {}".format(k))    
	ax[i].set_xlabel("Topic")  
	plt.tight_layout()  
	plt.show() 
	
	
	
	