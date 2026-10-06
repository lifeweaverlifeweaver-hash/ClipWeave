import streamlit as st
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, AudioFileClip
# Или ImageSequenceClip за рендиране кадър по кадър с MoviePy

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

# ФУНКЦИЯ ЗА ГЕНЕРИРАНЕ НА ИСТИНСКИ MP4 КЛИП СЪС СУБТИТРИ (ВИДЕО РЕНДЪР)
def generate_mp4_video(text: string, output_filename="clipweave_output.mp4"):
    width, height = 720, 1280  # Вертикален формат 9:16 (TikTok/Reels)
    fps = 24
    duration_per_line = 3.0
    
    subtitles = split_into_subtitles(text, max_chars=22)
    total_duration = max(len(subtitles) * duration_per_line, 3.0)
    
    def make_frame(t):
        # Създаване на динамичен фон (градиент или цвят)
        img = Image.new("RGB", (width, height), color=(15, 23, 42)) # Тъмно син/сив стил
        draw = ImageDraw.Draw(img)
        
        # Намиране на активния ред субтитри за съответната секунда t
        line_index = int(t // duration_per_line)
        if line_index >= len(subtitles):
            line_index = len(subtitles) - 1
        current_text = subtitles[line_index] if subtitles else text
        
        # Опит за зареждане на шрифт, с fallback към стандартен
        try:
            # Опит за стандартен дебел шрифт в Linux/Streamlit Cloud
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None

        # Отрисуване на декоративен горен елемент (брендинг)
        draw.rectangle([50, 100, width - 50, 140], fill=(255, 75, 75))
        
        # Центриране и изписване на текста на субтитрите
        # Използваме multi-line или стандартен draw.text
        bbox = draw.textbbox((0, 0), current_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Фон зад текста за четливост
        padding = 20
        draw.rectangle([x - padding, y - padding, x + text_width + padding, y + text_height + padding], fill=(0, 0, 0))
        draw.text((x, y), current_text, fill=(255, 255, 255), font=font)
        
        # Добавяне на водяен знак долу
        watermark = "ClipWeave AI Studio"
        draw.text((50, height - 100), watermark, fill=(148, 163, 184), font=font)
        
        return np.array(img)

    # Създаване на MoviePy клип
    animation = VideoClip(make_frame, duration=total_duration)
    animation.fps = fps
    
    # Запис във временен файл
    animation.write_videofile(output_filename, codec="libx264", audio=False, logger=None)
    return output_filename

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
    agent_topic = st.text_input("Въведете тема или продуктов ниш за анализ:", "натурална козметика и био продукти")
    
    if st.button("🧠 Стартирай AI анализ и генерирай стратегия"):
        if not agent_topic:
            st.warning("Моля, въведете тема.")
        else:
            st.success("✨ AI агентът анализира успешно нишата!")
            st.markdown("---")
            st.markdown("#### 📊 Доклад и препоръки от агента:")
            st.markdown(f"1. **Целева аудитория в България:** Активна жени 20-45 г. в големите градове, търсещи чисти съставки.")
            st.markdown(f"2. **Препоръчителна структура за видеото:** Динамични субтитри на тъмен фон (9:16 формат).")
            st.markdown(f"3. **Генерирана топ кука (Hook):** *„Спрете да превъртате! Ето как {agent_topic} променя изцяло грижата за вас.“*")

# -------------------------------------------------------------
# МОДУЛ 2: AI ГЕНЕРАТОР НА СУБТИТРИ И КЛИПОВЕ (С ИСТИНСКИ MP4 РЕНДЪР)
# -------------------------------------------------------------
elif menu == "🚀 AI Генератор на субтитри и клипове":
    st.title("🎬 ClipWeave Видео и Субтитри Генератор")
    st.markdown("### Създайте истинско вертикално видео (.mp4) с фон и синхронизирани субтитри на български език.")

    platform = st.selectbox("Платформа:", ["TikTok", "Instagram Reels", "YouTube Shorts"])
    raw_input_text = st.text_area("Въведете вашия текст или сценарий за субтитрите:", 
                                  "Спрете да превъртате! Това е най-лесният начин да развиете проекта си бързо и без излишни разходи.")

    if st.button("🚀 Рендирай и генерирай истински MP4 клип"):
        if not is_my_admin and st.session_state.free_uses >= max_free:
            st.error("⚠️ Изчерпихте вашите 3 безплатни опита! За неограничен достъп преминете към платен план през EasyPay.")
        elif not raw_input_text:
            st.warning("Моля, въведете текст.")
        else:
            if not is_my_admin:
                st.session_state.free_uses += 1
            
            cleaned_text = clean_bulgarian_text(raw_input_text)
            
            with st.spinner("⏳ Рендиране на видеоклипа (9:16) в ход... Моля, изчакайте няколко секунди."):
                video_filename = generate_mp4_video(cleaned_text, output_filename=f"clipweave_{platform.lower()}.mp4")
            
            st.success("🎉 Видеоклипът е успешно рендиран и готов за изтегляне!")
            
            # Представяне на видео плеър в Streamlit за преглед
            st.video(video_filename)
            
            # Бутон за сваляне на истинския MP4 файл
            with open(video_filename, "rb") as file:
                btn = st.download_button(
                    label="📥 Свали готови клип (.mp4)",
                    data=file,
                    file_name=f"clipweave_{platform.lower()}_ready.mp4",
                    mime="video/mp4"
                )

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
    st.metric(label="Използвани генерации", value=st.session_state.free_uses)
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
