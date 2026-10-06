import os
try:
    from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, AudioFileClip, VideoFileClip
except ImportError:
    pass

class BulgarianVideoRenderer:
    def __init__(self, output_resolution=(1080, 1920)):
        self.width, self.height = output_resolution

    def create_text_video(self, subtitles: list, background_color=(20, 20, 30), duration_per_line: float = 3.0, output_filename: str = "temp_video.mp4"):
        """
        Създава основното видео с динамични субтитри ред по ред.
        """
        print(f"[*] Рендиране на вертикално видео ({self.width}x{self.height})...")
        total_duration = len(subtitles) * duration_per_line
        
        try:
            background = ColorClip(size=(self.width, self.height), color=background_color).set_duration(total_duration)
            clips = [background]
            
            for i, text in enumerate(subtitles):
                start_time = i * duration_per_line
                txt_clip = (TextClip(text, fontsize=60, color='white', font='Arial', 
                                     size=(self.width - 100, None), method='caption')
                            .set_position('center')
                            .set_start(start_time)
                            .set_duration(duration_per_line))
                clips.append(txt_clip)
            
            final_video = CompositeVideoClip(clips)
            final_video.write_videofile(output_filename, fps=24, codec='libx264', audio_codec='aac')
            print(f"[+] Основният видео слой е готов.")
            return output_filename
            
        except Exception as e:
            print(f"[-] Грешка при видео рендъра: {e}")
            return None

    def add_background_music(self, video_filename: str, audio_filename: str, final_output: str = "final_clipweave_video.mp4"):
        """
        Добавя фонова музика към готовото видео и настройва времетраенето.
        """
        print([*] Интегриране на фонова музика...)
        try:
            video_clip = VideoFileClip(video_filename)
            audio_clip = AudioFileClip(audio_filename)
            
            # Ако музиката е по-дълга от клипа, я изрязваме точно до дължината на видеото
            if audio_clip.duration > video_clip.duration:
                audio_clip = audio_clip.subclip(0, video_clip.duration)
                
            # Закачаме аудиото към видеото
            final_video = video_clip.set_audio(audio_clip)
            final_video.write_videofile(final_output, fps=24, codec='libx264', audio_codec='aac')
            
            # Почистване на временния файл
            if os.path.exists(video_filename):
                os.remove(video_filename)
                
            print(f"[+] Финалният видео файл с музика и субтитри е готов: {final_output}")
            
        except Exception as e:
            print(f"[-] Грешка при добавяне на музика (уверете се, че аудио файлът съществува): {e}")

# --- Пълен тест на конвейера ---
if __name__ == "__main__":
    from linguistic_engine import BulgarianLinguisticEngine
    
    # 1. Генериране на субтитри през лингвистичния двигател
    engine = BulgarianLinguisticEngine()
    sample_text = "Спрете да превъртате! Това е най-лесният начин да развиете проекта си бързо и без излишни разходи."
    subtitles = engine.split_into_subtitles(sample_text, max_chars_per_line=25)
    
    # 2. Създаване на видео и добавяне на музика
    renderer = BulgarianVideoRenderer()
    temp_file = renderer.create_text_video(subtitles, output_filename="temp_v.mp4")
    
    if temp_file:
        # Пример: подаваме файлов път за фонова музика (напр. 'background.mp3')
        # renderer.add_background_music(temp_file, audio_filename="background.mp3", final_output="ClipWeave_Ready.mp4")
        pass
