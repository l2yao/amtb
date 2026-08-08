#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create wiki source pages for 學佛答問 series.
"""

import os
import re
from pathlib import Path

# The 71 codes to process
CODES = [
    "21-015", "21-045", "21-047", "21-052", "21-080", "21-081", "21-090",
    "21-115", "21-116", "21-117", "21-157", "21-171", "21-214", "21-227",
    "21-234", "21-236", "21-242", "21-245", "21-246", "21-247", "21-249",
    "21-250", "21-251", "21-252", "21-253", "21-254", "21-255", "21-261",
    "21-267", "21-268", "21-269", "21-270", "21-271", "21-272", "21-274",
    "21-275", "21-277", "21-279", "21-283", "21-284", "21-285", "21-286",
    "21-287", "21-288", "21-289", "21-291", "21-292", "21-293", "21-294",
    "21-295", "21-296", "21-298", "21-299", "21-304", "21-305", "21-307",
    "21-310", "21-313", "21-316", "21-319", "21-321", "21-323", "21-324",
    "21-325", "21-326", "21-328", "21-329", "21-330", "21-332", "21-333", "21-334"
]

# Existing concept pages (31)
CONCEPTS = [
    "一乘", "三皈依", "三福", "五戒", "佛教與宗教", "佛陀教育", "六和敬", "六度", "十善",
    "四十八願", "四弘誓願", "念佛", "普賢十大願王", "菩提心", "阿彌陀佛", "信願行",
    "極樂世界", "一心不亂", "帶業往生", "一門深入", "持名念佛", "看破放下", "三昧",
    "華嚴", "善財童子五十三參", "楞嚴", "法華", "因果", "般若", "師承", "孝道"
]

# Base paths
DOC_BASE = Path(r"C:\Users\Long\Documents\amtb\amtb\doc\開示問答與活動\學佛答問")
WIKI_BASE = Path(r"C:\Users\Long\Documents\amtb\amtb\wiki\開示問答與活動")

def extract_metadata(first_line):
    """Extract title, episode, date, place from first line."""
    # Pattern: Title (Episode) Date Place File: CODE-PAGE
    # Some may have missing fields
    line = first_line.strip()
    
    # Extract file code
    file_match = re.search(r'檔名[:：]\s*(\S+)', line)
    file_code = file_match.group(1) if file_match else ""
    
    # Extract episode
    episode_match = re.search(r'（(第[^）]+集|共[^）]+集)）', line)
    episode = episode_match.group(1) if episode_match else ""
    
    # Try to extract date and place
    # Format: Title 　　(Episode) 　　Date 　　Place 　　File: CODE
    # Using full-width spaces as separators
    parts = re.split(r'\s{2,}', line)
    
    title = ""
    date = ""
    place = ""
    
    if parts:
        # First part is title (may include episode)
        title = parts[0].strip()
        # Remove episode from title if present
        title = re.sub(r'\s*（[^）]+集）\s*$', '', title)
    
    # Look for date pattern (YYYY/M/D or YYYY/M or YYYY)
    for part in parts[1:]:
        if re.match(r'^\d{4}[/年]\d{1,2}([/月]\d{1,2})?', part):
            date = part.replace('年', '/').replace('月', '/').replace('日', '')
            break
    
    # Place is usually between date and file
    if date:
        date_idx = parts.index(next(p for p in parts if date in p))
        if date_idx + 1 < len(parts):
            next_part = parts[date_idx + 1]
            if '檔名' not in next_part and not re.match(r'^\d{4}[/年]', next_part):
                place = next_part
    elif len(parts) >= 3:
        # No date found, place might be parts[2]
        if '檔名' not in parts[2]:
            place = parts[2]
    
    # Clean up title - remove episode suffix if still there
    title = re.sub(r'\s*[（(]第[^）)]+集[）)]\s*$', '', title)
    title = re.sub(r'\s*[（(]共[^）)]+集[）)]\s*$', '', title)
    
    return title, episode, date, place, file_code

def extract_pages_from_episode(episode):
    """Extract number of pages from episode string."""
    if not episode:
        return "1"
    match = re.search(r'共(\d+)集', episode)
    if match:
        return match.group(1)
    match = re.search(r'第(\d+)集', episode)
    if match:
        # For single episode, we need to check how many files exist
        return "1"  # Will be overridden by actual file count
    return "1"

def read_first_line(filepath):
    """Read first line of a file, handling BOM."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return f.readline()

