import streamlit as st
import requests
import json
from openai import OpenAI
import time


base_url = "https://api.zyfan.zone/v1/"
client = OpenAI(api_key="sk-XnLvK819JUq44iQx488a4216DbC34c10A1AfA414Dc55C30a", base_url=base_url)

# 定义API的端点和headers
API_ENDPOINT = "https://fake-sora-api.sorawebui.com/v1/video/generations"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-1111"
}

# 创建Streamlit页面
st.title("OpenAI-Sora 演示版")
st.info("这是一个使用OpenAI和Sora API的简单演示。")
st.warning("请注意，目前Sora API尚未开放，当前仅为模拟接口功能。")
prompt_text = "A man sits on a chair in a closed but transparent room, wearing a red coat and his eyes glaze over as fireworks go up outside the room"

# 创建两列布局
col1, col2, col3 = st.columns(3)
# 向第一列添加内容
with col1:
    if st.button("A man sits on a chair in a closed but transparent room, wearing a red coat and his eyes glaze over as fireworks go up outside the room"):
        prompt_text = "A man sits on a chair in a closed but transparent room, wearing a red coat and his eyes glaze over as fireworks go up outside the room"

# 向第二列添加内容
with col2:
    if st.button("A gorgeously rendered papercraft world of a coral reef, rife with colorful fish and sea creatures"):
        prompt_text = "A gorgeously rendered papercraft world of a coral reef, rife with colorful fish and sea creatures"

# 向第三列添加内容
with col3:
    if st.button("3D animation of a small, round, fluffy creature with big, expressive eyes explores a vibrant, enchanted forest. "):
        prompt_text = "3D animation of a small, round, fluffy creature with big, expressive eyes explores a vibrant, enchanted forest. The creature, a whimsical blend of a rabbit and a squirrel, has soft blue fur and a bushy, striped tail. It hops along a sparkling stream, its eyes wide with wonder. The forest is alive with magical elements: flowers that glow and change colors, trees with leaves in shades of purple and silver, and small floating lights that resemble fireflies. The creature stops to interact playfully with a group of tiny, fairy-like beings dancing around a mushroom ring. The creature looks up in awe at a large, glowing tree that seems to be the heart of the forest."


st.text_input("请输入你希望生成的影片描述词:", prompt_text)

submit_button = st.button("Send API Request")

progress_bar = st.progress(0)

# 按钮功能
if submit_button:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system",
            "content": "将下列描述翻译为英文, 如果描述本来为英文，则直接返回该描述, 不要做任何额外改变。"},
                  {
            "role": "user",
            "content": prompt_text}],
        stream=False,
        max_tokens=1024,
        temperature=0.8,
        presence_penalty=1.1,
        top_p=0.8)
    progress_bar.progress(30)
    content = response.choices[0].message.content
    st.write(content)
    time.sleep(0.1)
    progress_bar.progress(40)
    
    payload = {
        "model": "sora-1.0-turbo",
        "prompt": content,
        "size": "1920x1080"
    }
    
    response = requests.post(API_ENDPOINT, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        st.success("Request was successful!")
        
        response_json = response.json()
        # st.json(response_json)  # 显示原始JSON响应
        
        # 提取视频URL
        video_url = response_json.get('data', [{}])[0].get('url', None)
        if video_url:
            st.video(video_url)
        else:
            st.warning("No video URL found in the response.")
        
    else:
        st.error(f"Request failed with status code: {response.status_code}")
    progress_bar.progress(100)