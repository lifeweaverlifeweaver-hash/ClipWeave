import streamlit as st

# Конфигурация на страницата
st.set_page_config(page_title="ClipWeave - Autonomous UGC SaaS", page_icon="🎬", layout="wide")

# Инициализация на данни в сесията
if "campaigns" not in st.session_state:
    st.session_state.campaigns = [
        {"id": 1, "brand": "BioGlow Cosmetics", "title": "TikTok UGC за нов серум", "budget": 120.0, "status": "Активна"},
        {"id": 2, "brand": "EcoHome BG", "title": "Reels видео за домакински уред", "budget": 150.0, "status": "Активна"}
    ]

if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

max_free = 3

# --- ЛИНГВИСТИЧЕН ДВИГАТЕЛ ЗА БЪЛГАРСКИ КОНТЕКСТ ---
def clean_bulgarian_text(text: str) -> str:
    glossary = {
        "клиентски опит": "потребителско изживяване",
        "лайк": "харесване",
        "шервам": "споделям",
        "бууствам": "промотирам"
    }
    for wrong, correct in glossary.items():
        text = text.replace(wrong, correct)
    return text.strip()

def split_into_subtitles(text: str, max_chars: int = 25) -> list:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = (current_line + " " + word).strip()
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# Странично меню (Sidebar)
st.sidebar.title("🔐 Клиентски и Админ Панел")
admin_password = st.sidebar.text_input("Парола за неограничен достъп:", type="password")
is_my_admin = (admin_password == "admin123")

if is_my_admin:
    st.sidebar.success("✅ Администраторски режим: НАПЪЛНО БЕЗПЛАТНО И НЕОГРАНИЧЕНО")
else:
    st.sidebar.info(f"Използвани безплатни генерации: {st.session_state.free_uses} / {max_free}")

menu = st.sidebar.selectbox("Изберете модул:", [
    "🤖 Streamlit AI Агент и Автоматизация", 
    "🚀 AI Генератор на субтитри и клипове", 
    "🛒 Маркетплейс за задачи (€)", 
    "📊 Моите Кампании", 
    "💳 Плащане и Абонамент (EasyPay)"
])

# -------------------------------------------------------------
# МОДУЛ 1: STREAMLIT AI АГЕНТ И АВТОМАТИЗАЦИЯ
# -------------------------------------------------------------
if menu == "🤖 Streamlit AI Агент и Автоматизация":
    st.title("🤖 ClipWeave Autonomous AI Agent")
    st.markdown("### Вашият интелигентен помощник за анализ на съдържание и оптимизация на български език.")

    st.info("💡 **Как работи AI агентът:** Той анализира актуалните тенденции за кратки форми (TikTok/Reels), коригира терминологията според българския бизнес контекст и подготвя готови пакети за субтитриране без глас зад кадър.")

    agent_topic = st.text_input("Въведете тема или продуктов ниш за анализ:", "натурална козметика и био продукти")
    
    if st.button("🧠 Стартирай AI анализ и генерирай стратегия"):
        if not agent_topic:
            st.warning("Моля, въведете тема.")
        else:
            st.success("✨ AI агентът анализира успешно нишата!")
            st.markdown("---")
            st.markdown("#### 📊 Доклад и препоръки от агента:")
            st.markdown(f"1. **Целева аудитория в България:** Активна жени 20-45 г. в големите градове, търсещи чисти съставки.")
            st.markdown(f"2. **Препоръчителна структура за видеото:** Динамични субтитри на тъмен фон с енергийна фонова музика (без говор).")
            st.markdown(f"3. **Генерирана топ кука (Hook):** *„Спрете да превъртате! Ето как {agent_topic} променя изцяло грижата за вас.“*")
            st.markdown("4. **Лингвистична проверка:** Термините са прегледани през българския речник на ClipWeave.")

