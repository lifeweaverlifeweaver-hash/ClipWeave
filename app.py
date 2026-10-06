import streamlit as st
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Безопасен импорт за различните версии на MoviePy (v1.x и v2.x)
try:
    from moviepy import VideoClip
except ImportError:
    try:
        from moviepy.editor import VideoClip
    except ImportError:
        VideoClip = None

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

# ФУНКЦИЯ ЗА СТАБИЛНО ГЕНЕРИРАНЕ НА ВИДЕО И СУБТИТРИ (ПИКСЕЛЕН МЕТОД С ГАРАНТИРАНА КИРИЛИЦА)
def generate_reliable_video(text: str, output_filename="clipweave_output.mp4"):
    width, height = 720, 1280  # 9:16 вертикален формат
    fps = 24
    duration = 5.0  # 5 секунди динамичен клип
    
    def make_frame(t):
        # Създаване на кадър с помощта на PIL (което позволява перфектно изобразяване на кирилица)
        img = Image.new("RGB", (width, height), color=(15, 23, 42)) # Тъмно син фон
        draw = ImageDraw.Draw(img)
        
        # Опит за зареждане на шрифт с кирилица от Linux системата
        font = None
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, 36)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()

        # Декоративен горен елемент (брендинг лента)
        draw.rectangle([40, 60, width - 40, 110], fill=(255, 75, 75))
        draw.text((60, 72), "CLIPWEAVE AI STUDIO", fill=(255, 255, 255), font=font)
        
        # Разделяне на дългия текст на редове, за да се побере на екрана
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 25:
                current_line = (current_line + " " + word).strip()
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
            
        # Рисуване на текста ред по ред с красив фон за контраст
        start_y = 450
        for i, line in enumerate(lines[:5]):  # Показваме до 5 реда
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                lw = bbox[2] - bbox[0]
                lh = bbox[3] - bbox[1]
            except:
                lw, lh = len(line) * 12, 30
                
            lx = (width - lw) // 2
            ly = start_y + (i * 60)
            
            # Черен фон зад всеки ред за максимална четимост
            draw.rectangle([lx - 20, ly - 10, lx + lw + 20, ly + lh + 15], fill=(0, 0, 0))
            # Бял текст
            draw.text((lx, ly), line, fill=(255, 255, 255), font=font)
            
        # Долен воден знак
        draw.text((40, height - 80), "Автоматично генерирано за TikTok & Reels", fill=(148, 163, 184), font=font)
        
        return np.array(img)

    # Използване на MoviePy за съединяване на кадрите във видеофайл
    if VideoClip is not None:
        animation = VideoClip(make_frame, duration=duration)
        animation.fps = fps
        animation.write_videofile(output_filename, codec="libx264", audio=False, logger=None)
        return output_filename
    else:
        raise ImportError("MoviePy не е инсталиран или зареден правилно в системата.")

# Странично меню (Sidebar)
st.sidebar.title("Клиентски и Админ Панел")
admin_password = st.sidebar.text_input("Парола за неограничен достъп:", type="password")
is_my_admin = (admin_password == "admin123")

if is_my_admin:
    st.sidebar.success("Администраторски режим: НАПЪЛНО БЕЗПЛАТНО И НЕОГРАНИЧЕНО")
else:
    st.sidebar.info(f"Използвани безплатни генерации: {st.session_state.free_uses} / {max_free}")

menu = st.sidebar.selectbox("Изберете модул:", [
    "Streamlit AI Агент и Автоматизация", 
    "AI Генератор на субтитри и клипове", 
    "Маркетплейс за задачи (€)", 
    "Моите Кампании", 
    "Плащане и Абонамент (EasyPay)"
])

