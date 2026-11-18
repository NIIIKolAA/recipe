
import streamlit as st
import pandas as pd

# ==================================================
# 1. НАСТРОЙКА
# ==================================================

st.set_page_config(
    page_title="SaaS Advisor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. ДИЗАЙН
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #F3F6FB;
    font-family: 'Inter', sans-serif;
    color: #1E293B;
}

.block-container {
    max-width: 1550px;
    padding: 1rem 2rem 1rem 2rem !important;
}

header[data-testid="stHeader"] {
    background: transparent;
}

footer {
    visibility: hidden;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] * {
    color: #334155;
}

/* Заголовки */
h1, h2, h3, h4 {
    color: #172554 !important;
    font-weight: 800 !important;
}

/* Hero */
.hero {
    background: linear-gradient(110deg, #FFFFFF, #EAF4FF);
    border: 1px solid #DCEBFA;
    border-radius: 20px;
    padding: 20px 28px;
    margin-bottom: 17px;
    box-shadow: 0 4px 18px rgba(15,23,42,0.04);
}

.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 13px;
    color: #64748B;
}

/* Метрики */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 13px 16px;
    box-shadow: 0 3px 12px rgba(15,23,42,0.035);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 12px !important;
}

[data-testid="stMetricValue"] {
    color: #0284C7 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
}

