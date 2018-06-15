import jieba

# 去除停用词
stopwords = {}.fromkeys(['的', '包括', '等', '是'])
text = "故宫的著名景点包括乾清宫、太和殿和午门等。其中乾清宫非常精美，午门是紫禁城的正门。"
# 精确模式
segs = jieba.cut(text, cut_all=False)
final = ''
for seg in segs:
    if seg not in stopwords:
            final += seg
print (final)

seg_list = jieba.cut(final, cut_all=False)
print ("/ ".join(seg_list))
