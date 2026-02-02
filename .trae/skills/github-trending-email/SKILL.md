---
name: "github-trending-email"
description: "爬取GitHub今日热门项目前5个，获取README，生成中文摘要并发送邮件。当用户需要了解GitHub热门项目并接收邮件摘要时调用。"
---

# GitHub Trending Email

This skill helps you stay updated with the latest GitHub trending projects by:

1. **Scraping GitHub Trending** - Fetches the top 5 trending repositories from https://github.com/trending
2. **Getting README Files** - Retrieves the README.md for each trending project
3. **Generating Summary** - Creates a Chinese summary for each project including:
   - What the project is
   - What problem it solves
   - Technology stack
   - Star count
4. **Sending Email** - Delivers the summary to your email address

## Usage

Invoke this skill when you want to:
- Stay updated with the latest GitHub trends
- Receive a curated list of popular projects with summaries
- Get insights into what's hot in the developer community

## Scripts Included

1. **scrape_trending.py** - Scrapes GitHub trending page and fetches READMEs
2. **send_email.py** - Sends the summary email

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4
  - python-dotenv

## Configuration

1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 python-dotenv
   ```

2. Create a `.env` file with your email configuration:
   ```env
   SMTP_SERVER=your_smtp_server
   SMTP_PORT=your_smtp_port
   SMTP_USERNAME=your_email
   SMTP_PASSWORD=your_password
   RECIPIENT_EMAIL=recipient_email
   ```

## Execution

Run the main script to start the process:
```bash
python scrape_trending.py
```