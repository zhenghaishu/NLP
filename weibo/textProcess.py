fread = open('weibocontent.txt')
fwrite = open('weibocontent2.txt', 'w')
	
try:
	for line in fread:
		text = line.strip()
		if("" == text):
			continue
		if(4 >= len(text)):	#第几条微博，总共5000多条，所以不超过四位数
			continue
		if(-1 != text.find("转发理由")):
			continue
		if(-1 != text.find("原图")):
			continue
			
		pos1 = 0
		if("发布了" in text or "转发了" in text):
			if(-1 != text.find("：")):
				pos1 = text.find("：") + 1
			elif(-1 != text.find(":")):
				pos1 = text.find(":") + 1
		pos2 = len(text)
		if(-1 != text.find("http")):
			pos2 = text.find("http")		
		elif(-1 != text.find("全文")):
			pos2 = text.find("全文")
		elif (-1 != text.find("赞")):
			pos2 = text.find("赞")
		elif(-1 != text.find("[组图共")):
			pos2 = text.find("[组图共")
		
		content = text[pos1 : pos2]
		fwrite.write(content+'\n')
finally:
	fread.close()
	fwrite.close()