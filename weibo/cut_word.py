import jieba

def read_file_cut():
	source_file = open('weibocontent2.txt')
	res_file = open("cut_word_result.txt", 'w')
	
	cnt = 0;
	with open('weibocontent2.txt') as source:
		content = source.read()
		seglist = jieba.cut(content,cut_all=False)  #精确模式
		output = ' '.join(list(seglist))        	#空格拼接
		with open('cut_word_result.txt', 'w') as target:
			target.write(output)

if __name__ == '__main__':
	read_file_cut()