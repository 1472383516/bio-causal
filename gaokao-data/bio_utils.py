"""Claw 项目公共工具函数"""
import json
import os
import re

# 生物知识点分类关键词
TOPIC_KEYWORDS = {
    "细胞分子组成": ["元素组成", "蛋白质", "核酸", "糖类", "脂质", "水", "无机盐", "氨基酸", "核苷酸"],
    "细胞结构功能": ["细胞膜", "细胞器", "线粒体", "叶绿体", "内质网", "高尔基体", "核糖体", "溶酶体", "液泡", "细胞核"],
    "跨膜运输": ["跨膜", "主动运输", "协助扩散", "自由扩散", "载体", "通道", "渗透"],
    "酶": ["酶", "活化能", "ATP", "ADP", "催化"],
    "光合作用": ["光合", "光反应", "暗反应", "叶绿素", "C3", "C4"],
    "呼吸作用": ["呼吸", "有氧", "无氧", "丙酮酸", "线粒体"],
    "遗传规律": ["遗传", "孟德尔", "基因分离", "自由组合", "测交"],
    "基因与染色体": ["基因表达", "转录", "翻译", "DNA复制", "突变", "染色体"],
    "神经体液调节": ["神经", "激素", "胰岛素", "反馈调节"],
    "免疫调节": ["免疫", "抗体", "抗原", "淋巴细胞"],
    "生态学": ["种群", "群落", "生态系统", "食物链", "演替"],
}


def clean_text(text):
    """清理题干文本：去除题号前缀、分数标记、多余空白"""
    text = re.sub(r'^\d+[．.、]\s*', '', text.strip())
    text = re.sub(r'^\（\s*\d+\s*分\s*\）', '', text)
    text = re.sub(r'[\s　]+', ' ', text)
    return text.strip()


def classify_by_topic(text):
    """按关键词分类题目所属知识域"""
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[topic] = score
    if not scores:
        return "其他"
    return max(scores, key=scores.get)


def read_jsonl(filepath):
    """逐行读取 JSONL 文件，返回 (line_index, dict) 生成器"""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def get_markdown_path(week_str="5月-1周"):
    """获取 bio-vault 目录下的 markdown 笔记路径"""
    base = os.path.dirname(os.path.abspath(__file__))
    vault_dir = os.path.join(base, "bio-vault")
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir)
    return os.path.join(vault_dir, f"{week_str}.md")
