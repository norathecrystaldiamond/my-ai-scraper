# Import the required libraries
import streamlit as st
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph
import os
import subprocess

# 自动安装 Playwright 浏览器（解决云端报错核心）
@st.cache_resource
def install_playwright():
    if not os.path.exists(os.path.expanduser("~/.cache/ms-playwright")):
        subprocess.run(["playwright", "install", "chromium"])

install_playwright()

# Set up the Streamlit app
st.title("网页扒皮神器🕵️‍♂️")
st.caption("输入网址，让 AI 帮你提取你需要的信息")

# Get OpenAI API key from user
openai_access_token = st.secrets.get("DEEPSEEK_API_KEY", "")

if openai_access_token:
    model = st.radio(
        "Select the model",
        ["deepseek-chat"], 
        index=0,
    )    
    
    graph_config = {
        "llm": {
            "api_key": openai_access_token,
            "model": model,
            "base_url": "https://api.deepseek.com",
        },
    }
    
    # Get the URL of the website to scrape
    url = st.text_input("Enter the URL of the website you want to scrape")
    
    # 给用户一个下拉菜单选择任务
    task_option = st.selectbox(
        "请选择你想让 AI 提取什么内容：",
        ["提取网页上的所有标题", "提取网页上的主要正文内容", "提取网页上的所有链接", "自定义需求..."]
    )

    # 如果选了自定义，就弹出一个输入框
    if task_option == "自定义需求...":
        user_prompt = st.text_input("请输入你的自定义需求：")
    else:
        user_prompt = task_option

    # 关键修复：必须在点击按钮且参数完整时才执行抓取
    if st.button("Scrape") and url and user_prompt:
        
        with st.spinner('AI 正在努力抓取中，请耐心等待...'):
            # Create a SmartScraperGraph object
            smart_scraper_graph = SmartScraperGraph(
                prompt=user_prompt,
                source=url,
                config=graph_config
            )
            
            try:
                result = smart_scraper_graph.run()
                
                if result and "content" in result:
                    data = result["content"]

                    if isinstance(data, list):
                        # 如果是列表，展示漂亮的表格
                        if len(data) > 0 and isinstance(data[0], dict):
                            clean_data = [list(item.values())[0] if item else "" for item in data]
                            df = pd.DataFrame(clean_data, columns=["抓取结果"])
                        else:
                            df = pd.DataFrame(data, columns=["抓取结果"])
                        
                        st.dataframe(df, use_container_width=True)
                        
                        # 一键下载按钮
                        csv = df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 下载数据 (Excel 可打开)",
                            data=csv,
                            file_name='抓取数据.csv',
                            mime='text/csv',
                        )
                    else:
                        # 如果是长文本，直接展示文本
                        st.success("AI 提取完成！")
                        st.markdown(f"### 📝 AI 的提取结果：\n{data}")
                else:
                    st.write(result)
            except Exception as e:
                st.error(f"抓取失败了，错误原因：{e}")
