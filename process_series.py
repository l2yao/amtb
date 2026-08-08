#!/usr/bin/env python3
"""
Process AMTB series and generate wiki source pages.
"""

import os
import re
from pathlib import Path

# Configuration
DOC_ROOT = Path(r"C:\Users\Long\Documents\amtb\amtb\doc\開示問答與活動")
WIKI_ROOT = Path(r"C:\Users\Long\Documents\amtb\amtb\wiki\開示問答與活動")

# Topic mapping
TOPICS = {
    "電台弘法": {
        "codes": ["24-001", "24-002", "24-003", "24-004", "24-005", "24-006", "24-007", 
                  "24-008", "24-009", "24-010", "24-011", "24-012", "24-013", "24-014", 
                  "24-015", "24-016", "24-017", "24-018", "24-019", "24-020", "24-021", 
                  "24-022", "24-023", "24-024"],
        "topic_name": "電台弘法"
    },
    "弘法紀實專題紀念影片": {
        "codes": ["25-058", "25-059", "25-060", "25-061", "25-062", "25-063", "25-066",
                  "25-134", "25-137", "25-146", "25-151", "25-156", "32-009", "61-268", "65-076"],
        "topic_name": "弘法紀實專題紀念影片"
    },
    "基礎佛學": {
        "codes": ["22-005", "22-006", "22-012", "22-015"],
        "topic_name": "基礎佛學"
    }
}

# Existing concept pages (from wiki/概念/)
CONCEPTS = [
    "一乘", "三皈依", "三福", "五戒", "佛教與宗教", "佛陀教育", "六和敬", "六度", 
    "十善", "四十八願", "四弘誓願", "念佛", "普賢十大願王", "菩提心", "阿彌陀佛", 
    "信願行", "極樂世界", "一心不亂", "帶業往生", "一門深入", "持名念佛", 
    "看破放下", "三昧", "華嚴", "善財童子五十三參", "楞嚴", "法華", "因果", 
    "般若", "師承", "孝道"
]

def extract_metadata(first_line, total_episodes=1):
    """Extract metadata from first line: 題目（共N集）日期 地點 檔名：CODE-PAGE"""
    result = {
        "title": "",
        "episodes": total_episodes,
        "date": "",
        "place": "",
        "code": "",
        "page": ""
    }
    
    # Extract title (everything before （共 or （第)
    title_match = re.match(r'^([^（]+)', first_line.strip())
    if title_match:
        result["title"] = title_match.group(1).strip()
    
    # Extract episodes from "共N集" if present
    ep_match = re.search(r'（共(\d+)集）', first_line)
    if ep_match:
        result["episodes"] = int(ep_match.group(1))
    else:
        result["episodes"] = total_episodes
    
    # Extract date (format: YYYY/M or YYYY/M/D)
    date_match = re.search(r'(\d{4}/\d{1,2}(?:/\d{1,2})?)', first_line)
    if date_match:
        result["date"] = date_match.group(1)
    
    # Extract place (between date and 檔名)
    place_match = re.search(r'\d{4}/\d{1,2}(?:/\d{1,2})?\s+([^檔]+)\s+檔名', first_line)
    if place_match:
        place = place_match.group(1).strip()
        if place and place != "—":
            result["place"] = place
    
    # Extract code and page
    file_match = re.search(r'檔名：([^\s]+)', first_line)
    if file_match:
        full_code = file_match.group(1).strip()
        result["code"] = "-".join(full_code.split("-")[:2])
        result["page"] = full_code
    
    return result

def read_series_files(topic_folder, code):
    """Read all .md files in a series folder, sorted."""
    series_path = DOC_ROOT / topic_folder / code
    md_files = sorted(series_path.glob("*.md"))
    contents = []
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            contents.append((md_file.name, content))
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    return contents

def generate_summary(content, max_sentences=3):
    """Generate a 2-3 sentence summary from content."""
    # Remove first line (metadata)
    lines = content.split('\n')[1:]
    text = ' '.join(line.strip() for line in lines if line.strip())
    
    # Split into sentences (Chinese punctuation)
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    # Take first few meaningful sentences
    summary = '。'.join(sentences[:max_sentences])
    if summary and not summary.endswith('。'):
        summary += '。'
    return summary

