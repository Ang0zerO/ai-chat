import streamlit as st
import openai

# API 配置从 Streamlit Secrets 读取
openai.api_base = st.secrets["openai"]["api_base"]
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="角色扮演AI", page_icon="🎭")
st.title("🎭 角色扮演 AI")

# 侧边栏：角色设定 + 清除对话
with st.sidebar:
    st.header("🎭 角色设定")
    system_prompt = st.text_area(
        "输入角色描述，例如：\n你是一只可爱的猫娘，说话带喵~，喜欢撒娇。",
        value="你是一个友好的助手。",
        height=200
    )
    if st.button("✨ 应用角色"):
        st.session_state.system_prompt = system_prompt
        st.success("角色已更新！")
    
    if st.button("🗑️ 清除对话"):
        st.session_state.messages = []
        st.rerun()

# 初始化 session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "你是一个友好的助手。"

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 构建消息列表，加入系统提示词
                messages = [{"role": "system", "content": st.session_state.system_prompt}]
                messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
                
                response = openai.ChatCompletion.create(
                    model="deepseek-chat",  # 根据你的中转站支持的模型名修改
                    messages=messages
                )
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"出错了：{e}")
