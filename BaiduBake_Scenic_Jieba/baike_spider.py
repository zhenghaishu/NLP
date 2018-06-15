import os
import time
import codecs
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")


def getInfoBox(spotname, filename):
	try:
		print(filename)
		info = codecs.open(filename,'w','utf-8')
			
		driver.get("http://baike.baidu.com/")
		elem_input = driver.find_element_by_xpath("//form[@id='searchForm']/input")
		time.sleep(2)
		spotname = spotname.rstrip('\n')		# 景点名称是从文件中读取的，含有换行符（最后一行的景点名称可能不含护身符）
		elem_input.send_keys(spotname)
		elem_input.send_keys(Keys.RETURN)
		
		info.write(spotname + '\r\n')  		# codecs不支持'\n'换行
		print (driver.current_url)
		print (driver.title)
		
		elem_value = driver.find_elements_by_xpath("//div[@class='lemma-summary']/div")
		for value in elem_value:
			print (value.text)
			info.writelines(value.text + '\r\n')
		time.sleep(2)
		info.close()

	except Exception as e:  
		print ("Error: ", e)
	finally:
		pass
		

def main():
	# 创建路径
	path = "scenic_spots\\"
	if os.path.isdir(path):
		shutil.rmtree(path, True)
	os.makedirs(path)
	
	source = open("scenic_spots_5A.txt", 'r')
	num = 1
	for scenicspot in source:
		name = "%03d" % num
		fileName = path + str(name) + ".txt"
		getInfoBox(scenicspot, fileName)
		num += 1
	print ('End Read Files!')
	time.sleep(10)
	
	source.close()
	driver.close()

if __name__ == '__main__':
	main()
