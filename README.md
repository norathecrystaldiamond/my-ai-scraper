# my-ai-scraper
# 🕵️‍♂️ AI 智能网页抓取助手 (Streamlit Web Scraping Agent)

## 📖 项目简介

本项目是 AI 提效工具的**入门级轻量级 PoC（概念验证）**。
基于 Streamlit 框架与 ScrapeGraphAI 构建。用户无需编写任何复杂的爬虫代码，只需输入目标网址和自然语言提示词（如：“提取网页上的所有标题”），AI 就会自动渲染网页、理解内容并返回结构化的表格数据。

## ✨ 核心功能

1. **自然语言驱动抓取**：摒弃传统的 XPath/CSS 选择器，直接通过 Prompt 指挥大模型提取信息。
2. **动态网页支持**：底层集成 Playwright (Chromium) 无头浏览器，能够应对 JS 动态渲染的网页（如小红书等）。
3. **数据格式化与导出**：内置 Pandas 数据处理，将大模型返回的 JSON 转为可视化表格，并支持一键下载为 Excel (CSV) 格式（已处理中文乱码）。
4. **多模型兼容**：底层接入 DeepSeek API，在保证效果的同时大幅降低 Token 消耗成本。

## 🛠️ 环境依赖

本项目基于 Python 3.10+ 运行。请先安装依赖包：
```bash
pip install -r requirements.txt

☁️ 云端部署方案
本项目已成功部署至 Streamlit Community Cloud。

通过配置 packages.txt 安装 Linux 系统级依赖（如 libnss3、libatk-bridge2.0-0 等）。

通过配置 requirements.txt 锁定 Playwright 稳定版本。

同事无需配置任何环境，直接访问公网链接，填入 API Key 即可使用。

💻 快速运行指令
进入项目目录：

bash
cd starter_ai_agents/web_scraping_ai_agent
启动 Streamlit 应用：

bash
streamlit run ai_scrapper.py
浏览器会自动弹出界面（通常为 http://localhost:8501），在左侧输入你的 DeepSeek API Key 即可开始使用。
