import os
import re
from pathlib import Path

# Configuration
RAW_BASE = Path(r"C:\Users\Long\Documents\amtb\amtb\doc\開示問答與活動\學佛答問")
WIKI_BASE = Path(r"C:\Users\Long\Documents\amtb\amtb\wiki\開示問答與活動")
CONCEPTS = [
    "一乘", "三皈依", "三福", "五戒", "佛教與宗教", "佛陀教育", "六和敬", "六度", "十善",
    "四十八願", "四弘誓願", "念佛", "普賢十大願王", "菩提心", "阿彌陀佛", "信願行",
    "極樂世界", "一心不亂", "帶業往生", "一門深入", "持名念佛", "看破放下", "三昧",
    "華嚴", "善財童子五十三參", "楞嚴", "法華", "因果", "般若", "師承", "孝道"
]

CODES = [
    "21-335", "21-336", "21-338", "21-339", "21-342", "21-343", "21-346", "21-348",
    "21-350", "21-352", "21-356", "21-358", "21-363", "21-366", "21-368", "21-369",
    "21-371", "21-374", "21-375", "21-378", "21-383", "21-388", "21-389", "21-390",
    "21-391", "21-392", "21-393", "21-395", "21-396", "21-397", "21-400", "21-402",
    "21-404", "21-405", "21-406", "21-409", "21-414", "21-415", "21-416", "21-417",
    "21-418", "21-419", "21-422", "21-426", "21-431", "21-432", "21-437", "21-439",
    "21-442", "21-444", "21-447", "21-448", "21-452", "21-453", "21-454", "21-455",
    "21-474", "21-479", "21-482", "21-483", "21-491", "21-493", "21-498", "21-499",
    "21-505", "21-507", "21-509", "21-659", "21-699", "21-741", "32-236"
]

def extract_metadata(first_line):
    """Extract title, date, place, pages from first line."""
    line = first_line.strip()
    
    # Split by multiple spaces (full-width or regular)
    parts = re.split(r'\s{2,}', line)
    
    title = parts[0] if parts else ""
    
    # Extract pages from （共N集） or （第一集） etc.
    pages_match = re.search(r'[（(]共?([^）)]+)集[）)]', title)
    pages = pages_match.group(1) if pages_match else "一"
    if "共" in title and pages_match:
        pages = "共" + pages + "集"
    elif "第一集" in title:
        pages = "一"
    
    # Remove the pages part from title
    title = re.sub(r'\s*[（(]共?[^）)]+集[）)]', '', title)
    
    # Date and place
    date = ""
    place = ""
    if len(parts) >= 3:
        date = parts[2] if parts[2] != "—" else ""
    if len(parts) >= 4:
        place = parts[3] if parts[3] != "—" else ""
    
    # Clean up date format
    if date:
        date = date.replace(".", "/")
    
    return title.strip(), date.strip(), place.strip(), pages.strip()

def generate_summary_and_key_points(content, code):
    """Generate summary and key points from content."""
    # Extract key teachings - look for patterns like "答：" or key Buddhist terms
    key_points = []
    
    # Look for answer sections
    answers = re.findall(r'答[：:]\s*([^問\n]{50,300})', content)
    for ans in answers[:5]:
        ans = ans.strip().replace('　', ' ')
        ans = re.sub(r'\s+', ' ', ans)
        if len(ans) > 30:
            key_points.append(ans[:150] + ("..." if len(ans) > 150 else ""))
    
    # If not enough, look for other patterns
    if len(key_points) < 3:
        # Look for sentences with key Buddhist terms
        sentences = re.split(r'[。！？]', content)
        keywords = ['念佛', '往生', '阿彌陀佛', '極樂世界', '業力', '煩惱', '戒定慧', 
                    '帶業往生', '信願行', '一門深入', '看破放下', '持名念佛', '華嚴',
                    '般若', '法華', '楞嚴', '因果', '菩提心', '四弘誓願', '普賢十大願王',
                    '師承', '孝道', '三皈依', '五戒', '十善', '六度', '六和敬', '三福',
                    '四十八願', '一乘', '一心不亂', '三昧', '善財童子五十三參', '佛陀教育',
                    '佛教與宗教']
        
        for sent in sentences:
            sent = sent.strip().replace('　', ' ')
            sent = re.sub(r'\s+', ' ', sent)
            if len(sent) > 30 and len(sent) < 200:
                for kw in keywords:
                    if kw in sent:
                        key_points.append(sent)
                        break
            if len(key_points) >= 5:
                break
    
    # Deduplicate
    unique_points = []
    for p in key_points:
        if p not in unique_points:
            unique_points.append(p)
    
    # Ensure 3-5 points
    key_points = unique_points[:5]
    while len(key_points) < 3:
        key_points.append("開示佛法要義，指導同修正確修行方向")
    
    # Summary: first 2-3 sentences
    summary_sentences = re.split(r'[。！？]', content[:1500])
    summary_parts = []
    for s in summary_sentences:
        s = s.strip().replace('　', ' ')
        s = re.sub(r'\s+', ' ', s)
        if len(s) > 20:
            summary_parts.append(s)
        if len(summary_parts) >= 3:
            break
    summary = '。'.join(summary_parts) + '。'
    
    return summary, key_points

