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
    st.stop()import streamlit as st
import re
from gigachat import GigaChat

st.set_page_config(page_title="SecurLLM — прототип", layout="centered")

# Шапка с логотипом (иконка Сбера через Font Awesome)
st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <i class="fas fa-building-columns" style="font-size: 28px; color: #21a038;"></i>
        <span style="font-size: 24px; font-weight: 600; color: #21a038;">СБЕР</span>import streamlit as st
import re
from gigachat import GigaChat

st.set_page_config(page_title="SecurLLM — прототип", layout="centered")

# Шапка с логотипом (иконка Сбера через Font Awesome)
st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <i class="fas fa-building-columns" style="font-size: 28px; color: #21a038;"></i>
        <span style="font-size: 24px; font-weight: 600; color: #21a038;">СБЕР</span>
        <span style="font-size: 18px; color: #b0c9d4;">| SecurLLM</span>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

st.title("🏦 Методология оснащения ИТСО")
st.markdown("_Интеллектуальная классификация помещений на основе GigaChat_")

# Проверка секрета
try:
    GIGACHAT_KEY = st.secrets["GIGACHAT_KEY"]
except Exception:
    st.error("❌ Ошибка: не найден секрет GIGACHAT_KEY. Проверьте настройки приложения.")
    st.stop()

# Кнопки быстрого ввода
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏧 Касса"):
        st.session_state.room_desc = "Кассовый узел на 2 кассы, работает с наличными, есть сейф."
with col2:
    if st.button("🖥️ Серверная"):
        st.session_state.room_desc = "Серверная с 5 стойками, круглосуточный доступ, система охлаждения."
with col3:
    if st.button("🏛️ Хранилище"):
        st.session_state.room_desc = "Хранилище ценностей, металлические сейфы, система климат-контроля."

# Поле для ввода
room_desc = st.text_area(
    "Опишите помещение банка:",
    value=st.session_state.get("room_desc", ""),
    height=120
)

if st.button("Получить рекомендацию", type="primary"):
    if not room_desc.strip():
        st.warning("Введите описание помещения или выберите пример.")
    else:
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
Определи зону и выдай рекомендацию по ИТСО с обоснованием.
Оформи ответ строго в таком формате:

**Зона:** ...
**Рекомендуемый состав ИТСО:** ...
**Обоснование:** ...
"""
                    response = client.chat(prompt)
                    raw = response.choices[0].message.content

                    # Парсим структурированный ответ
                    zone_match = re.search(r"\*\*Зона:\*\*\s*(.+)", raw)
                    rec_match = re.search(r"\*\*Рекомендуемый состав ИТСО:\*\*\s*(.+)", raw)
                    just_match = re.search(r"\*\*Обоснование:\*\*\s*(.+)", raw)

                    if zone_match and rec_match and just_match:
                        st.success("✅ Рекомендация готова")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📌 Зона**")
                            st.info(zone_match.group(1))
                            st.markdown("**🛠️ Рекомендуемый состав ИТСО**")
                            st.success(rec_match.group(1))
                        with col2:
                            st.markdown("**📋 Обоснование**")
                            st.write(just_match.group(1))
                    else:
                        # если парсинг не удался — выводим как есть
                        st.success("✅ Рекомендация готова")
                        st.markdown(raw)
            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")
        <span style="font-size: 18px; color: #b0c9d4;">| SecurLLM</span>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

st.title("🏦 Методология оснащения ИТСО")
st.markdown("_Интеллектуальная классификация помещений на основе GigaChat_")

# Проверка секрета
try:
    GIGACHAT_KEY = st.secrets["GIGACHAT_KEY"]
except Exception:
    st.error("❌ Ошибка: не найден секрет GIGACHAT_KEY. Проверьте настройки приложения.")
    st.stop()

# Кнопки быстрого ввода
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏧 Касса"):
        st.session_state.room_desc = "Кассовый узел на 2 кассы, работает с наличными, есть сейф."
with col2:
    if st.button("🖥️ Серверная"):
        st.session_state.room_desc = "Серверная с 5 стойками, круглосуточный доступ, система охлаждения."
with col3:
    if st.button("🏛️ Хранилище"):
        st.session_state.room_desc = "Хранилище ценностей, металлические сейфы, система климат-контроля."

# Поле для ввода
room_desc = st.text_area(
    "Опишите помещение банка:",
    value=st.session_state.get("room_desc", ""),
    height=120
)

if st.button("Получить рекомендацию", type="primary"):
    if not room_desc.strip():
        st.warning("Введите описание помещения или выберите пример.")
    else:
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
Определи зону и выдай рекомендацию по ИТСО с обоснованием.
Оформи ответ строго в таком формате:

**Зона:** ...
**Рекомендуемый состав ИТСО:** ...
**Обоснование:** ...
"""
                    response = client.chat(prompt)
                    raw = response.choices[0].message.content

                    # Парсим структурированный ответ
                    zone_match = re.search(r"\*\*Зона:\*\*\s*(.+)", raw)
                    rec_match = re.search(r"\*\*Рекомендуемый состав ИТСО:\*\*\s*(.+)", raw)
                    just_match = re.search(r"\*\*Обоснование:\*\*\s*(.+)", raw)

                    if zone_match and rec_match and just_match:
                        st.success("✅ Рекомендация готова")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📌 Зона**")
                            st.info(zone_match.group(1))
                            st.markdown("**🛠️ Рекомендуемый состав ИТСО**")
                            st.success(rec_match.group(1))
                        with col2:
                            st.markdown("**📋 Обоснование**")
                            st.write(just_match.group(1))
                    else:
                        # если парсинг не удался — выводим как есть
                        st.success("✅ Рекомендация готова")
                        st.markdown(raw)
            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")

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