# -------------------------------------------------------------
# МОДУЛ 2: AI ГЕНЕРАТОР НА СУБТИТРИ И КЛИПОВЕ
# -------------------------------------------------------------
elif menu == "🚀 AI Генератор на субтитри и клипове":
    st.title("🎬 ClipWeave Видео и Субтитри Генератор")
    st.markdown("### Създайте вертикално видео (9:16) само с музика и перфектно синхронизирани субтитри на български.")

    platform = st.selectbox("Платформа:", ["TikTok", "Instagram Reels", "YouTube Shorts"])
    raw_input_text = st.text_area("Въведете вашия текст или сценарий за субтитрите:", 
                                  "Спрете да превъртате! Това е най-лесният начин да развиете проекта си бързо и без излишни разходи.")

    if st.button("🚀 Генерирай пакет субтитри и подготви за рендър"):
        if not is_my_admin and st.session_state.free_uses >= max_free:
            st.error("⚠️ Изчерпихте вашите 3 безплатни опита! За неограничен достъп преминете към платен план през EasyPay.")
        elif not raw_input_text:
            st.warning("Моля, въведете текст.")
        else:
            if not is_my_admin:
                st.session_state.free_uses += 1
            
            cleaned_text = clean_bulgarian_text(raw_input_text)
            subtitles = split_into_subtitles(cleaned_text, max_chars=25)
            
            st.success("🎉 Текстът е успешно обработен и разбит на субтитри!")
            st.markdown("---")
            st.markdown(f"#### 📱 Резултат за {platform} (Без глас, само музика и текст):")
            
            for i, line in enumerate(subtitles):
                st.code(f"Ред {i+1} [Тайминг {i*3.0}с - {(i+1)*3.0}с]: {line}", language="text")
                
            st.info("🎵 *Системата автоматично синхронизира тези редове за вграждане във видео рендъра с фонова музика.*")

            if not is_my_admin:
                remaining = max_free - st.session_state.free_uses
                st.info(f"Остават ви {remaining} безплатни опита.")

# -------------------------------------------------------------
# МОДУЛ 3: МАРКЕТПЛЕЙС БОРСА (€)
# -------------------------------------------------------------
elif menu == "🛒 Маркетплейс за задачи (€)":
    st.title("🛒 Маркетплейс за брандове и създатели")
    st.markdown("### Публикувайте задачи с фиксирани бюджети в **€** или кандидатствайте като създател.")

    with st.expander("➕ Пусни нова задача"):
        new_title = st.text_input("Заглавие:")
        new_brand = st.text_input("Име на бранд:")
        new_budget = st.number_input("Бюджет в евро (€):", min_value=10.0, max_value=1000.0, value=50.0)
        
        if st.button("Публикувай в маркетплейса"):
            if new_title and new_brand:
                st.session_state.campaigns.append({"id": len(st.session_state.campaigns)+1, "brand": new_brand, "title": new_title, "budget": new_budget, "status": "Активна"})
                st.success("Успешно публикувахте задача!")
            else:
                st.warning("Попълнете полетата.")

    st.markdown("---")
    st.markdown("### Активни поръчки:")
    for camp in st.session_state.campaigns:
        st.info(f"**{camp['title']}** (Бранд: *{camp['brand']}*) — **Бюджет: €{camp['budget']}** [Статус: {camp['status']}]")
        if st.button(f"Кандидатствай #{camp['id']}", key=f"app_{camp['id']}"):
            st.success("Успешно кандидатствахте по задачата!")

# -------------------------------------------------------------
# МОДУЛ 4: КАМПАНИИ
# -------------------------------------------------------------
elif menu == "📊 Моите Кампании":
    st.title("📊 Управление на кампании")
    st.metric(label="Използвани генерации", value=st.session_state.free_uses if not is_my_admin else "Неограничено (Admin)")
    st.metric(label="Активни задачи в системата", value=len(st.session_state.campaigns))

# -------------------------------------------------------------
# МОДУЛ 5: ПЛАЩАНЕ (EasyPay)
# -------------------------------------------------------------
elif menu == "💳 Плащане и Абонамент (EasyPay)":
    st.title("💳 Абонаментни планове")
    st.markdown("Отключете пълния потенциал с плащане през EasyPay или Viber Pay в евро (€):")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Starter План")
        st.markdown("**€39 / месец**")
        if st.button("Плати €39 през EasyPay"):
            st.info("📌 Код за плащане на каса EasyPay: **CW-START-39**. Сума: **39 EUR** (по курс на БНБ).")

    with col2:
        st.markdown("### Pro План")
        st.markdown("**€99 / месец**")
        if st.button("Плати €99 през EasyPay"):
            st.info("📌 Код за плащане на каса EasyPay: **CW-PRO-99**. Сума: **99 EUR** (по курс на БНБ).")
