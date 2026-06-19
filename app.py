import streamlit as st
import re
from gigachat import GigaChat

st.set_page_config(page_title="SecurLLM — прототип", layout="centered")

# --- ТЁМНЫЙ CSS (как на лендинге) ---
st.markdown("""
<style>
    /* Общий фон */
    .stApp {
        background-color: #0b1115;
        color: #e0e9ee;
    }
    .main > div {
        background-color: #0b1115;
    }
    /* Заголовки */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
    }
    /* Поля ввода и выпадающие списки */
    .stTextArea textarea, .stSelectbox div, .stButton button {
        background-color: #111e1e !important;
        color: #e0e9ee !important;
        border: 1px solid #2a4a3a !important;
        border-radius: 8px !important;
    }
    .stSelectbox div {
        background-color: #111e1e !important;
    }
    /* Кнопка */
    .stButton button {
        background-color: transparent !important;
        border: 1px solid #80c9b0 !important;
        color: #80c9b0 !important;
        font-weight: 600 !important;
        transition: 0.2s;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #162424 !important;
        box-shadow: 0 0 12px rgba(120, 200, 160, 0.1);
    }
    /* Блоки вывода */
    .stAlert, .stInfo, .stSuccess, .stWarning {
        background-color: #111e1e !important;
        border: 1px solid #2a4a3a !important;
        color: #b0c9d4 !important;
        border-radius: 8px !important;
    }
    .stAlert { border-left: 3px solid #80c9b0 !important; }
    .stInfo { border-left: 3px solid #2dd4bf !important; }
    .stSuccess { border-left: 3px solid #80c9b0 !important; }
    .stWarning { border-left: 3px solid #f59e0b !important; }
    /* Метки */
    .stMarkdown label {
        color: #b0c9d4 !important;
    }
    /* Разделитель */
    hr {
        border-color: #1a2a2a !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ШАПКА С ЛОГОТИПОМ СБЕРА ---
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

# --- ПРОВЕРКА СЕКРЕТА ---
try:
    GIGACHAT_KEY = st.secrets["GIGACHAT_KEY"]
except Exception:
    st.error("❌ Ошибка: не найден секрет GIGACHAT_KEY. Проверьте настройки приложения.")
    st.stop()

# --- СПИСОК ТИПОВЫХ ПОМЕЩЕНИЙ ---
room_types = {
    "Кабинет генерального директора": "Кабинет руководителя, сейф для документов, переговорная зона.",
    "Операционный зал": "Зал обслуживания клиентов, 4 кассы, работа с наличными и безналом.",
    "Кассовый узел": "Кассовая комната, 2 кассы, сейф для денег, работа с наличными.",
    "Серверная (ЦОД)": "Серверная стойка, 5 серверов, система охлаждения, круглосуточный доступ.",
    "Хранилище ценностей": "Сейфовая комната, металлические сейфы, система климат-контроля.",
    "ИТ-отдел": "Рабочие места программистов, сетевое оборудование, доступ в серверную."
}

# --- ИНТЕРФЕЙС: ДВЕ КОЛОНКИ (выпадающий список + ручной ввод) ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📋 Выберите типовое помещение**")
    selected = st.selectbox("", list(room_types.keys()), index=0, label_visibility="collapsed")

with col2:
    st.markdown("**✏️ Или введите своё описание**")
    manual_input = st.text_area("", height=68, placeholder="Например: переговорная комната на 10 человек", label_visibility="collapsed")

# --- КНОПКА "ПОЛУЧИТЬ РЕКОМЕНДАЦИЮ" ---
if st.button("Получить рекомендацию", type="primary", use_container_width=True):
    # Определяем, что использовать: выбранное типовое или ручной ввод
    if manual_input.strip():
        room_desc = manual_input.strip()
    else:
        room_desc = room_types[selected] + f" (Тип: {selected})"

    if not room_desc.strip():
        st.warning("⚠️ Выберите типовое помещение или введите описание вручную.")
    else:
        with st.spinner("🔄 GigaChat анализирует..."):
            try:
                with GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False) as client:
                    prompt = f"""
Ты — эксперт по оснащению банков инженерно-техническими средствами охраны (ИТСО).
Нормативная база: Сборник № 4461, РД 78.36.003-2002, Р 102-2024.

Твоя задача — по описанию помещения определить зону защиты и выдать детальную рекомендацию по составу ИТСО с обоснованием.

Классификация зон и категории:
- Категория 1 (Зона 1, клиентская/общедоступная): операционные залы, вестибюли, коридоры.
  Требования: видеонаблюдение, датчики движения на входах.
- Категория 2 (Зона 2, офисная/ограниченного доступа): кабинеты руководителей, бухгалтерия, ИТ-отделы.
  Требования: СКУД (карты), тревожная кнопка, видеонаблюдение, датчики открытия/движения.
- Категория 3A (Зона 3A, ЦОД/серверная): серверные, коммутационные.
  Требования: СКУД (двухфакторная: карта+PIN), многорубежная сигнализация, видео с высоким разрешением, контроль климата.
- Категория 3B (Зона 3B, хранилище ценностей): сейфовые комнаты, депозитарии.
  Требования: СКУД (карта+биометрия), многорубежная сигнализация (вибрация, акустика), видео с распознаванием лиц, вывод на Росгвардию.
- Категория 3C (Зона 3C, кассовый узел): операционные кассы, кассовые комнаты.
  Требования: СКУД (карта+PIN), сигнализация, видео над каждым рабочим местом.

Для каждого рекомендованного средства указывай, на основании какого документа и какой категории оно требуется.

Помещение: {room_desc}

Определи категорию (зону) и выдай рекомендацию по ИТСО с обоснованием.
Оформи ответ строго в таком формате:

**Категория (Зона):** ...
**Рекомендуемый состав ИТСО:** ...
**Обоснование:** ... (с указанием нормативных документов и категорий)
"""
                    response = client.chat(prompt)
                    raw = response.choices[0].message.content

                    # Парсим структурированный ответ
                    zone_match = re.search(r"\*\*Категория \(Зона\):\*\*\s*(.+)", raw)
                    rec_match = re.search(r"\*\*Рекомендуемый состав ИТСО:\*\*\s*(.+)", raw)
                    just_match = re.search(r"\*\*Обоснование:\*\*\s*(.+)", raw)

                    if zone_match and rec_match and just_match:
                        st.success("✅ Рекомендация готова")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📌 Категория (Зона)**")
                            st.info(zone_match.group(1))
                            st.markdown("**🛠️ Рекомендуемый состав ИТСО**")
                            st.success(rec_match.group(1))
                        with col2:
                            st.markdown("**📋 Обоснование**")
                            st.write(just_match.group(1))
                    else:
                        st.success("✅ Рекомендация готова")
                        st.markdown(raw)
            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")
