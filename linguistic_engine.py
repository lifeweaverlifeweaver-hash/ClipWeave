import re

class BulgarianLinguisticEngine:
    def __init__(self):
        # Персонализиран речник за корекция на специфични термини и избягване на буквализъм
        self.custom_glossary = {
            "клиентски опит": "потребителско изживяване",
            "лайк": харесване,
            "шервам": споделям,
            "бууствам": промотирам
        }
        
        # Шаблони за мощни куки (Hooks) на естествен български език
        self.hook_templates = [
            "Спрете да превъртате, ако все още търсите решение за {topic}!",
            "Това е тайният трик за {topic}, който никой друг няма да ви каже.",
            "Ако искате да промените изцяло подхода си към {topic}, вижте това."
        ]

    def clean_and_format_text(self, text: str) -> str:
        """Почиства текста и го подготвя за кратки субтитри (разделя го на оптимални редове)"""
        text = text.strip()
        # Прилагане на речника за корекции
        for wrong, correct in self.custom_glossary.items():
            text = text.replace(wrong, correct)
            
        # Премахване на излишни интервали
        text = re.sub(r'\s+', ' ', text)
        return text

    def generate_hook(self, topic: str, style_index: int = 0) -> str:
        """Генерира първите 3 секунди (кука) на база шаблоните"""
        template = self.hook_templates[style_index % len(self.hook_templates)]
        return template.format(topic=topic)

    def split_into_subtitles(self, text: str, max_chars_per_line: int = 30) -> list:
        """Разбива дълъг текст на кратки редове, идеални за динамични субтитри без глас"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line = (current_line + " " + word).strip()
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
            
        return lines

# --- Тестване на модула ---
if __name__ == "__main__":
    engine = BulgarianLinguisticEngine()
    
    sample_topic = "автоматичното създаване на съдържание"
    raw_text = "Клиентският опит е най-важното нещо. Когато шервате видеата си, вие бууствате своя бранд бързо и лесно."
    
    print("--- ТЕСТ НА ЛИНГВИСТИЧНИЯ ДВИГАТЕЛ ---")
    print("1. Генерирана кука:", engine.generate_hook(sample_topic))
    print("2. Почистен текст:", engine.clean_and_format_text(raw_text))
    print("3. Разбити субтитри за екран:", engine.split_into_subtitles(raw_text))
