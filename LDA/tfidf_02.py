from sklearn import feature_extraction    
from sklearn.feature_extraction.text import TfidfTransformer    
from sklearn.feature_extraction.text import CountVectorizer
  

if __name__ == "__main__": 
	corpus = []

	#读取预料 一行预料为一个文档 
	for line in open('test.txt', 'r').readlines():
		#print line
		corpus.append(line.strip())
	#print (corpus)#将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频  
	
	vectorizer = CountVectorizer()  
	  
	#该类会统计每个词语的tf-idf权值  
	transformer = TfidfTransformer()  
	#print(transformer)
	  
	#第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus)) 
	#print(tfidf)
	  
	#获取词袋模型中的所有词语   
	word = vectorizer.get_feature_names()  
	print(word)
	weight = tfidf.toarray()  
	print(weight)