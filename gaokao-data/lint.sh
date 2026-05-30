#!/bin/bash
# 代码质量一键检查
# 用法: bash lint.sh

echo "🔍 代码质量检查..."
echo ""

PYTHON="C:/ProgramData/WorkBuddy/chromium-env/6nqz0u/.workbuddy/binaries/python/versions/3.13.12/python.exe"

echo "=== Python (pylint) ==="
$PYTHON -m pylint --rcfile=.pylintrc \
    extract_gaokao_bio.py \
    extract_all_gaokao.py \
    analyze_papers.py \
    rebuild_exam_bank.py \
    clean_exam_bank.py \
    gen_exam_js.py \
    replace_banks.py \
    2>&1 | tail -5

echo ""
echo "=== 大文件检查 ==="
for f in $(ls -S *.html *.json 2>/dev/null | head -5); do
    size=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null)
    if [ "$size" -gt 100000 ]; then
        echo "⚠️  $f: $((size/1024))KB (>100KB)"
    else
        echo "✅ $f: $((size/1024))KB"
    fi
done

echo ""
echo "=== 重复代码检测 (jscpd) ==="
if command -v npx &> /dev/null; then
    npx jscpd --min-lines 5 --min-tokens 50 --ignore "gaokao-dataset,optimization-demo,skills" . 2>&1 | grep -E "Clones found|detection"
else
    echo "  jscpd 未安装，跳过"
fi

echo ""
echo "✅ 检查完成"