def find_concepts(content):
    """Find which of the 31 concepts appear in the content."""
    found = []
    for concept in CONCEPTS:
        if concept in content:
            found.append(concept)
    return found[:5]  # Limit to 5

def generate_tags(title, concepts):
    """Generate 2-3 tags."""
    tags = []
    if '念佛' in concepts or '阿彌陀佛' in concepts or '極樂世界' in concepts or '往生' in title:
        tags.append('淨土')
    if '華嚴' in concepts or '法華' in concepts or '楞嚴' in concepts or '般若' in concepts:
        tags.append('經典')
    if '戒定慧' in title or '修行' in title or '懺悔' in title:
        tags.append('修行')
    if '答問' in title or '學佛答問' in title:
        tags.append('答問')
    if not tags:
        tags = ['開示', '答問']
    return tags[:3]

def process_code(code):
    """Process a single code and return the wiki page content and metadata."""
    # First, get metadata from first line
    code_dir = RAW_BASE / code
    md_files = sorted(code_dir.glob("*.md"))
    if not md_files:
        return None, None, f"No content for {code}"
    
    with open(md_files[0], 'r', encoding='utf-8-sig') as f:
        first_line = f.readline().strip()
    title, date, place, pages = extract_metadata(first_line)
    
    # Read full content
    with open(md_files[0], 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    summary, key_points = generate_summary_and_key_points(content, code)
    concepts = find_concepts(content)
    tags = generate_tags(title, concepts)
    
    # Build wiki content
    wiki_content = f"""---
type: source
category: 開示問答與活動
topic: 學佛答問
code: {code}
title: {title}
date: {date}
place: {place}
pages: {pages}
raw: doc/開示問答與活動/學佛答問/{code}/
tags: {tags}
created: 2026-08-07
updated: 2026-08-07
---

# {title}（{code}）

- **檔名**：{code}
- **類別**：開示問答與活動 / 學佛答問
- **集數**：{pages}
- **日期地點**：{date}，{place}
- **原始路徑**：`doc/開示問答與活動/學佛答問/{code}/`

## 概要

{summary}

## 重點

"""
    for kp in key_points:
        wiki_content += f"- {kp}〔{code}-0001〕\n"
    
    wiki_content += "\n## 相關概念\n\n"
    if concepts:
        for c in concepts:
            wiki_content += f"- [[概念/{c}]]\n"
    else:
        wiki_content += "- (無對應概念頁)\n"
    
    wiki_content += "\n## 相關頁面\n\n"
    wiki_content += "- [[開示問答與活動/學佛答問]] — 主題頁\n"
    
    return wiki_content, (date, place), None

# Main processing
if __name__ == "__main__":
    WIKI_BASE.mkdir(parents=True, exist_ok=True)
    
    written = 0
    errors = []
    incomplete = []
    
    for code in CODES:
        try:
            content, meta, error = process_code(code)
            if error:
                errors.append((code, error))
                continue
            
            date, place = meta
            output_path = WIKI_BASE / f"{code}.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            written += 1
            print(f"Written: {code}")
            
            # Check for incomplete metadata
            if not date or not place:
                incomplete.append(code)
                
        except Exception as e:
            errors.append((code, str(e)))
            print(f"Error processing {code}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Files written: {written}")
    print(f"Errors: {len(errors)}")
    print(f"Incomplete metadata: {len(incomplete)}")
    if incomplete:
        print(f"Codes with incomplete metadata: {incomplete}")
    if errors:
        for code, err in errors:
            print(f"  {code}: {err}")