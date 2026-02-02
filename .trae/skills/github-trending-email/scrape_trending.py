import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# GitHub Trending URL
TRENDING_URL = "https://github.com/trending"

# Headers to mimic browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_github_trending():
    """爬取GitHub热门项目前5个"""
    print("正在爬取GitHub热门项目...")
    
    # 发送请求
    response = requests.get(TRENDING_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return []
    
    # 解析HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 找到所有热门项目
    repositories = []
    repo_elements = soup.select("article.Box-row")
    
    # 只取前5个
    for i, repo_element in enumerate(repo_elements[:5]):
        # 提取仓库信息
        repo_link = repo_element.select_one("h2 a")
        if not repo_link:
            continue
        
        # 提取仓库路径 (owner/repo)
        repo_path = repo_link.get("href").strip("/").strip()
        repo_name = repo_path.split("/")[-1]
        
        # 提取描述
        description_element = repo_element.select_one("p")
        description = description_element.text.strip() if description_element else ""
        
        # 提取语言
        language_element = repo_element.select_one(".text-gray-dark span[itemprop='programmingLanguage']")
        language = language_element.text.strip() if language_element else ""
        
        # 提取Star数量
        star_element = repo_element.select_one("a[href$='stargazers']")
        star_count = star_element.text.strip() if star_element else "0"
        # 处理K格式的Star数量
        star_count = int(float(star_count.replace("k", "")) * 1000) if "k" in star_count else int(star_count.replace(",", ""))
        
        # 获取README
        readme_content = get_repository_readme(repo_path)
        
        # 生成中文摘要
        summary = generate_chinese_summary(repo_name, description, language, star_count, readme_content)
        
        # 构建仓库信息
        repo_info = {
            "rank": i + 1,
            "name": repo_name,
            "full_path": repo_path,
            "description": description,
            "language": language,
            "stars": star_count,
            "readme": readme_content,
            "summary": summary,
            "url": f"https://github.com/{repo_path}"
        }
        
        repositories.append(repo_info)
        print(f"已获取项目 {i+1}: {repo_name}")
    
    return repositories

def get_repository_readme(repo_path):
    """获取仓库的README.md内容"""
    readme_url = f"https://raw.githubusercontent.com/{repo_path}/main/README.md"
    
    try:
        response = requests.get(readme_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.text
        
        # 尝试其他分支
        readme_url = f"https://raw.githubusercontent.com/{repo_path}/master/README.md"
        response = requests.get(readme_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.text
        
        return ""
    except Exception as e:
        print(f"获取README失败 {repo_path}: {e}")
        return ""

def generate_chinese_summary(repo_name, description, language, stars, readme_content):
    """生成中文摘要"""
    # 提取README中的关键信息
    readme_text = readme_content[:2000]  # 只取前2000字符
    
    # 简单的摘要生成逻辑
    summary_parts = []
    
    # 项目名称
    summary_parts.append(f"**项目名称：** {repo_name}")
    
    # 项目描述
    if description:
        summary_parts.append(f"**项目描述：** {description}")
    else:
        # 从README中提取描述
        readme_description = extract_description_from_readme(readme_text)
        if readme_description:
            summary_parts.append(f"**项目描述：** {readme_description}")
        else:
            summary_parts.append("**项目描述：** 暂无详细描述")
    
    # 解决的问题
    problem_solved = extract_problem_solved(readme_text)
    if problem_solved:
        summary_parts.append(f"**解决的问题：** {problem_solved}")
    else:
        summary_parts.append("**解决的问题：** 暂无详细信息")
    
    # 技术栈
    if language:
        summary_parts.append(f"**技术栈：** {language}")
    else:
        # 从README中提取技术栈
        tech_stack = extract_tech_stack(readme_text)
        if tech_stack:
            summary_parts.append(f"**技术栈：** {tech_stack}")
        else:
            summary_parts.append("**技术栈：** 暂无详细信息")
    
    # Star数量
    summary_parts.append(f"**Star数量：** {stars}")
    
    return "\n".join(summary_parts)

def extract_description_from_readme(readme_text):
    """从README中提取描述"""
    # 尝试从README的开头提取描述
    lines = readme_text.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!") and not line.startswith("```"):
            return line[:200]
    return ""

def extract_problem_solved(readme_text):
    """从README中提取解决的问题"""
    # 简单的关键词匹配
    keywords = ["解决", "solve", "problem", "issue", "challenge", "痛点"]
    lines = readme_text.split("\n")
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in keywords:
            if keyword in line_lower:
                # 返回包含关键词的行及其后几行
                context = " ".join(lines[i:i+3])
                return context[:200]
    return ""

def extract_tech_stack(readme_text):
    """从README中提取技术栈"""
    # 简单的技术栈提取
    tech_keywords = ["技术栈", "tech", "stack", "language", "framework", "依赖", "dependencies"]
    lines = readme_text.split("\n")
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for keyword in tech_keywords:
            if keyword in line_lower:
                # 返回包含关键词的行及其后几行
                context = " ".join(lines[i:i+5])
                return context[:200]
    return ""

def save_to_json(data, filename="trending_repos.json"):
    """保存数据到JSON文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {filename}")

def main():
    """主函数"""
    print(f"开始爬取GitHub热门项目 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 爬取热门项目
    trending_repos = scrape_github_trending()
    
    if trending_repos:
        # 保存到JSON文件
        save_to_json(trending_repos)
        
        # 打印摘要
        print("\n=== 热门项目中文摘要 ===")
        for repo in trending_repos:
            print(f"\n【{repo['rank']}】{repo['name']}")
            print(repo['summary'])
            print("-" * 50)
        
        # 提示执行发送邮件脚本
        print("\n爬取完成，请运行 send_email.py 发送邮件")
    else:
        print("未获取到热门项目")

if __name__ == "__main__":
    main()