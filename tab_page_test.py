import gradio as gr
import time
from openai import OpenAI
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# 定义莫兰迪春季色彩主题
morandi_colors = {
    "mint_green": "#C7D3CC",  # 主色调：淡薄荷绿
    "soft_pink": "#E8D6CF",   # 辅助色1：柔和粉色
    "light_blue": "#B8C5D6",  # 辅助色2：淡蓝色
    "warm_beige": "#E4CFBF",  # 辅助色3：浅杏色
    "background": "#F5F2ED",  # 背景色：米白色
    "text": "#5D5C58"         # 文字色：深灰褐色
}

# 自定义CSS样式，使用莫兰迪色彩
custom_css = """
:root {
    --mint-green: """ + morandi_colors["mint_green"] + """;
    --soft-pink: """ + morandi_colors["soft_pink"] + """;
    --light-blue: """ + morandi_colors["light_blue"] + """;
    --warm-beige: """ + morandi_colors["warm_beige"] + """;
    --background: """ + morandi_colors["background"] + """;
    --text: """ + morandi_colors["text"] + """;
}

body {
    background-color: var(--background);
    color: var(--text);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.gradio-container {
    background-color: var(--background);
}

/* 标题样式 */
h1 {
    color: var(--text);
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: linear-gradient(to right, var(--mint-green), var(--soft-pink));
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
    color: var(--text);
    font-size: 1.8rem;
    border-bottom: 2px solid var(--mint-green);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* 标签页样式 */
.tabs {
    background-color: var(--background);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.tab-nav {
    background-color: var(--mint-green);
    padding: 0.5rem;
    border-radius: 10px 10px 0 0;
}

.tab-nav button {
    background-color: transparent;
    color: var(--text);
    border: none;
    padding: 0.8rem 1.5rem;
    margin: 0 0.2rem;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    transition: all 0.3s ease;
}

.tab-nav button:hover, .tab-nav button.selected {
    background-color: var(--background);
    color: var(--text);
}

/* 聊天界面样式 */
.message-wrap {
    background-color: var(--background);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.user-message {
    background-color: var(--light-blue);
    color: var(--text);
    border-radius: 18px 18px 0 18px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.bot-message {
    background-color: var(--soft-pink);
    color: var(--text);
    border-radius: 18px 18px 18px 0;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* 输入框和按钮样式 */
input[type="text"], textarea {
    background-color: white;
    border: 2px solid var(--mint-green);
    border-radius: 8px;
    padding: 0.8rem;
    color: var(--text);
    font-size: 1rem;
}

button {
    background-color: var(--mint-green);
    color: var(--text);
    border: none;
    border-radius: 8px;
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

button:hover {
    background-color: var(--soft-pink);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 移除了春季装饰元素 */
"""

# 创建自定义主题 - 简化版本，移除不支持的参数
theme = gr.themes.Base(
    primary_hue="green",
    secondary_hue="pink",
    neutral_hue="gray",
    font=("Segoe UI", "ui-sans-serif", "system-ui", "sans-serif"),
)

# 设置自定义颜色
theme.background_fill = morandi_colors["background"]
theme.button_primary_background_fill = morandi_colors["mint_green"]
theme.button_primary_background_fill_hover = morandi_colors["soft_pink"]
theme.button_secondary_background_fill = morandi_colors["light_blue"]
theme.button_secondary_background_fill_hover = morandi_colors["warm_beige"]
theme.block_title_text_color = morandi_colors["text"]
theme.block_label_text_color = morandi_colors["text"]
theme.input_background_fill = "white"
theme.input_border_color = morandi_colors["mint_green"]

NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
NVIDIA_MODEL = os.getenv('NV_MODEL')

