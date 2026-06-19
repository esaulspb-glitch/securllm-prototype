import streamlit as st
import re
from gigachat import GigaChat

st.set_page_config(
    page_title="SecurLLM — прототип",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------------------------
# Стилизация под лендинг (тёмный фон, зелёные акценты, шрифты)
# ----------------------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #0b1115;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0rem;
        max-width: 800px;
    }
    h1, h2, h3, .stMarkdown {
        color: #e0e9ee !important;
    }
    .stButton > button {
        background-color: #1a2a2a !important;
        color: #80c9b0 !important;
        border: 1px solid #80c9b0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #162424 !important;
        border-color: #80c9b0 !important;
        box-shadow: 0 0 12px rgba(120,200,160,0.3) !important;
    }
    .stSelectbox, .stTextArea {
        background-color: #111e1e !important;
        border: 1px solid #2a403a !important;
        border-radius: 8px !important;
        color: #e0e9ee !important;
    }
    .stAlert {
        background-color: #111e1e !important;
        border-left: 3px solid #80c9b0 !important;
    }
    .stSpinner > div {
        border-color: #80c9b0 !important;
    }
    .result-card {
        background: #111e1e;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #2a4a3a;
        margin-top: 20px;
    }
    .result-card h4 {
        color: #80c9b0;
        margin-top: 0;
    }
    .footer {
        margin-top: 40px;
        font-size: 0.8rem;
        color: #6a8a94;
        text-align: center;
        border-top: 1px solid #1a2828;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Шапка с логотипом
st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
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

# ----------------------------------------------------------------------
# Выпадающий список типовых помещений + ручной ввод
# ----------------------------------------------------------------------
presets = {
    "Кассовый узел": "Кассовый узел на 2 кассы, работает с наличными, есть сейф.",
    "Серверная (ЦОД)": "Серверная с 5 стойками, круглосуточный доступ, система охлаждения.",
    "Хранилище ценностей": "Хранилище ценностей, металлические сейфы, система климат-контроля.",
    "Кабинет генерального директора": "Кабинет генерального директора с сейфом для документов, переговорная зона.",
    "Операционный зал": "Операционный зал на 4 рабочих места, работа с клиентами, без наличных.",
    "Бухгалтерия": "Отдел бухгалтерии, 6 рабочих мест, документооборот, сейф для печатей."
}
preset_names = list(presets.keys())
preset_names.insert(0, "— выберите из списка —")

selected_preset = st.selectbox("Типовое помещение:", preset_names)

# Если выбран пресет, подставляем его описание в поле ввода
default_text = presets.get(selected_preset, "")
room_desc = st.text_area(
    "Или опишите своё помещение:",
    value=default_text,
    height=120,
    key="room_text"
)

# ----------------------------------------------------------------------
# Кнопка анализа
# ----------------------------------------------------------------------
if st.button("Получить рекомендацию", type="primary"):
    if not room_desc.strip():
        st.warning("Введите описание помещения или выберите типовое.")
    else:
        with st.spinner("GigaChat анализирует..."):
            try:
                with GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False) as client:
                    prompt = f"""
Ты — эксперт по оснащению банков инженерно-техническими средствами охраны (ИТСО).
Нормативная база: Сборник № 4461, РД 78.36.003-2002, Р 102-2024.

Задача: по описанию помещения определить категорию защиты и выдать детальную рекомендацию по составу ИТСО.

Классификация зон и требования к оснащению (согласно РД 78.36.003-2002, Сборнику № 4461):

- Зона 1 (клиентская / общедоступная): операционные залы, вестибюли, коридоры, холлы.
  Требования: видеонаблюдение (общий обзор), охранная сигнализация на входных группах.
- Зона 2 (офисная / ограниченного доступа): кабинеты руководителей, бухгалтерия, ИТ-отделы, переговорные.
  Требования: СКУД (электронные замки, считыватели карт), тревожная кнопка, видеонаблюдение (внутреннее и на входе), охранная сигнализация (датчики движения, открытия, разбития стекла).
- Зона 3A (ЦОД / серверная): серверные, коммутационные, аппаратные.
  Требования: СКУД (двухфакторная: карта+PIN или биометрия), многорубежная сигнализация (движение, открытие, вибрация, температура), видеонаблюдение с высокой детализацией, контроль микроклимата, резервирование питания.
- Зона 3B (хранилище ценностей): сейфовые комнаты, депозитарии.
  Требования: СКУД с биометрией, многорубежная сигнализация (вибрационные, акустические, магнитоконтактные), видеонаблюдение с распознаванием лиц, тревожная сигнализация с выводом на пульт Росгвардии, усиленная инженерная защита.
- Зона 3C (кассовый узел): операционные кассы, кассовые комнаты.
  Требования: СКУД (карта+PIN), сигнализация (движение, открытие, разбитие стекла), видеонаблюдение над каждым рабочим местом, тревожная кнопка.

Для каждого помещения также учитываются:
- Категория важности (по внутренней классификации банка) — соотносится с зоной.
- Группа защиты (определяется на основе ценности активов и уровня угроз) — задаётся автоматически.

Теперь, получив описание помещения: {room_desc}
Определи зону, категорию важности и группу защиты.
Выдай рекомендацию по ИТСО, указав обоснование со ссылкой на конкретные пункты нормативных документов.

Оформи ответ строго в таком формате:

**Зона:** ...
**Категория важности:** ...
**Группа защиты:** ...
**Рекомендуемый состав ИТСО:** ...
**Обоснование:** (с указанием, на основании каких нормативных требований и категорий принято решение)
"""
                    response = client.chat(prompt)
                    raw = response.choices[0].message.content

                    # Парсим структурированный ответ
                    zone_match = re.search(r"\*\*Зона:\*\*\s*(.+)", raw)
                    cat_match = re.search(r"\*\*Категория важности:\*\*\s*(.+)", raw)
                    group_match = re.search(r"\*\*Группа защиты:\*\*\s*(.+)", raw)
                    rec_match = re.search(r"\*\*Рекомендуемый состав ИТСО:\*\*\s*(.+)", raw)
                    just_match = re.search(r"\*\*Обоснование:\*\*\s*(.+)", raw)

                    st.success("✅ Рекомендация готова")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    if zone_match:
                        st.markdown(f"**📌 Зона:** {zone_match.group(1)}")
                    if cat_match:
                        st.markdown(f"**📊 Категория важности:** {cat_match.group(1)}")
                    if group_match:
                        st.markdown(f"**🔒 Группа защиты:** {group_match.group(1)}")
                    if rec_match:
                        st.markdown(f"**🛠️ Рекомендуемый состав ИТСО:**\n\n{rec_match.group(1)}")
                    if just_match:
                        st.markdown(f"**📋 Обоснование:**\n\n{just_match.group(1)}")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Ошибка при обращении к GigaChat: {e}")

# ----------------------------------------------------------------------
# Футер
# ----------------------------------------------------------------------
st.markdown("""
<div class="footer">
    SecurLLM — интеллектуальная методология оснащения ИТСО<br>
    © 2026 | ПАО Сбербанк
</div>
""", unsafe_allow_html=True)