def extract_key_points(content, code):
    """Extract key teachings from content."""
    lines = content.split('\n')[1:]  # Skip metadata line
    points = []
    
    # Look for lines with key teachings (often start with 師父：, 法師：, or contain important terms)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip very short lines
        if len(line) < 15:
            continue
        # Look for substantive teachings
        if any(keyword in line for keyword in ['佛法', '修行', '念佛', '往生', '業障', '因果', '孝道', 
                                                  '三皈', '五戒', '十善', '六度', '四弘', '菩提心',
                                                  '阿彌陀佛', '極樂世界', '看破', '放下', '清淨心',
                                                  '平等心', '真誠', '慈悲', '智慧', '禪定', '般若',
                                                  '師承', '教育', '教學', '倫理', '道德', '宗教',
                                                  '迷信', '開光', '灌頂', '超度', '冤業', '宿業']):
            # Clean up the line
            point = line[:120] + ('…' if len(line) > 120 else '')
            points.append(f"- {point}〔{code}-0001〕")
            if len(points) >= 5:
                break
    
    # If not enough points, add some from beginning of content
    if len(points) < 3:
        for line in lines:
            line = line.strip()
            if len(line) > 20 and len(points) < 5:
                point = line[:120] + ('…' if len(line) > 120 else '')
                points.append(f"- {point}〔{code}-0001〕")
    
    return points[:5]

def find_related_concepts(content):
    """Find which existing concept pages are mentioned in content."""
    found = []
    for concept in CONCEPTS:
        if concept in content:
            found.append(f"[[概念/{concept}]]")
    return found[:5]  # Limit to 5

def generate_wiki_page(topic_folder, topic_name, code, contents):
    """Generate wiki page content for a series."""
    # Use first file for metadata
    first_file, first_content = contents[0]
    total_episodes = len(contents)
    meta = extract_metadata(first_content.split('\n')[0], total_episodes)
    
    title = meta["title"] or code
    episodes = meta["episodes"]
    date = meta["date"]
    place = meta["place"]
    
    # Combine all content for analysis
    full_content = '\n'.join(c for _, c in contents)
    
    # Generate sections
    summary = generate_summary(first_content)
    key_points = extract_key_points(first_content, code)
    related_concepts = find_related_concepts(full_content)
    
    # Tags based on topic and content
    tags = [topic_name]
    if "念佛" in full_content or "阿彌陀佛" in full_content or "往生" in full_content:
        tags.append("淨土")
    if "孝道" in full_content or "父母" in full_content:
        tags.append("孝道")
    if "教育" in full_content or "教學" in full_content:
        tags.append("教育")
    tags = tags[:3]
    
    # Build wiki page
    lines = []
    lines.append("---")
    lines.append(f"type: source")
    lines.append(f"category: 開示問答與活動")
    lines.append(f"topic: {topic_name}")
    lines.append(f"code: {code}")
    lines.append(f"title: {title}")
    lines.append(f"date: {date}")
    lines.append(f"place: {place}")
    lines.append(f"pages: 共 {episodes} 集")
    lines.append(f"raw: doc/開示問答與活動/{topic_folder}/{code}/")
    lines.append(f"tags: {tags}")
    lines.append(f"created: 2026-08-07")
    lines.append(f"updated: 2026-08-07")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}（{code}）")
    lines.append("")
    lines.append(f"- **檔名**：{code}")
    lines.append(f"- **類別**：開示問答與活動 / {topic_name}")
    lines.append(f"- **集數**：共 {episodes} 集")
    lines.append(f"- **日期地點**：{date}，{place}")
    lines.append(f"- **原始路徑**：`doc/開示問答與活動/{topic_folder}/{code}/`")
    lines.append("")
    lines.append("## 概要")
    lines.append("")
    lines.append(summary)
    lines.append("")
    lines.append("## 重點")
    lines.append("")
    for point in key_points:
        lines.append(point)
    lines.append("")
    lines.append("## 相關概念")
    lines.append("")
    if related_concepts:
        for concept in related_concepts:
            lines.append(f"- {concept}")
    else:
        lines.append("- [[概念/念佛]]")
        lines.append("- [[概念/因果]]")
    lines.append("")
    lines.append("## 相關頁面")
    lines.append("")
    lines.append(f"- [[開示問答與活動/{topic_name}]] — 主題頁")
    lines.append("")
    
    return '\n'.join(lines)

def main():
    WIKI_ROOT.mkdir(parents=True, exist_ok=True)
    
    total_written = 0
    issues = []
    
    for topic_folder, topic_info in TOPICS.items():
        topic_name = topic_info["topic_name"]
        codes = topic_info["codes"]
        
        for code in codes:
            try:
                contents = read_series_files(topic_folder, code)
                if not contents:
                    issues.append(f"{code}: No .md files found")
                    continue
                
                wiki_content = generate_wiki_page(topic_folder, topic_name, code, contents)
                
                output_path = WIKI_ROOT / f"{code}.md"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wiki_content)
                
                total_written += 1
                print(f"Written: {code}.md")
                
            except Exception as e:
                issues.append(f"{code}: {str(e)}")
    
    print(f"\n=== Summary ===")
    print(f"Files written: {total_written}")
    print(f"Issues: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")

if __name__ == "__main__":
    main()