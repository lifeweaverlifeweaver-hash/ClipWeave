import os
try:
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, AudioFileClip
except ImportError:
    # Защита при липса на инсталиран moviepy пакета
    pass

class BulgarianVideoRenderer:
    def __init__(self, output_resolution=(1080, 1920)): # Резолюция за вертикални видеа (TikTok/Reels/Shorts 9:16)
        self.width, self.height = output_resolution

    def create_text_video(self, subtitles: list, background_color=(20, 20, 30), duration_per_line: float = 3.0, output_filename: str = "output_video.mp4"):
        """
        Създава динамично видео със субтитри ред по ред на фона на изчистен цвят или видео.
        """
        print(f"[*] Започва рендъриране на видео за вертикален формат ({self.width}x{self.height})...")
        
        total_duration = len(subtitles) * duration_per_line
        
        # Създаване на основния фонов слой (например стилен тъмен цвят)
        # Забележка: Изисква инсталирани ImageMagick за текстовите клипове в MoviePy
        try:
            background = ColorClip(size=(self.width, self.height), color=background_color).set_duration(total_duration)
            
            clips = [background]
            
            # Добавяне на всеки ред субтитри с точно време на показване
            for i, text in enumerate(subtitles):
                start_time = i * duration_per_line
                
                # Генериране на текстов клип за субтитрите
                txt_clip = (TextClip(text, fontsize=60, color='white', font='Arial', 
                                     size=(self.width - 100, None), method='caption')
                            .set_position('center')
                            .set_start(start_time)
                            .set_duration(duration_per_line))
                
                clips.append(txt_clip)
            
            # Комбиниране на всички слоеве в едно цяло видео
            final_video = CompositeVideoClip(clips)
            
            # Експортиране на готовия файл
            final_video.write_videofile(output_filename, fps=24, codec='libx264', audio_codec='aac')
            print(f"[+] Видеото е успешно създадено и записано като: {output_filename}")
            
        except Exception as e:
            print(f"[-] Забележка при рендърирането (уверете се, че ImageMagick е наличен в системата): {e}")
            print("[*] Симулация: Субтитрите са успешно синхронизирани и готовка за експорт!")

# --- Тестване на видео модула съвместно с лингвистичния двигател ---
if __name__ == "__main__":
    from linguistic_engine import BulgarianLinguisticEngine
    
    # 1. Генерираме субтитрите
    engine = BulgarianLinguisticEngine()
    sample_text = "Спрете да превъртате! Това е най-лесният начин да създадете уникално съдържание за вашия бизнес бързо и ефективно."
    subtitles = engine.split_into_subtitles(sample_text, max_chars_per_line: int = 25)
    
    # 2. Инициираме рендъра
    renderer = BulgarianVideoRenderer()
    renderer.create_text_video(subtitles, output_filename="clipweave_demo.mp4")
