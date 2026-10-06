import streamlit as st
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Безопасен импорт за MoviePy спрямо версията му
try:
    from moviepy.editor import VideoClip
except ImportError:
    try:
        from moviepy import VideoClip
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

# ФУНКЦИЯ ЗА ГЕНЕРИРАНЕ НА ВИДЕО С ПЪЛНА ПОДДРЪЖКА НА КИРИЛИЦА
def generate_mp4_video(text: str, output_filename="clipweave_output.mp4"):
    width, height = 720, 1280  # Вертикален формат 9:16 (TikTok/Reels)
    fps = 24
    duration_per_line = 3.0
    
    subtitles = split_into_subtitles(text, max_chars=22)
    total_duration = max(len(subtitles) * duration_per_line, 3.0)
    
    def make_frame(t):
        img = Image.new("RGB", (width, height), color=(15, 23, 42))  # Тъмно син фон
        draw = ImageDraw.Draw(img)
        
        line_index = int(t // duration_per_line)
        if line_index >= len(subtitles):
            line_index = len(subtitles) - 1
        current_text = subtitles[line_index] if subtitles else text
        
        # Интелигентно търсене на TrueType шрифт с кирилица в Linux/Streamlit Cloud
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
                    font = ImageFont.truetype(path, 42)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()

        # Декоративен горен елемент (брендинг линия)
        draw.rectangle([50, 80, width - 50, 120], fill=(255, 75, 75))
        
        # Центриране на текста на субтитрите
        try:
            bbox = draw.textbbox((0, 0), current_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width, text_height = len(current_text) * 15, 40
            
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Черен плътен фон зад текста за отличен контраст
        padding = 24
        draw.rectangle([x - padding, y - padding, x + text_width + padding, y + text_height + padding], fill=(0, 0, 0))
        
        # Изписване на кирилицата с бял цвят
        draw.text((x, y), current_text, fill=(255, 255, 255), font=font)
        
        # Воден знак долу вляво
        watermark = "ClipWeave AI Studio"
        draw.text((50, height - 80), watermark, fill=(148, 163, 184), font=font)
        
        return np.array(img)

    if VideoClip is not None:
        animation = VideoClip(make_frame, duration=total_duration)
        animation.fps = fps
        animation.write_videofile(output_filename, codec="libx264", audio=False, logger=None)
        return output_filename
    else:
        raise ImportError("MoviePy не е инсталиран правилно на сървъра.")

# Странично меню (Sidebar)
st.sidebar.title("🔐 Клиентски и Админ Панел")
admin_password = st.sidebar.text_input("Парола за неограничен достъп:", type="password")
is_my_admin = (admin_password == "admin123")

if is_my_admin:
    st.sidebar.success("✅ Администраторски режим: НАП
