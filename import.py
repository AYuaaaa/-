import json
import pymysql
import jieba

# 连接 MySQL
conn = pymysql.connect(host="localhost", user="root", password="021207", database="poem", charset="utf8mb4")
cursor = conn.cursor()

# 读取 JSON 文件
with open("chinese-poetry\蒙学\baijiaxing.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 预设常见的飞花令关键词
common_tags = {"春","花","月","风","山","水","云","雨","夜","人","心","酒","江","雪","柳","草","鸟","梦","愁","情","红","黄","绿","青","白","黑","紫","蓝","金","银","灰","粉","橙","碧","赤","丹","翠","苍","玄","朱"}

# 解析 JSON 并导入数据库
for poem in data:
    title = poem["title"]
    author = poem["author"]#诗人
    content = "\n".join(poem["paragraphs"])  # 拼接诗句

    # **方式 1：使用关键词匹配**
    words = set(jieba.cut(content))  # 分词
    tags = list(words & common_tags)  # 只保留常见关键词

    # **方式 2：使用 NLP 自动提取关键词（更智能，但可能不准）**
    #tags = jieba.analyse.extract_tags(content, topK=5)

    # 插入数据库 哪一个表
    cursor.execute(
        "INSERT INTO mengxue ( title, author,content, tags) VALUES (%s,%s,%s,%s)",
        ( title,author,content, json.dumps(tags, ensure_ascii=False))  # 存 JSON
    )

conn.commit()
cursor.close()
conn.close()

print("✅ 诗词数据导入完成！")