def generate_recommended_response(message, history):
    """
    Function to stream OpenAI responses for 饮食预算 tab.
    """
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )
    # Prepare the messages in the required format
    messages = [{"role": "system", "content": "你是生鲜超市的销售员,店里最近来了一批时令春菜,有荠菜,春笋,蕨菜,请根据用户提出的采购需求,根据营养学搭配原则,推荐客户购买新的春菜,同时要引导客户购买店里其他的商品,比如鸡蛋,牛奶,面包等,并且要给出合理的搭配方案,让客户觉得你是一个专业的营养师.在对话末尾要列出需要采购的食材,并以markdown格式输出表格,同时提示用户去超市里现场体验购买,请根据用户的提问进行回答,文字末尾加入如下内容:你要是去逛的话,我帮你打印一份清单"}]
    for msg in history:
        if 'role' in msg:
            if msg['role'] == 'user':
                messages.append({"role": "user", "content": msg['content']})
            if msg['role'] == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
    # Add the current user message to the conversation history if it's not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})
      # Call OpenAI's API with streaming enabled
    # meta/llama-3.3-70b-instruct
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1-distill-qwen-32b",
        messages=messages,
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True
    )
    # Stream the response chunks
    bot_message = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_message += chunk.choices[0].delta.content
            yield history + [{"role": "assistant", "content": bot_message}]

def generate_emotional_recipe_response(message, history):
    """
    Function to stream OpenAI responses for 情感菜谱 tab.
    """
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )
    # Prepare the messages in the required format
    messages = [{"role": "system", "content": "你是一位专业的情感美食顾问，能够根据用户的情绪状态推荐适合的食谱。你擅长分析用户的心情，并推荐能够改善情绪或配合情绪的美食。请根据用户描述的情感状态，推荐适合的食谱，并解释这些食物如何影响情绪。在回答中，请提供详细的烹饪步骤，并以markdown格式输出食材清单。"}]
    for msg in history:
        if 'role' in msg:
            if msg['role'] == 'user':
                messages.append({"role": "user", "content": msg['content']})
            if msg['role'] == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
    # Add the current user message to the conversation history if it's not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})
    # Call OpenAI's API with streaming enabled
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1-distill-qwen-32b",
        messages=messages,
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True
    )
    # Stream the response chunks
    bot_message = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_message += chunk.choices[0].delta.content
            yield history + [{"role": "assistant", "content": bot_message}]

def generate_random_food_response(message, history):
    """
    Function to stream OpenAI responses for 随机美食 tab.
    """
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )
    # Prepare the messages in the required format
    messages = [{"role": "system", "content": "你是一位创意美食专家，擅长推荐新颖、意想不到的食物组合。你的任务是根据用户的喜好或要求，随机推荐有趣且美味的食物搭配。这些推荐可以打破传统，但必须保证美味和可行性。在回答中，请提供详细的食材清单和简单的制作方法，并以markdown格式呈现。每次回答都应该包含一些惊喜元素，让用户感到新鲜和兴奋。"}]
    for msg in history:
        if 'role' in msg:
            if msg['role'] == 'user':
                messages.append({"role": "user", "content": msg['content']})
            if msg['role'] == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
    # Add the current user message to the conversation history if it's not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})
    # Call OpenAI's API with streaming enabled
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1-distill-qwen-32b",
        messages=messages,
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True
    )
    # Stream the response chunks
    bot_message = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_message += chunk.choices[0].delta.content
            yield history + [{"role": "assistant", "content": bot_message}]

def generate_nutrition_response(message, history):
    """
    Function to stream OpenAI responses for 营养定制 tab.
    """
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )
    # Prepare the messages in the required format
    messages = [{"role": "system", "content": "你是一位专业的营养师，能够根据用户的健康状况和目标提供个性化的饮食建议。你擅长分析用户的营养需求，并设计符合这些需求的饮食计划。请根据用户提供的信息（如健康目标、饮食限制、过敏原等），提供详细的营养建议和饮食计划。在回答中，请解释各种食物的营养价值，并以markdown格式提供每日或每周的饮食安排表。"}]
    for msg in history:
        if 'role' in msg:
            if msg['role'] == 'user':
                messages.append({"role": "user", "content": msg['content']})
            if msg['role'] == 'assistant':
                messages.append({"role": "assistant", "content": msg['content']})
    # Add the current user message to the conversation history if it's not empty
    if message and message.strip():
        messages.append({"role": "user", "content": message})
    # Call OpenAI's API with streaming enabled
    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-r1-distill-qwen-32b",
        messages=messages,
        temperature=0.6,
        top_p=0.7,
        max_tokens=4096,
        stream=True
    )
    # Stream the response chunks
    bot_message = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            bot_message += chunk.choices[0].delta.content
            yield history + [{"role": "assistant", "content": bot_message}]

