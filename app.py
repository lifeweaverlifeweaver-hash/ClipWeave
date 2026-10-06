import streamlit as st

# Конфигурация на страницата
st.set_page_config(page_title="ClipWeave - UGC Generator", page_icon="🎬", layout="wide")

# Секция за администраторски (напълно безплатен и неограничен) достъп за вас
st.sidebar.title("🔐 Администрация")
admin_password = st.sidebar.text_input("Админ парола:", type="password")

# Задайте ваша лична парола тук (например "admin123")
is_my_admin = (admin_password == "admin123")

if is_my_admin:
    st.sidebar.success("✅ Администраторски режим: НАПЪЛНО БЕЗПЛАТНО И НЕОГРАНИЧЕНО!")

st.title("🎬 ClipWeave")
st.markdown("### Платформа за автоматично генериране на UGC сценарии и видеа")

# Управление на безплатните опита (3 броя за външни клиенти)
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

max_free = 3

if not is_my_admin:
    st.info(f"Използвани безплатни генерации: {st.session_state.free_uses} / {max_free}")

# Поле за въвеждане от клиента
product_name = st.text_input("Име на продукта или услугата:")
product_desc = st.text_area("Кратко описание или линк към продукта:")

if st.button("🚀 Генерирай UGC сценарий"):
    # Проверка дали клиентът е изчерпал безплатните си опити и не е администратор
    if not is_my_admin and st.session_state.free_uses >= max_free:
        st.error("⚠️ Изчерпихте вашите 3 безплатни опита! За да продължите, моля платете абонамент от €39 през EasyPay.")
    elif not product_name:
        st.warning("Моля, въведете име на продукта.")
    else:
        if not is_my_admin:
            st.session_state.free_uses += 1
        
        st.success("✨ Успешно генериран UGC сценарий!")
        
        # Резултат
        st.markdown("---")
        st.markdown("#### 📝 Генериран Сценарий:")
        st.write(f"**Кука (Hook):** Спрете да превъртате, ако търсите перфектното решение за {product_name}!")
        st.write(f"**Съдържание (Body):** {product_desc} – този продукт напълно променя играта.")
        st.write("**Призив за действие (CTA):** Вземете го от линка по-долу днес!")
        
        if not is_my_admin:
            remaining = max_free - st.session_state.free_uses
            st.info(f"Остават ви {remaining} безплатни опита.")

# Секция за плащане през EasyPay за клиенти, които искат неограничен достъп
st.markdown("---")
st.subheader("💳 Пълен достъп за клиенти (Плащане през EasyPay)")
st.markdown("След изчерпване на безплатните опити, абонирайте се за **Starter плана на стойност €39/месец**:")

if st.button("💵 Генерирай код за плащане през EasyPay (€39)"):
    st.info("📌 Вашият уникален код за плащане на каса EasyPay или през Viber Pay е: **CW-8844-EU**. Сума за плащане: **39 EUR** (по курс на БНБ в лева). След плащане достъпът ви се активира автоматично!")
