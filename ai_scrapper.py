# Import the required libraries
import streamlit as st
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph

# Set up the Streamlit app
st.title("网页扒皮神器🕵️‍♂️")
st.caption("输入网址，让 AI 帮你提取你需要的信息")

# Get OpenAI API key from user
openai_access_token = st.text_input("DeepSeek API Key", type="password")

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
        "loader_kwargs": {
            "headless": True,
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],
        },
    }
    # Get the URL of the website to scrape
    url = st.text_input("Enter the URL of the website you want to scrape")
    # Get the user prompt
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

    # Create a SmartScraperGraph object
    smart_scraper_graph = SmartScraperGraph(
        prompt=user_prompt,
        source=url,
        config=graph_config
    )
    # Scrape the website
if st.button("Scrape"):
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
        else:
            # 如果是长文本，直接展示文本，不要塞进表格
            st.success("AI 提取完成！")
            st.markdown(f"### 📝 AI 的提取结果：\n{data}")
    else:
        st.write(result)
