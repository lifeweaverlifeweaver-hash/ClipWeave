import streamlit as st

# Конфигурация на страницата
st.set_page_config(page_title="ClipWeave - UGC Generator & Marketplace", page_icon="🎬", layout="wide")

# Администраторска проверка или вход за лична употреба (безплатно за вас)
st.sidebar.title("🔐 Меню за управление")
is_admin = st.sidebar.checkbox("Вход като Администратор (Пълен безплатен достъп)")

st.title("🎬 ClipWeave")
st.markdown("### Платформа „всичко в едно“ за генериране на UGC видеа и сценарии")

# Симулация на лимит за безплатни клипове (3 броя, следени по сесия/IP)
if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

max_free = 3

if not is_admin:
    st.info(f"Използвани безплатни генерации: {st.session_state.free_uses} / {max_free}")

# Основно поле за въвеждане
product_name = st.text_input("Име на продукта или услугата:")
product_desc = st.text_area("Кратко описание / Линк към продукта:")

if st.button("🚀 Генерирай UGC сценарий и клип"):
    if not is_admin and st.session_state.free_uses >= max_free:
        st.error("⚠️ Изчерпихте вашите 3 безплатни клипа! Моля, изберете платен план (Starter: €39/мес) през PayPal или EasyPay, за да продължите.")
    elif not product_name:
        st.warning("Моля, въведете име на продукта.")
    else:
        if not is_admin:
            st.session_state.free_uses += 1
        
        st.success("✨ Успешно генериран UGC сценарий!")
        
        # Резултат от AI генератора
        st.markdown("---")
        st.markdown("#### 📝 Първи вариант на сценарий (Hook + Body + CTA):")
        st.write(f"**Кука (Hook):** Спрете да превъртате, ако търсите перфектното решение за {product_name}!")
        st.write(f"**Съдържание (Body):** {product_desc} – този продукт напълно променя играта.")
        st.write("**Призив за действие (CTA):** Кликнете линка по-долу и го вземете още днес в ClipWeave!")
        
        if not is_admin:
            remaining = max_free - st.session_state.free_uses
            st.info(f"Остават ви {remaining} безплатни опита.")

# Секция за плащане и абонаменти (за външни клиенти)
st.markdown("---")
st.subheader("💳 Абонаментни планове (в €)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Starter План")
    st.markdown("**€39 / месец**")
    st.markdown("- Неограничени AI сценарии\n- Стандартни шаблони\n- Поддръжка на PayPal и EasyPay")
    if st.button("Купи Starter"):
        st.info("Пренасочване към защитена платежна страница (PayPal / EasyPay)...")

with col2:
    st.markdown("### Pro / Agency План")
    st.markdown("**€99 / месец**")
    st.markdown("- Всичко от Starter\n- Разширени AI аватари\n- Приоритетен маркетплейс за създатели")
    if st.button("Купи Pro"):
        st.info("Пренасочване към защитена платежна страница...")
