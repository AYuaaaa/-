import pymysql
#导入know 
from know import extract_keywords

def search_poetry(keywords):
    """ 在多个表中查询匹配的诗句，返回最相关的一个结果 """
    conn = pymysql.connect(host="localhost", user="root", password="021207", database="poem", charset="utf8mb4")
    cursor = conn.cursor()
    
    # 动态生成查询条件
    conditions = " OR ".join([f"tags LIKE '%{tag}%'" for tag in keywords])
    
    # 查询多个表，使用 UNION 合并结果，并根据匹配的关键词数量排序
    query = f"""
        SELECT title, tags, content, 
               (LENGTH(tags) - LENGTH(REPLACE(tags, '{keywords[0]}', ''))) AS match_count
        FROM caocao WHERE {conditions}
        UNION
        SELECT title, tags, content, 
               (LENGTH(tags) - LENGTH(REPLACE(tags, '{keywords[0]}', ''))) AS match_count
        FROM chuci WHERE {conditions}
        UNION
        SELECT title, tags, content, 
               (LENGTH(tags) - LENGTH(REPLACE(tags, '{keywords[0]}', ''))) AS match_count
        FROM shuimotangshi WHERE {conditions}
        ORDER BY match_count DESC
        LIMIT 1
    """
    
    cursor.execute(query)
    result = cursor.fetchone()  # 只获取一条结果
    
    cursor.close()
    conn.close()
    
    if result:
        return result[:3]  # 只返回标题、作者和内容
    else:
        return "未找到匹配的诗句"