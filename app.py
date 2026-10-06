# В секцията за генератора добавяме визуализация и бутон за сваляне:
st.success("🎉 Текстът е успешно обработен и разбит на субтитри!")

# Тук добавяме компонент за видео плейър и сваляне (ако файлът е рендъриран на сървъра)
import os
output_file_path = "final_clipweave_video.mp4" # или името на генерирания файл

if os.path.exists(output_file_path):
    st.markdown("### 🎥 Вашето готово видео:")
    st.video(output_file_path)
    
    with open(output_file_path, "rb") as file:
        st.download_button(
            label="📥 Изтегли готовото видео (MP4)",
            data=file,
            file_name="ClipWeave_Video.mp4",
            mime="video/mp4"
        )
else:
    st.info("ℹ️ За момента субтитрите са напълно готови и синхронизирани. За да се запише и физическият видео файл на сървъра с всички графични ефекти и музика, стартирайте пълния MoviePy рендър скрипт през терминала или добавете пълния медиен пакет.")
