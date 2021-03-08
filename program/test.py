import math
import jieba.analyse
import time
words2='《地球引力》（Gravity）编剧，著名导演阿方索·夸隆（Alfonso Cuarón）之子乔纳斯·夸隆（Jonás Cuarón）日前确认将执导并编剧筹划已久的未来版“佐罗”电影——《Z》（Z）。该片由Lantica Media和Sobini Films联合摄制，Pantelion Films负责海外销售，影片计划今年夏天在多米尼加共和国Pinewood片场拍摄。'
words='恐怖/奇幻/冒险'
print(jieba.analyse.extract_tags(words,topK=20,withWeight=True))
print(jieba.analyse.textrank(words))
print(jieba.analyse.extract_tags(words2,topK=20,withWeight=True))
test="fsf"
print(test.split('/n')[0])