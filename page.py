from openai import OpenAI
import streamlit as st

st.set_page_config(page_title='Rewriter', page_icon=':wave:', layout='wide')


def creds_entered():
    if (st.session_state['user'].strip() == st.secrets['user_login'] and
            st.session_state['passwd'].strip() == st.secrets['password_login']):
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False


def authenticate_user():
    if 'authenticated' not in st.session_state:
        st.text_input(label='Username :', value='', key='user', on_change=creds_entered)
        st.text_input(label='Password :', value='', key='passwd', type='password', on_change=creds_entered)
        return False
    else:
        if st.session_state['authenticated']:
            return True
        else:
            st.text_input(label='Username :', value='', key='user', on_change=creds_entered)
            st.text_input(label='Password :', value='', key='passwd', type='password', on_change=creds_entered)
            return False


if authenticate_user():

    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

    # Список моделей
    models = ['gpt-3.5-turbo-16k', 'gpt-3.5-turbo-1106', 'gpt-4-1106-preview']

    # Заголовок и боковая панель
    model = st.sidebar.selectbox('Выберите модель', models)
    temperature = st.sidebar.slider("Температура", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
    result = ''

    # Функция для обработки чата
    def chat(model, temperature, prompt, assistant, content):
        response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": 'Для обработки '+prompt+' используй '+assistant},
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
