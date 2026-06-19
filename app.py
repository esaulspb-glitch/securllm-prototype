import streamlit as st
from gigachat import GigaChat

st.set_page_config(page_title="SecurLLM — прототип", layout="centered")
st.title("🏦 SecurLLM")
st.markdown("_Методология оснащения ИТСО на основе GigaChat_")

# Проверяем, что секрет передан
try:
    GIGACHAT_KEY = st.secrets["GIGACHAT_KEY"]
except Exception as e:
    st.error(f"❌ Ошибка: не найден секрет GIGACHAT_KEY. Проверьте настройки приложения.")
    st.stop()

room_desc = st.text_area("Опишите помещение банка:", height=150)

if st.button("Получить рекомендацию"):
    if room_desc:
        with st.spinner("GigaChat анализирует..."):
            try:
                with GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False) as client:
                    prompt = f"""
Ты — эксперт по оснащению банков ИТСО.
Нормативная база: Сборник № 4461, РД 78.36.003-2002, Р 102-2024.

Классификация:
- Зона 1: клиентская → только видео
- Зона 2: офисная → СКУД + тревожная кнопка + видео
- Зона 3A: ЦОД → СКУД + сигнализация + видео
- Зона 3B: хранилище → СКУД + многорубежная сигнализация + видео + биометрия
- Зона 3C: касса → СКУД + сигнализация + видео (карта+PIN)

Помещение: {room_desc}
Определи зону и выдай рекомендацию по ИТСО с обоснованием (в виде структурированного отчёта).
"""
                    response = client.chat(prompt)
                    st.success("✅ Рекомендация готова")
                    st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")
    else:
        st.warning("Введите описание помещения")
