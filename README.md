# Bio Causal Reasoning

高中生物因果推导引擎 — WorkBuddy AI Skill

## 核心能力

- **因果链推导**: 不只是"选什么"，深入理解"为什么"
- **避坑清单**: 基于9套河北+山东真题统计的6大高频陷阱
- **高频考点地图**: 教材必修一二三全部考点的真实频率排序
- **得分策略**: 河北阅卷标准的踩分点拆解
- **错题本系统**: 思维路径记录+根因分析标签+间隔重复

## 适用场景

高二起点60分，目标高考99分。适用于 WorkBuddy / Claude / 任意支持 skill 加载的 AI 助手。

## 技能层级

| 层 | 文件 | 大小 | 用途 |
|---|---|---|---|
| 完整版 | `SKILL.md` | ~18KB/455行 | 复杂大题、错题复盘 |
| 精简版 | `SKILL_COMPACT.md` | ~2KB/70行 | 日常简单选择题 |

## 快速开始

```bash
# 克隆到 WorkBuddy skills 目录
cd ~/.workbuddy/skills
git clone https://github.com/1472383516/bio-causal.git bio-causal-reasoning
```

加载 skill 后，直接发送生物题目即可触发因果推导。

## 文件结构

```
.
├── SKILL.md                 # 完整版引擎（日常答题加载）
├── SKILL_COMPACT.md         # 精简版引擎（省Token）
├── evolution_log.md         # 进化历史
├── learning_profile.md      # 学习档案（薄弱域追踪）
└── references/              # 参考数据（按需加载）
    ├── exam_strategy.md     # 题型分值/提分路径/考点地图
    ├── hebei_real_exams_bank.md   # 河北真题库
    └── shandong_real_exams_bank.md # 山东真题库
```

## 提分路径

| 阶段 | 目标 | 核心动作 |
|---|---|---|
| 60→75 | 保基础 | 背教材原话、绝对化词排除、概念对比 |
| 75→85 | 攻实验 | 三步模板、因果链训练 |
| 85→95 | 冲难题 | 多选满分、遗传大题、生态大题 |
| 95→99 | 完美发挥 | 错题本迭代、避坑指南、考前冲刺 |

## 成本优化

- 精简版比完整版省 **~85% Token**
- 响应缓存：同一问题问第二遍 → **0 API 调用**

## License

MIT — 自由使用，欢迎改进。
