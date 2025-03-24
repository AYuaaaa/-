import jieba.analyse

# 预设同义词词典
synonyms = {
    "月亮": "月", "明月": "月", "风雨": ["风", "雨"], 
    "江河": ["江", "水"], "花草": "花", "夜晚": "夜"
}

def extract_keywords(user_input):
    """ 从用户输入中提取关键词，并替换成标准标签 """
    keywords = jieba.analyse.extract_tags(user_input, topK=3)
    search_tags = []
    
    for word in keywords:
        if word in synonyms:
            search_tags.extend(synonyms[word] if isinstance(synonyms[word], list) else [synonyms[word]])
        else:
            search_tags.append(word)
    
    return search_tags