/* Рекомендация */
.recommendation {
    background: linear-gradient(110deg,#E0F2FE,#F8FBFF);
    border: 1px solid #BAE6FD;
    border-left: 5px solid #0284C7;
    border-radius: 16px;
    padding: 15px 20px;
    margin: 14px 0;
}

.rec-label {
    color: #0369A1;
    font-size: 11px;
    font-weight: 800;
}

.rec-name {
    color: #172554;
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.rec-price {
    color: #0284C7;
    font-size: 23px;
    font-weight: 800;
}

/* Заголовки разделов */
.section-title {
    color: #172554;
    font-size: 18px;
    font-weight: 800;
    margin: 8px 0 10px 0;
}

/* Таблица */
[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    overflow: hidden;
}

/* График */
[data-testid="stVegaLiteChart"] {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 8px;
}

/* Уведомления */
.stAlert {
    border-radius: 13px;
}

/* Слайдер */
.stSlider [data-baseweb="slider"] {
    padding-top: 5px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 11px;
    padding: 12px;
    border-top: 1px solid #E2E8F0;
    margin-top: 15px;
}

/* Мобильная версия */
@media(max-width: 768px) {
    .block-container {
        padding: 0.7rem !important;
    }
    .hero-title {
        font-size: 23px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. ШАПКА
# ==================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">💎 SaaS Advisor</div>
    <div class="hero-subtitle">
        ✦ SMART TCO ANALYTICS · 2026
        <br>
        Интеллектуальная платформа сравнения облачных сервисов
        и подбора оптимального тарифа для вашей команды.
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# 4. ПАРАМЕТРЫ КОМАНДЫ
# ==================================================

with st.sidebar:

    st.markdown("## 💎 SaaS Advisor")
    st.caption("SMART TCO ANALYTICS")

    st.divider()

    st.markdown("### ⚙️ Параметры команды")

    team_size = st.slider(
        "👥 Количество сотрудников",
        10, 500, 100, 10
    )

    require_sso = st.checkbox(
        "🔐 Требуется SSO",
        value=False
    )

    st.divider()

    st.markdown("### ☁️ Информация")
    st.caption("Версия: 3.0")
    st.caption("Период: 2026")
    st.caption("© SaaS Advisor")


# ==================================================
# 5. БАЗА ТАРИФОВ
# ==================================================

tariffs = {
    "VK WorkSpace Базовый": {
        "price": 309,
        "max": 300,
        "sso": False,
        "icon": "📨"
    },
    "VK WorkSpace Расширенный": {
        "price": 499,
        "max": 500,
        "sso": True,
        "icon": "🚀"
    },
    "Яндекс 360 Минимальный": {
        "price": 319,
        "max": 250,
        "sso": False,
        "icon": "📁"
    },
    "Яндекс 360 Основной": {
        "price": 549,
        "max": 250,
        "sso": True,
        "icon": "⭐"
    },
    "Р7 пространство": {
        "price": 320,
        "max": 50,
        "sso": False,
        "icon": "🗂️"
    }
}


# ==================================================
# 6. РАСЧЕТ
# ==================================================

results = []
best_option = None
min_price = float("inf")

for name, params in tariffs.items():

    if team_size <= params["max"]:

        if require_sso and not params["sso"]:
            continue

        annual = params["price"] * team_size * 12

        results.append({
            "Платформа": params["icon"] + " " + name,
            "Цена / мес.": params["price"],
            "Стоимость / год": annual,
            "SSO": "✓ Да" if params["sso"] else "— Нет",
            "raw_name": name
        })

        if annual < min_price:
            min_price = annual
            best_option = name


# ==================================================
# 7. МЕТРИКИ
# ==================================================

st.markdown(
    '<div class="section-title">📊 Панель аналитики</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("👥 Команда", f"{team_size} чел.")

c2.metric(
    "🔐 SSO",
    "Включено" if require_sso else "Не требуется"
)

c3.metric("☁️ Тарифов найдено", len(results))

c4.metric(
    "💰 Минимум в год",
    f"{min_price:,.0f} ₽" if best_option else "—"
)


# ==================================================
# 8. РЕКОМЕНДАЦИЯ
# ==================================================

if best_option:

    st.markdown(f"""
    <div class="recommendation">
        <div class="rec-label">🏆 РЕКОМЕНДАЦИЯ СИСТЕМЫ · BEST CHOICE</div>
        <div class="rec-name">✨ {best_option}</div>
        <div class="rec-price">{min_price:,.0f} ₽ / год</div>
        <div style="color:#64748B;font-size:12px;">
            Наиболее доступный из подходящих тарифов
            с учетом параметров вашей команды.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 9. ТАБЛИЦА И ГРАФИК В ОДНОЙ СТРОКЕ
# ==================================================

col_table, col_chart = st.columns(
    [1.35, 1],
    gap="medium"
)

with col_table:

    st.markdown(
        '<div class="section-title">🏆 Сравнение тарифов</div>',
        unsafe_allow_html=True
    )

    if results:

        df = pd.DataFrame(results)

        display_df = df[
            ["Платформа", "Цена / мес.", "Стоимость / год", "SSO"]
        ].copy()

        def highlight_best(row):
            if best_option in row["Платформа"]:
                return [
                    "background-color: #E0F2FE; color: #075985; font-weight: bold"
                ] * len(row)
            return [""] * len(row)

        styled_df = display_df.style.apply(
            highlight_best,
            axis=1
        ).format({
            "Цена / мес.": "{:,.0f} ₽",
            "Стоимость / год": "{:,.0f} ₽"
        })

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            height=260
        )

    else:
        st.warning("Нет подходящих тарифов.")


with col_chart:

    st.markdown(
        '<div class="section-title">📈 Сравнение стоимости</div>',
        unsafe_allow_html=True
    )

    if results:

        chart_df = pd.DataFrame([
            {
                "Платформа": r["raw_name"],
                "Стоимость": r["Стоимость / год"]
            }
            for r in results
        ])

        chart_df = chart_df.sort_values(
            "Стоимость",
            ascending=True
        )

        st.bar_chart(
            chart_df.set_index("Платформа"),
            color="#38A6DF",
            height=260,
            use_container_width=True
        )


# ==================================================
# 10. ДОПОЛНИТЕЛЬНАЯ АНАЛИТИКА
# ==================================================

if results:

    average = sum(
        r["Стоимость / год"] for r in results
    ) / len(results)

    maximum = max(
        r["Стоимость / год"] for r in results
    )

    savings = maximum - min_price

    st.markdown(
        '<div class="section-title">🔍 Финансовая аналитика</div>',
        unsafe_allow_html=True
    )

    a1, a2, a3 = st.columns(3)

    a1.metric(
        "📊 Средняя стоимость",
        f"{average:,.0f} ₽"
    )

    a2.metric(
        "💸 Максимальная стоимость",
        f"{maximum:,.0f} ₽"
    )

    a3.metric(
        "🎯 Разница в стоимости",
        f"{savings:,.0f} ₽"
    )


# ==================================================
# 11. МЕТОДОЛОГИЯ
# ==================================================

with st.expander("📚 О проекте и методологии"):

    st.write("""
    **SaaS Advisor** — интеллектуальный инструмент
    для сравнения облачных платформ.

    Учитываемые параметры:

    - Количество сотрудников.
    - Стоимость лицензии.
    - Ограничение пользователей.
    - Поддержка SSO.
    - Годовая стоимость владения.

    **Формула:**

    TCO = Цена лицензии × Количество сотрудников × 12.

    Цены и лимиты являются демонстрационными
    и требуют проверки перед реальным внедрением.
    """)


# ==================================================
# 12. ФУТЕР
# ==================================================

st.markdown("""
<div class="footer">
    💎 <b>SaaS Advisor</b> · Intelligent SaaS Comparison Platform
    <br>
    © 2026 Academic Project · Smart TCO Analytics
</div>
""", unsafe_allow_html=True)
