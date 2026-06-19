import streamlit as st
import re
from gigachat import GigaChat

st.set_page_config(page_title="SecurLLM", layout="centered")

# --- КАСТОМНЫЙ CSS (фирменный стиль Сбера + исправленные отступы) ---
st.markdown("""
<style>
    /* Скрываем стандартный хедер Streamlit */
    header {
        display: none !important;
    }
    /* Убираем верхний отступ у main */
    .main > div {
        padding-top: 0 !important;
    }
    /* Увеличиваем отступ контейнера */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
    }
    /* Основные цвета Сбера */
    :root {
        --sber-green: #1A991A;
        --sber-dark: #333F48;
        --sber-bg: #FFFFFF;
        --sber-gray: #EEF3FF;
        --sber-text: #333F48;
    }

    /* Общий фон */
    .stApp {
        background-color: var(--sber-bg);
    }
    .main > div {
        background-color: var(--sber-bg);
    }

    /* Заголовки — графитовый */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--sber-dark) !important;
        font-family: 'Inter', 'Arial', sans-serif;
        font-weight: 600;
    }

    /* Основной текст */
    .stMarkdown, .stText, label, .stSelectbox label, .stTextArea label {
        color: var(--sber-dark) !important;
        font-family: 'Inter', 'Arial', sans-serif;
    }

    /* Поля ввода и выпадающие списки */
    .stTextArea textarea, .stSelectbox div, .stButton button {
        background-color: var(--sber-gray) !important;
        color: var(--sber-dark) !important;
        border: 1px solid #d0d7de !important;
        border-radius: 8px !important;
        font-family: 'Inter', 'Arial', sans-serif;
    }
    .stTextArea textarea:focus, .stSelectbox div:focus {
        border-color: var(--sber-green) !important;
        box-shadow: 0 0 0 2px rgba(26, 153, 26, 0.2) !important;
    }

    /* Кнопка — зелёная */
    .stButton button {
        background-color: var(--sber-green) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        transition: 0.2s;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0f7a0f !important;
        box-shadow: 0 4px 12px rgba(26, 153, 26, 0.3);
    }

    /* Блоки вывода */
    .stAlert, .stInfo, .stSuccess, .stWarning {
        background-color: var(--sber-gray) !important;
        border: 1px solid #d0d7de !important;
        color: var(--sber-dark) !important;
        border-radius: 8px !important;
        font-family: 'Inter', 'Arial', sans-serif;
    }
    .stAlert { border-left: 4px solid var(--sber-green) !important; }
    .stInfo { border-left: 4px solid #2d7b2d !important; }
    .stSuccess { border-left: 4px solid var(--sber-green) !important; }
    .stWarning { border-left: 4px solid #f5a623 !important; }

    /* Разделитель */
    hr {
        border-color: #d0d7de !important;
    }

    /* Дополнительный отступ для шапки */
    .sber-header {
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- ШАПКА С ЛОГОТИПОМ СБЕРА (с отступом) ---
st.markdown("""
    <div class="sber-header" style="display: flex; align-items: center; gap: 16px; padding-bottom: 16px; border-bottom: 1px solid #d0d7de;">
        <div style="display: flex; align-items: center; gap: 6px;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0054A6, #FDB913, #1A991A); display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 20px; font-weight: 700;">✓</span>
            </div>
            <span style="font-size: 24px; font-weight: 700; color: #1A991A; letter-spacing: -0.5px;">Сбер</span>
        </div>
        <span style="font-size: 18px; color: #333F48; font-weight: 300;">| SecurLLM</span>
    </div>
""", unsafe_allow_html=True)

st.title("Методология оснащения ИТСО")
st.markdown("_Интеллектуальная классификация помещений на основе GigaChat_")

# --- ПРОВЕРКА СЕКРЕТА ---
try:
    GIGACHAT_KEY = st.secrets["GIGACHAT_KEY"]
except Exception:
    st.error("❌ Ошибка: не найден секрет GIGACHAT_KEY. Проверьте настройки приложения.")
    st.stop()

# --- СПИСОК ТИПОВЫХ ПОМЕЩЕНИЙ ---
room_options = {
    "": "— Выберите типовое помещение —",
    "Кабинет генерального директора": "Кабинет руководителя, сейф для документов, переговорная зона.",
    "Операционный зал": "Зал обслуживания клиентов, 4 кассы, работа с наличными и безналом.",
    "Кассовый узел": "Кассовая комната, 2 кассы, сейф для денег, работа с наличными.",
    "Серверная (ЦОД)": "Серверная стойка, 5 серверов, система охлаждения, круглосуточный доступ.",
    "Хранилище ценностей": "Сейфовая комната, металлические сейфы, система климат-контроля.",
    "ИТ-отдел": "Рабочие места программистов, сетевое оборудование, доступ в серверную.",
    "Туалет / подсобка": "Подсобное помещение, минимальная ценность активов."
}

# --- ИНТЕРФЕЙС: ДВЕ КОЛОНКИ ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Выберите типовое помещение**")
    selected_key = st.selectbox(
        "",
        options=list(room_options.keys()),
        format_func=lambda x: room_options[x] if x else "",
        index=0,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Или введите своё описание**")
    manual_input = st.text_area(
        "",
        height=68,
        placeholder="Например: переговорная комната на 10 человек",
        label_visibility="collapsed"
    )

# --- КНОПКА ---
if st.button("Получить рекомендацию", type="primary", use_container_width=True):
    if manual_input.strip():
        room_desc = manual_input.strip()
    elif selected_key:
        room_desc = room_options[selected_key] + f" (Тип: {selected_key})"
    else:
        room_desc = ""

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

                    zone_match = re.search(r"\*\*Категория \(Зона\):\*\*\s*(.+)", raw)
                    rec_match = re.search(r"\*\*Рекомендуемый состав ИТСО:\*\*\s*(.+)", raw)
                    just_match = re.search(r"\*\*Обоснование:\*\*\s*(.+)", raw)

                    if zone_match and rec_match and just_match:
                        st.success("✅ Рекомендация готова")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**📌 Категория (Зона)**")
                            st.info(zone_match.group(1))
                            st.markdown("**🛠️ Рекомендуемый состав ИТСО**")
                            st.success(rec_match.group(1))
                        with c2:
                            st.markdown("**📋 Обоснование**")
                            st.write(just_match.group(1))
                    else:
                        st.success("✅ Рекомендация готова")
                        st.markdown(raw)
            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")
