import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 邮件配置（从环境变量读取，或使用默认值）
SMTP_SERVER = os.getenv('SMTP_SERVER', 'your_smtp_server')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'your_email')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_password')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'recipient_email')
SENDER_EMAIL = SMTP_USERNAME

def load_trending_data(filename="trending_repos.json"):
    """加载热门项目数据"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"错误：{filename} 文件不存在，请先运行 scrape_trending.py")
        return []
    except json.JSONDecodeError:
        print(f"错误：{filename} 文件格式错误")
        return []

def generate_email_content(repos):
    """生成邮件内容"""
    if not repos:
        return "", ""
    
    # 邮件主题
    subject = f"GitHub今日热门项目摘要 - {datetime.now().strftime('%Y-%m-%d')}"
    
    # 邮件正文
    body_parts = []
    body_parts.append(f"# GitHub今日热门项目摘要\n")
    body_parts.append(f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    body_parts.append(f"\n以下是今日GitHub热门项目前5个的详细摘要：\n")
    body_parts.append(f"\n{'='*60}\n")
    
    for repo in repos:
        body_parts.append(f"\n## 【{repo['rank']}】{repo['name']}")
        body_parts.append(f"项目地址：{repo['url']}")
        body_parts.append(f"\n{repo['summary']}")
        body_parts.append(f"\n{'='*60}\n")
    
    body_parts.append(f"\n---\n")
    body_parts.append(f"此邮件由 GitHub Trending Email 技能自动生成")
    
    return subject, "\n".join(body_parts)

def send_email(subject, body):
    """发送邮件"""
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENT_EMAIL]):
        print("错误：邮件配置不完整，请在 .env 文件中配置以下变量：")
        print("- SMTP_SERVER: 邮件服务器地址")
        print("- SMTP_PORT: 邮件服务器端口")
        print("- SMTP_USERNAME: 发件人邮箱")
        print("- SMTP_PASSWORD: 发件人邮箱密码或授权码")
        print("- RECIPIENT_EMAIL: 收件人邮箱")
        return False
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = Header(SENDER_EMAIL, 'utf-8')
        msg['To'] = Header(RECIPIENT_EMAIL, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加正文
        msg.attach(MIMEText(body, 'markdown', 'utf-8'))
        
        # 连接服务器并发送邮件
        print(f"正在连接邮件服务器 {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # 启用TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"邮件发送成功！发送到：{RECIPIENT_EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("错误：邮件服务器认证失败，请检查用户名和密码")
        return False
    except smtplib.SMTPConnectError:
        print("错误：无法连接到邮件服务器，请检查服务器地址和端口")
        return False
    except Exception as e:
        print(f"错误：发送邮件失败 - {str(e)}")
        return False

def main():
    """主函数"""
    print(f"开始发送GitHub热门项目邮件 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载热门项目数据
    repos = load_trending_data()
    
    if not repos:
        print("没有找到热门项目数据，发送失败")
        return
    
    # 生成邮件内容
    subject, body = generate_email_content(repos)
    
    # 发送邮件
    send_email(subject, body)

if __name__ == "__main__":
    main()