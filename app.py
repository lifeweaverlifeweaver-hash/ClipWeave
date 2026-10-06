import streamlit as st

# Конфигурация на страницата
st.set_page_config(page_title="ClipWeave - UGC Platform & Marketplace", page_icon="🎬", layout="wide")

# Инициализация на базата данни в паметта на сесията (за демонстрация и тестове)
if "campaigns" not in st.session_state:
    st.session_state.campaigns = [
        {"id": 1, "brand": "BioGlow Cosmetics", "title": "TikTok UGC за нов серум", "budget": 120.0, "status": "Активна"},
        {"id": 2, "brand": "EcoHome BG", "title": "Reels видео за кухненски робот", "budget": 150.0, "status": "Активна"}
    ]

if "free_uses" not in st.session_state:
    st.session_state.free_uses = 0

max_free = 3

# Странично меню (Sidebar)
st.sidebar.title("🔐 Меню за управление")
admin_password = st.sidebar.text_input("Админ парола:", type="password")
is_my_admin = (admin_password == "admin123")

if is_my_admin:
    st.sidebar.success("✅ Администраторски режим: ПЪЛЕН И НЕОГРАНИЧЕНО БЕЗПЛАТЕН ДОСТЪП")
else:
    st.sidebar.info(f"Безплатни генерации: {st.session_state.free_uses} / {max_free}")

# Навигация в приложението
menu = st.sidebar.selectbox("Изберете модул:", ["🚀 AI Генератор на сценарии", "🛒 Маркетплейс за задачи (€)", "📊 Моите Кампании и Профил", "💳 Плащане и Абонамент (EasyPay)"])

# -------------------------------------------------------------
# МОДУЛ 1: AI ГЕНЕРАТОР НА СЦЕНАРИИ И ВИДЕА
# -------------------------------------------------------------
if menu == "🚀 AI Генератор на сценарии":
    st.title("🎬 ClipWeave AI Generator")
    st.markdown("### Създавайте професионални UGC сценарии за TikTok, Instagram Reels и YouTube Shorts за секунди!")

    platform = st.selectbox("Изберете платформа за видеото:", ["TikTok (Динамично и бързо)", "Instagram Reels (Естетично и лайфстайл)", "YouTube Shorts (Информативно и образователно)"])
    product_name = st.text_input("Име на продукта или услугата:")
    product_desc = st.text_area("Кратко описание, ключови ползи или линк към продукта:")

    if st.button("✨ Генерирай UGC сценарий с AI"):
        if not is_my_admin and st.session_state.free_uses >= max_free:
            st.error("⚠️ Изчерпихте вашите 3 безплатни опита! За да продължите, моля преминете към платен план през EasyPay в секцията за абонаменти.")
        elif not product_name:
            st.warning("Моля, въведете име на продукта.")
        else:
            if not is_my_admin:
                st.session_state.free_uses += 1
            
            st.success("🎉 Сценарият е успешно генериран!")
            
            st.markdown("---")
            st.markdown(f"#### 📱 Резултат за: *{platform}*")
            st.write(f"**🎯 Кука (Hook - първите 3 секунди):** Спрете да превъртате! Ако търсите начин да промените ежедневието си с {product_name}, това е за вас.")
            st.write(f"**💡 Основно тяло (Body):** Ето какво точно прави впечатление: {product_desc}. Изключително лесно за употреба и с гарантиран ефект.")
            st.write(f"**🔥 Призив за действие (CTA):** Кликнете линка в описанието или в профила, за да вземете своя продукт днес чрез ClipWeave!")
            
            if not is_my_admin:
                remaining = max_free - st.session_state.free_uses
                st.info(f"Остават ви {remaining} безплатни опита.")

# -------------------------------------------------------------
# МОДУЛ 2: МАРКЕТПЛЕЙС БОРСА
# -------------------------------------------------------------
elif menu == "🛒 Маркетплейс за задачи (€)":
    st.title("🛒 Маркетплейс за брандове и създатели")
    st.markdown("### Разгледайте актуалните задачи или пуснете нова кампания с бюджет в **€**.")

    with st.expander("➕ Пусни нова задача като бранд"):
        new_title = st.text_input("Заглавие на задачата:")
        new_brand = st.text_input("Име на вашия бранд/магазин:")
        new_budget = st.number_input("Бюджет в евро (€):", min_value=10.0, max_value=1000.0, value=50.0)
        
        if st.button("Публикувай задачата"):
            if new_title and new_brand:
                st.session_state.campaigns.append({"id": len(st.session_state.campaigns)+1, "brand": new_brand, "title": new_title, "budget": new_budget, "status": "Активна"})
                st.success("Успешно публикувахте задача в маркетплейса!")
            else:
                st.warning("Моля, попълнете заглавието и името на бранда.")

    st.markdown("---")
    st.markdown("### 📋 Активни задачи в платформата:")
    for camp in st.session_state.campaigns:
        st.info(f"**{camp['title']}** (Бранд: *{camp['brand']}*) — **Бюджет: €{camp['budget']}** [Статус: {camp['status']}]")
        if st.button(f"Кандидатствай по задача #{camp['id']}", key=f"apply_{camp['id']}"):
            st.success(f"Успешно кандидатствахте по задачата на {camp['brand']}! Очаквайте връзка.")

# -------------------------------------------------------------
# МОДУЛ 3: УПРАВЛЕНИЕ НА КАМПАНИИ И ПРОФИЛ
# -------------------------------------------------------------
elif menu == "📊 Моите Кампании и Профил":
    st.title("📊 Управление на кампании и клиентски профил")
    st.markdown("Тук можете да следите вашите създадени проекти, генерирани видео материали и статистика.")
    
    st.metric(label="Общо създадени сценарии", value=st.session_state.free_uses if not is_my_admin else "Неограничено")
    st.metric(label="Активни поръчки в маркетплейса", value=len(st.session_state.campaigns))
    
    st.markdown("---")
    st.subheader("⚙️ Настройки на профила")
    st.text_input("Име за контакт:", value="Tsvetelina Stoyanova" if is_my_admin else "Клиент")
    st.text_input("Имейл адрес:", value="lifeweaverlifeweaver@gmail.com" if is_my_admin else "client@example.com")
    st.button("Запази промените")

# -------------------------------------------------------------
# МОДУЛ ЛОКАЛНИ ПЛАЩАНИЯ (EasyPay)
# -------------------------------------------------------------
elif menu == "💳 Плащане и Абонамент (EasyPay)":
    st.title("💳 Абонаментни планове и плащане")
    st.markdown("За да отключите неограничен достъп и пълните възможности на ClipWeave, изберете план:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Starter План")
        st.markdown("**€39 / месец**")
        st.markdown("- Неограничени AI сценарии\n- Достъп до маркетплейса\n- Стандартни лимити")
        if st.button("Плати €39 през EasyPay"):
            st.info("📌 Код за плащане на каса EasyPay или Viber Pay: **CW-START-39**. Сума: **39 EUR** (по курс на БНБ). Достъпът се активира веднага след плащане.")

    with col2:
        st.markdown("### Pro / Agency План")
        st.markdown("**€99 / месец**")
        st.markdown("- Всичко от Starter\n- Приоритетни поръчки\n- Разширени AI инструменти")
        if st.button("Плати €99 през EasyPay"):
            st.info("📌 Код за плащане на каса EasyPay или Viber Pay: **CW-PRO-99**. Сума: **99 EUR** (по курс на БНБ).")