def read_file_content(filepath, max_chars=2000):
    """Read file content for summary extraction."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return f.read(max_chars)

def generate_summary_and_keypoints(code, md_files):
    """Generate 概要 and 重點 from actual content."""
    if not md_files:
        return "無內容可供摘要。", []
    
    # For 21-090 with 89 pages, read first, last, and key middle pages
    if code == "21-090" and len(md_files) > 10:
        key_indices = [0, 9, 19, 29, 39, 49, 59, 69, 79, -1]  # 0001, 0010, 0020, 0030, 0040, 0050, 0060, 0070, 0080, 0089
        key_files = [md_files[i] for i in key_indices if 0 <= i < len(md_files) or i == -1]
        if -1 in key_indices:
            key_files[-1] = md_files[-1]
    else:
        key_files = md_files
    
    all_content = ""
    keypoints = []
    
    for idx, md_file in enumerate(key_files):
        content = read_file_content(md_file, 3000)
        all_content += content + "\n\n"
        
        # Extract key teachings (Q&A pairs)
        # Look for 問： and 答： patterns
        qa_pairs = re.findall(r'問[：:]\s*([^\n]+(?:\n[^\n]+)*?)\n\s*答[：:]\s*([^\n]+(?:\n[^\n]+)*)', content)
        for q, a in qa_pairs[:3]:  # Limit per file
            q_short = q.strip()[:80]
            a_short = a.strip()[:120]
            page_num = md_file.stem
            keypoints.append(f"{q_short} → {a_short}〔{code}-{page_num}〕")
            if len(keypoints) >= 5:
                break
        
        # Also look for key statements without Q&A format
        if len(keypoints) < 5:
            # Look for sentences with key Buddhist terms
            sentences = re.split(r'[。！？]', content)
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 20 and len(sent) < 200:
                    # Check for Buddhist keywords
                    keywords = ['念佛', '阿彌陀佛', '極樂世界', '往生', '業障', '因果', '皈依', '五戒', 
                               '一心不亂', '帶業往生', '一門深入', '持名念佛', '看破放下', '信願行',
                               '華嚴', '楞嚴', '法華', '般若', '菩提心', '四弘誓願', '師承', '孝道']
                    if any(kw in sent for kw in keywords):
                        page_num = md_file.stem
                        keypoints.append(f"{sent}〔{code}-{page_num}〕")
                        if len(keypoints) >= 5:
                            break
        
        if len(keypoints) >= 5:
            break
    
    # Generate summary from first file content
    first_content = read_file_content(md_files[0], 2000)
    # Extract first few meaningful sentences
    sentences = re.split(r'[。！？]', first_content)
    summary_sentences = []
    for s in sentences:
        s = s.strip()
        if len(s) > 15 and not s.startswith('檔名') and not s.startswith('諸位') and not s.startswith('大家'):
            summary_sentences.append(s)
            if len(summary_sentences) >= 3:
                break
    
    summary = "。".join(summary_sentences) + "。" if summary_sentences else "此系列為學佛答問開示，解答同修關於修行、念佛、往生等方面的疑問。"
    
    # Ensure we have 3-5 keypoints
    keypoints = keypoints[:5]
    while len(keypoints) < 3:
        keypoints.append(f"解答同修關於修行實踐的疑問〔{code}-{md_files[0].stem}〕")
    
    return summary, keypoints

def find_relevant_concepts(content):
    """Find which existing concepts are mentioned in content."""
    found = []
    for concept in CONCEPTS:
        if concept in content:
            found.append(concept)
    return found[:5]  # Limit to 5

def process_code(code):
    """Process a single code and generate wiki page."""
    code_dir = DOC_BASE / code
    if not code_dir.exists():
        return None, f"Directory not found: {code_dir}"
    
    md_files = sorted(code_dir.glob("*.md"))
    if not md_files:
        return None, f"No .md files found for {code}"
    
    # Read first file for metadata
    first_line = read_first_line(md_files[0])
    title, episode, date, place, file_code = extract_metadata(first_line)
    
    # Determine page count
    if "共" in episode:
        pages = extract_pages_from_episode(episode)
    else:
        pages = str(len(md_files))
    
    # Generate summary and keypoints
    summary, keypoints = generate_summary_and_keypoints(code, md_files)
    
    # Find relevant concepts from first file content
    first_content = read_file_content(md_files[0], 5000)
    if len(md_files) > 1:
        # Also check last file for multi-page series
        last_content = read_file_content(md_files[-1], 5000)
        first_content += "\n" + last_content
    relevant_concepts = find_relevant_concepts(first_content)
    
    # Format date
    formatted_date = date if date else ""
    
    # Generate tags
    tags = ["學佛答問", "開示問答"]
    if "念佛" in first_content or "阿彌陀佛" in first_content:
        tags.append("念佛法門")
    if "往生" in first_content or "極樂世界" in first_content:
        tags.append("往生淨土")
    
    # Build wiki content
    wiki_content = f"""---
type: source
category: 開示問答與活動
topic: 學佛答問
code: {code}
title: {title}
date: {formatted_date}
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
- **集數**：共 {pages} 集
- **日期地點**：{formatted_date}，{place}
- **原始路徑**：`doc/開示問答與活動/學佛答問/{code}/`

## 概要

{summary}

## 重點

"""
    for kp in keypoints:
        wiki_content += f"- {kp}\n"
    
    wiki_content += "\n## 相關概念\n\n"
    if relevant_concepts:
        for concept in relevant_concepts:
            wiki_content += f"- [[概念/{concept}]]\n"
    else:
        wiki_content += "- (無對應既有概念頁)\n"
    
    wiki_content += f"""
## 相關頁面

- [[開示問答與活動/學佛答問]] — 主題頁
"""
    
    # Write wiki file
    wiki_file = WIKI_BASE / f"{code}.md"
    wiki_file.parent.mkdir(parents=True, exist_ok=True)
    with open(wiki_file, 'w', encoding='utf-8') as f:
        f.write(wiki_content)
    
    return {
        'code': code,
        'title': title,
        'date': formatted_date,
        'place': place,
        'pages': pages,
        'concepts': relevant_concepts
    }, None

def main():
    print(f"Processing {len(CODES)} codes...")
    results = []
    errors = []
    
    for code in CODES:
        result, error = process_code(code)
        if error:
            errors.append((code, error))
            print(f"  FAIL {code}: {error}")
        else:
            results.append(result)
            print(f"  OK {code}: pages={result['pages']}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully created: {len(results)} pages")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for code, error in errors:
            print(f"  {code}: {error}")
    
    # Check for incomplete metadata
    incomplete = [r for r in results if not r['date'] or not r['place']]
    if incomplete:
        print(f"\nIncomplete metadata (missing date/place): {len(incomplete)}")
        for r in incomplete:
            missing = []
            if not r['date']: missing.append("date")
            if not r['place']: missing.append("place")
            print(f"  {r['code']}: missing {', '.join(missing)}")

if __name__ == "__main__":
    main()