# -------------------------------------------------------------
# МОДУЛ 1: STREAMLIT AI АГЕНТ И АВТОМАТИЗАЦИЯ
# -------------------------------------------------------------
if menu == "Streamlit AI Агент и Автоматизация":
    st.title("ClipWeave Autonomous AI Agent")
    st.markdown("### Вашият интелигентен помощник за анализ на съдържание и оптимизация на български език.")
    agent_topic = st.text_input("Въведете тема или продуктов ниш за анализ:", "натурална козметика и био продукти")
    
    if st.button("Стартирай AI анализ и генерирай стратегия"):
        if not agent_topic:
            st.warning("Моля, въведете тема.")
        else:
            st.success("AI агентът анализира успешно нишата!")
            st.markdown("---")
            st.markdown("#### Доклад и препоръки от агента:")
            st.markdown(f"1. **Целева аудитория в България:** Активни жени 20-45 г. в големите градове, търсещи чисти съставки.")
            st.markdown(f"2. **Препоръчителна структура за видеото:** Динамични субтитри на тъмен фон (9:16 формат).")
            st.markdown(f"3. **Генерирана топ кука (Hook):** *„Спрете да превъртате! Ето как {agent_topic} променя изцяло грижата за вас.“*")

# -------------------------------------------------------------
# МОДУЛ 2: AI ГЕНЕРАТОР НА СУБТИТРИ И КЛИПОВЕ
# -------------------------------------------------------------
elif menu == "AI Генератор на субтитри и клипове":
    st.title("ClipWeave Видео и Субтитри Генератор")
    st.markdown("### Създайте истинско вертикално видео (9:16) с вградени субтитри на български език.")

    platform = st.selectbox("Платформа:", ["TikTok", "Instagram Reels", "YouTube Shorts"])
    raw_input_text = st.text_area("Въведете вашия текст или сценарий за субтитрите:", 
                                  "Спрете да превъртате! Това е най-лесният начин да развиете проекта си бързо и без излишни разходи.")

    if st.button("Рендирай истински MP4 клип"):
        if not is_my_admin and st.session_state.free_uses >= max_free:
            st.error("Изчерпихте вашите 3 безплатни опита! За неограничен достъп преминете към платен план през EasyPay.")
        elif not raw_input_text:
            st.warning("Моля, въведете текст.")
        else:
            if not is_my_admin:
                st.session_state.free_uses += 1
            
            cleaned_text = clean_bulgarian_text(raw_input_text)
            
            try:
                with st.spinner("⏳ Създаване и рендиране на истинско видео (това отнема няколко секунди)..."):
                    video_filename = generate_reliable_video(cleaned_text, output_filename=f"clipweave_{platform.lower()}.mp4")
                
                st.success("🎉 Видеоклипът е успешно създаден и готов за гледане и сваляне!")
                st.video(video_filename)
                
                with open(video_filename, "rb") as file:
                    st.download_button(
                        label="📥 Свали готов MP4 клип",
                        data=file,
                        file_name=f"clipweave_{platform.lower()}_ready.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Грешка при рендирането: {e}")

            if not is_my_admin:
                remaining = max_free - st.session_state.free_uses
                st.info(f"Остават ви {remaining} безплатни опита.")

# -------------------------------------------------------------
# МОДУЛ 3: МАРКЕТПЛЕЙС БОРСА (€)
# -------------------------------------------------------------
elif menu == "Маркетплейс за задачи (€)":
    st.title("Маркетплейс за брандове и създатели")
    st.markdown("### Публикувайте задачи с фиксирани бюджети в **€** или кандидатствайте като създател.")

    with st.expander("Пусни нова задача"):
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
elif menu == "Моите Кампании":
    st.title("Управление на кампании")
    st.metric(label="Използвани генерации", value=st.session_state.free_uses)
    st.metric(label="Активни задачи в системата", value=len(st.session_state.campaigns))

# -------------------------------------------------------------
# МОДУЛ 5: ПЛАЩАНЕ (EasyPay)
# -------------------------------------------------------------
elif menu == "Плащане и Абонамент (EasyPay)":
    st.title("Абонаментни планове")
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
