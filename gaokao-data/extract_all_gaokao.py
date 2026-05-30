"""将 gaokao 生物数据集288道题全部提取入库，按年份+卷型+题型+知识域多维分类"""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(r"E:\workbuddy\Claw\gaokao-dataset\dataset\生物")
OUT = Path(r"E:\workbuddy\Claw\gaokao_bio_全题库.json")

# 知识域关键词（全量覆盖，不再只筛6个域）
KNOWLEDGE_MAP = {
    "细胞分子组成": ["元素组成", "C、H、O", "水", "无机盐", "蛋白质", "核酸", "糖类", "脂质", "脂肪", "磷脂", "固醇", "氨基酸", "核苷酸", "脱水缩合"],
    "细胞结构功能": ["细胞膜", "细胞器", "线粒体", "叶绿体", "内质网", "高尔基体", "核糖体", "溶酶体", "液泡", "中心体", "细胞核", "核膜", "细胞壁"],
    "跨膜运输": ["跨膜", "主动运输", "协助扩散", "自由扩散", "载体", "通道", "离子泵", "渗透", "质壁分离", "选择透过性", "胞吐", "胞吞"],
    "酶与ATP": ["酶", "活化能", "ATP", "ADP", "催化", "抑制剂", "竞争", "辅酶"],
    "光合作用": ["光合", "光反应", "暗反应", "卡尔文", "C3", "C4", "叶绿素", "类囊体", "Rubisco", "CO₂固定", "碳反应"],
    "呼吸作用": ["呼吸", "有氧", "无氧", "糖酵解", "丙酮酸", "酒精发酵", "乳酸发酵", "线粒体", "[H]", "氧化分解"],
    "细胞增殖分化": ["有丝分裂", "减数分裂", "细胞周期", "分化", "干细胞", "凋亡", "衰老", "癌变"],
    "遗传规律": ["遗传", "孟德尔", "基因分离", "自由组合", "显性", "隐性", "纯合", "杂合", "测交", "表现型", "基因型"],
    "基因与染色体": ["基因表达", "转录", "翻译", "中心法则", "DNA复制", "RNA", "密码子", "反密码子", "突变", "重组", "染色体变异"],
    "神经体液调节": ["神经", "突触", "反射", "激素", "胰岛素", "血糖", "甲状腺", "反馈调节", "体温", "渗透压"],
    "免疫调节": ["免疫", "抗体", "抗原", "淋巴细胞", "T细胞", "B细胞", "浆细胞", "记忆", "疫苗", "特异性", "非特异性"],
    "生态学": ["种群", "群落", "生态系统", "食物链", "食物网", "演替", "环境容纳量", "J型", "S型", "物种组成", "生产者", "消费者", "分解者"],
    "植物激素": ["生长素", "赤霉素", "脱落酸", "乙烯", "向光性", "顶端优势"],
    "基因工程": ["基因工程", "转基因", "限制酶", "DNA连接酶", "载体", "PCR", "重组DNA", "农杆菌"],
    "实验设计": ["实验", "对照", "变量", "观察", "检测", "显微镜"],
    "细胞工程": ["植物组织培养", "植物体细胞杂交", "动物细胞培养", "单克隆抗体", "胚胎移植", "核移植"],
}

def classify(text):
    """返回匹配到的知识域列表"""
    matched = []
    for domain, keywords in KNOWLEDGE_MAP.items():
        if any(kw in text for kw in keywords):
            matched.append(domain)
    return matched if matched else ["其他"]

# 全量收集
all_questions = []
stats = {"total": 0, "by_year": defaultdict(int), "by_type": defaultdict(int), "by_domain": defaultdict(int)}

for jsonl_file in sorted(BASE.rglob("*.jsonl")):
    year_dir = jsonl_file.parent.relative_to(BASE)
    year = year_dir.parts[0] if year_dir.parts else "未知"

    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                q = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            full_text = json.dumps(q, ensure_ascii=False)
            domains = classify(full_text)

            entry = {
                "year": year,
                "paper": str(year_dir),
                "type": q.get("question_type", jsonl_file.stem),
                "question": q.get("question", ""),
                "answer": q.get("answer", ""),
                "analysis": q.get("analysis", ""),
                "score": q.get("score", 0),
                "domains": domains
            }
            all_questions.append(entry)
            stats["total"] += 1
            stats["by_year"][year] += 1
            stats["by_type"][q.get("question_type", jsonl_file.stem)] += 1
            for d in domains:
                stats["by_domain"][d] += 1

# 去重（按题目文本）
seen = set()
unique = []
for q in all_questions:
    key = q["question"][:100]
    if key not in seen:
        seen.add(key)
        unique.append(q)

# 输出
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"stats": {k: dict(v) if isinstance(v, defaultdict) else v for k, v in stats.items()},
               "questions": unique}, f, ensure_ascii=False, indent=2)

print("全量提取完成")
print(f"  原始: {stats['total']} 道, 去重后: {len(unique)} 道")
print("\n按年份:")
for y, c in sorted(stats["by_year"].items()):
    print(f"  {y}: {c}道")
print("\n按题型:")
for t, c in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}道")
print("\n按知识域 (TOP10):")
for d, c in sorted(stats["by_domain"].items(), key=lambda x: -x[1])[:10]:
    print(f"  {d}: {c}道")
print(f"\n输出: {OUT}")
