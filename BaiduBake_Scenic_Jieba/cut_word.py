import sys
import codecs
import os
import shutil
import jieba


def read_file_cut():
	#create path
	path = "scenic_spots\\"
	respath = "cut_word_result\\"
	if os.path.isdir(respath):
		shutil.rmtree(respath, True)
	os.makedirs(respath)

	num = 1
	while num <= 8:
		name = "%03d" % num 
		fileName = path + str(name) + ".txt"
		source = open(fileName, 'r', encoding = 'utf-8')
		line = source.readline()
		line = line.rstrip('\n')

		resName = respath + str(name) + ".txt"
		if os.path.exists(resName):
			os.remove(resName)
		result = codecs.open(resName, 'w', encoding = 'utf-8')

		while line != "":
			seglist = jieba.cut(line,cut_all=False)  #精确模式
			output = ' '.join(list(seglist))         #空格拼接
			print (output)
			result.write(output + '\r\n')
			line = source.readline()
		else:
			print ('End file: ' + str(num))
			source.close()
			result.close()
		num += 1
	else:
		print ('End All')


if __name__ == '__main__':
    read_file_cut()