def user_input(user_message, history):
    """
    Function to handle user input for all tabs.
    """
    return "", history + [{"role": "user", "content": user_message}]

# 使用 Blocks API 创建多标签页界面
with gr.Blocks(css=custom_css, theme=theme) as demo:
# 应用标题
    gr.Markdown("""
    ##  🥗MealMind饭谋引擎🥬 
    *春风送暖，美食相伴*
    """)

    with gr.Tabs():
        # 第一个标签页：饮食预算
        with gr.Tab("预算"):
            gr.Markdown("""
            ### SmartFoodPlan智能饮食预算管家
            """)
            budget_chatbot = gr.Chatbot(type="messages")
            budget_msg = gr.Textbox(label="Your Message")
            budget_clear = gr.Button("Clear Chat")
            
            # Link the user input and bot response functions
            budget_msg.submit(user_input, [budget_msg, budget_chatbot], [budget_msg, budget_chatbot], queue=False).then(
                generate_recommended_response, inputs=[budget_msg, budget_chatbot], outputs=budget_chatbot
            )
            budget_clear.click(lambda: None, None, budget_chatbot, queue=False)
        
        # 第二个标签页：情感菜谱
        with gr.Tab("情感"):
            gr.Markdown("""
            ### FeelTaste情感驱动的菜谱设计师
            """)
            emotion_chatbot = gr.Chatbot(type="messages")
            emotion_msg = gr.Textbox(label="Your Message")
            emotion_clear = gr.Button("Clear Chat")
            
            # Link the user input and bot response functions
            emotion_msg.submit(user_input, [emotion_msg, emotion_chatbot], [emotion_msg, emotion_chatbot], queue=False).then(
                generate_emotional_recipe_response, inputs=[emotion_msg, emotion_chatbot], outputs=emotion_chatbot
            )
            emotion_clear.click(lambda: None, None, emotion_chatbot, queue=False)

        # 第三个标签页：随机美食
        with gr.Tab("随机"):
            gr.Markdown("""
            ### ChoiceLess轻决策随机美食助手
            """)
            random_chatbot = gr.Chatbot(type="messages")
            random_msg = gr.Textbox(label="Your Message")
            random_clear = gr.Button("Clear Chat")
            
            # Link the user input and bot response functions
            random_msg.submit(user_input, [random_msg, random_chatbot], [random_msg, random_chatbot], queue=False).then(
                generate_random_food_response, inputs=[random_msg, random_chatbot], outputs=random_chatbot
            )
            random_clear.click(lambda: None, None, random_chatbot, queue=False)
            
        # 第四个标签页：营养定制
        with gr.Tab("营养"):
            gr.Markdown("""
            ### NutriGoal营养目标反向定制系统
            """)
            nutrition_chatbot = gr.Chatbot(type="messages")
            nutrition_msg = gr.Textbox(label="Your Message")
            nutrition_clear = gr.Button("Clear Chat")
            
            # Link the user input and bot response functions
            nutrition_msg.submit(user_input, [nutrition_msg, nutrition_chatbot], [nutrition_msg, nutrition_chatbot], queue=False).then(
                generate_nutrition_response, inputs=[nutrition_msg, nutrition_chatbot], outputs=nutrition_chatbot
            )
            nutrition_clear.click(lambda: None, None, nutrition_chatbot, queue=False)

# 启动应用
demo.launch(share=False, server_name='0.0.0.0')
