from openai import OpenAI
import streamlit as st

st.set_page_config(layout='wide')

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Список моделей
models = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo-1106', 'gpt-4', 'gpt-4-1106-preview']

# Заголовок и боковая панель
# st.title("Чат-бот")
model = st.sidebar.selectbox('Выберите модель', models)

temperature = st.sidebar.slider("Температура", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
result = ''


# Функция для обработки чата
def chat(model, temperature, prompt, assistant, content):
    response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": 'Используй '+assistant+' для обработки '+prompt},
                    {"role": "user", "content": content},
                    # {"role": "assistant", "content": assistent},
                ],
                temperature=temperature,
            )
    return response.choices[0].message.content


# Поля для ввода текста
col1, col2 = st.columns(2)

with col1:
    prompt = col1.text_area(label='Введите инструкцию',
                            placeholder='Введите инструкцию',
                            height=150,
                            label_visibility='collapsed')

with col2:
    assistant = col2.text_area(label='Введите пример',
                               placeholder='Введите пример',
                               height=150,
                               label_visibility='collapsed')

# Поля для вывода результатов
col3, col4 = st.columns(2)
with col3:
    content = col3.text_area(label='Введите текст',
                             placeholder='Введите текст',
                             height=400,
                             label_visibility='collapsed')

    if st.button("Обработать", key='b_5'):
        result = chat(model, temperature, prompt, assistant, content)

with col4:
    col4.text_area(label='Обработанный текст',
                   placeholder='Обработанный текст',
                   value=result,
                   height=400,
                   label_visibility='collapsed')
