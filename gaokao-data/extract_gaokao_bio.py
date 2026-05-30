"""从 gaokao 数据集按薄弱知识域提取生物真题"""
import json
import os
from collections import defaultdict

BASE = r"E:\workbuddy\Claw\gaokao-dataset\dataset\生物"
OUT = r"E:\workbuddy\Claw\gaokao_bio_薄弱域真题.json"

# 薄弱域关键词映射
DOMAINS = {
    "酶_抑制剂": ["酶", "抑制剂", "竞争性", "非竞争性", "活性部位", "活化能", "催化"],
    "脂质_元素组成": ["脂质", "脂肪", "磷脂", "固醇", "脂肪酸", "元素组成", "C、H、O", "不饱和"],
    "群落_生态系统": ["群落", "生态系统", "种群", "演替", "结构层次", "食物链", "物种组成"],
    "跨膜运输": ["跨膜", "主动运输", "协助扩散", "自由扩散", "载体蛋白", "通道蛋白", "协同转运", "离子泵", "Na⁺/K⁺"],
    "光合_呼吸": ["光合", "呼吸", "ATP", "光反应", "暗反应", "有氧呼吸", "叶绿体", "线粒体", "CO₂"],
    "蛋白质_分选": ["分泌蛋白", "内质网", "高尔基体", "囊泡", "信号肽", "蛋白质合成", "核糖体"],
}

results = defaultdict(list)
total = 0

for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith(".jsonl"):
            continue
        fpath = os.path.join(root, f)
        year_dir = os.path.relpath(root, BASE)
        with open(fpath, "r", encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                line = line.strip()
                if not line:
                    continue
                try:
                    q = json.loads(line)
                except json.JSONDecodeError:
                    continue
                total += 1

                # 拼接题目+选项+解析全文检索
                full_text = json.dumps(q, ensure_ascii=False)

                for domain, keywords in DOMAINS.items():
                    if any(kw in full_text for kw in keywords):
                        results[domain].append({
                            "source": f"{year_dir}/{f}",
                            "question": q
                        })
                        break  # 一道题只归到一个域

# 输出统计
print(f"总题目数: {total}")
for domain, items in sorted(results.items()):
    print(f"  {domain}: {len(items)} 道")

# 每个域最多保留 10 道去重
deduped = {}
for domain, items in results.items():
    seen = set()
    unique = []
    for it in items:
        text = json.dumps(it["question"], ensure_ascii=False, sort_keys=True)
        h = hash(text)
        if h not in seen:
            seen.add(h)
            unique.append(it)
    deduped[domain] = unique[:10]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({d: items for d, items in deduped.items() if items},
              f, ensure_ascii=False, indent=2)

print(f"\n入库: {OUT}")
for d, items in deduped.items():
    print(f"  {d}: {len(items)} 道")
