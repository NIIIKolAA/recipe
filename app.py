
import streamlit as st
import pandas as pd
import html

# ============================================================
# 1. НАСТРОЙКА СТРАНИЦЫ
# ============================================================

st.set_page_config(
    page_title="SaaS Advisor — Smart TCO",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. ПРЕМИАЛЬНЫЙ СВЕТЛЫЙ ДИЗАЙН
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #0284C7;
    --primary-light: #E0F2FE;
    --text: #1E293B;
    --muted: #64748B;
    --border: #E2E8F0;
}

/* Основной фон */
.stApp {
    background: #F3F6FB !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

/* Основной контейнер */
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

footer {
    visibility: hidden;
}

/* Боковая панель */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E8EDF4;
}

[data-testid="stSidebar"] * {
    color: #334155 !important;
}

/* Заголовки */
h1, h2, h3, h4 {
    color: #172554 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

p, label {
    color: #475569;
}

/* Главная карточка */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #FFFFFF 0%, #EFF6FF 100%);
    border: 1px solid #DBEAFE;
    border-radius: 24px;
    padding: 36px 40px;
    margin-bottom: 28px;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.045);
}

.hero h1 {
    font-size: 38px;
    margin: 0;
    color: #172554 !important;
}

.hero p {
    color: #64748B !important;
    font-size: 15px;
    line-height: 1.7;
    max-width: 750px;
}

.hero-tag {
    display: inline-block;
    background: #DBEAFE;
    color: #0369A1;
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* Карточки метрик */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5EAF2 !important;
    border-radius: 19px !important;
    padding: 19px !important;
    min-height: 112px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.035);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #93C5FD !important;
    box-shadow: 0 8px 24px rgba(2,132,199,0.08);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #0284C7 !important;
    font-size: 25px !important;
    font-weight: 800 !important;
}

/* Заголовки разделов */
.section-heading {
    color: #172554;
    font-size: 21px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* Карточка рекомендации */
.recommendation {
    background: linear-gradient(120deg, #EFF6FF, #FFFFFF);
    border: 1px solid #BFDBFE;
    border-left: 5px solid #0284C7;
    border-radius: 18px;
    padding: 22px 25px;
    margin: 18px 0 25px 0;
    box-shadow: 0 5px 20px rgba(2,132,199,0.05);
}

.recommendation-label {
    color: #0369A1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.recommendation-name {
    color: #172554;
    font-size: 22px;
    font-weight: 800;
    margin-top: 8px;
}

.recommendation-price {
    color: #0284C7;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

/* Кастомная таблица */
.table-container {
    background: #FFFFFF;
    border: 1px solid #E5EAF2;
    border-radius: 19px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(15,23,42,0.035);
    margin-top: 12px;
}

.premium-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-family: 'Inter', sans-serif;
}

.premium-table th {
    background: #F1F5F9;
    color: #475569;
    font-size: 12px;
    font-weight: 700;
    text-align: left;
    padding: 19px 17px;
    border-bottom: 1px solid #E2E8F0;
}

.premium-table td {
    padding: 17px;
    font-size: 13px;
    font-weight: 500;
    color: #334155;
    border-bottom: 1px solid #F1F5F9;
    background: #FFFFFF;
    transition: background 0.2s;
}

.premium-table tr:last-child td {
    border-bottom: none;
}

.premium-table tr:hover td {
    background: #F8FAFC;
}

/* Лучшая строка */
.premium-table tr.best-row td {
    background: #EFF8FF;
    color: #0369A1;
    font-weight: 700;
}

.premium-table tr.best-row:hover td {
    background: #E0F2FE;
}

/* Значки */
.plan-badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    background: #E0F2FE;
    color: #0369A1;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
}

.sso-yes {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    background: #DCFCE7;
    color: #15803D;
    font-size: 11px;
    font-weight: 700;
}

.sso-no {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    background: #F1F5F9;
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
}

.best-badge {
    display: inline-block;
    padding: 5px 9px;
    background: #DBEAFE;
    color: #1D4ED8;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 800;
}

/* График */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: #FFFFFF !important;
    border: 1px solid #E5EAF2 !important;
    border-radius: 19px !important;
    padding: 15px !important;
    box-shadow: 0 5px 20px rgba(15,23,42,0.035);
}

/* Уведомления */
.stAlert {
    border-radius: 15px !important;
}

/* Кнопки */
.stButton > button {
    border-radius: 11px !important;
    font-weight: 600 !important;
}

/* Раскрывающийся блок */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E5EAF2 !important;
    border-radius: 15px !important;
}

/* Разделители */
hr {
    border-color: #E2E8F0 !important;
}

/* Адаптация для телефона */
@media (max-width: 768px) {
    .hero {
        padding: 24px 20px;
    }

    .hero h1 {
        font-size: 28px;
    }

    .premium-table th,
    .premium-table td {
        padding: 11px 9px;
        font-size: 11px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. ШАПКА САЙТА
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ SMART TCO ANALYTICS · 2026</div>
    <h1>💎 SaaS Advisor</h1>
    <p>
        Интеллектуальная платформа для выбора облачной среды.
        Сравнивайте тарифы, анализируйте расходы и находите
        оптимальное решение для вашей команды.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 4. БОКОВАЯ ПАНЕЛЬ
# ============================================================

with st.sidebar:
    st.markdown("## 💎 SaaS Advisor")
    st.caption("SMART TCO ANALYTICS")
    st.divider()

    st.markdown("### ⚙️ Настройки команды")

    team_size = st.slider(
        "👥 Количество сотрудников",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )

    require_sso = st.checkbox(
        "🔐 Требуется SSO",
        value=False
    )

    st.divider()

    st.markdown("### ☁️ О платформе")
    st.caption("Версия системы: 2.0")
    st.caption("Расчетный период: 2026")
    st.caption("© 2026 SaaS Advisor")


# ============================================================
# 5. БАЗА ТАРИФОВ
# ============================================================

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


# ============================================================
# 6. ЛОГИКА РАСЧЕТА
# ============================================================

results = []
best_option = None
min_price = float("inf")

for name, params in tariffs.items():

    if team_size <= params["max"]:

        if require_sso and not params["sso"]:
            continue

        annual = params["price"] * team_size * 12

        results.append({
            "name": name,
            "price": params["price"],
            "annual": annual,
            "sso": params["sso"],
            "icon": params["icon"]
        })

        if annual < min_price:
            min_price = annual
            best_option = name


# ============================================================
# 7. ОСНОВНЫЕ МЕТРИКИ
# ============================================================

st.markdown(
    '<div class="section-heading">📊 Панель аналитики</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Размер команды",
    f"{team_size} чел."
)

col2.metric(
    "🔐 Требование SSO",
    "Да" if require_sso else "Нет"
)

col3.metric(
    "☁️ Доступные тарифы",
    len(results)
)

col4.metric(
    "💰 Минимум в год",
    f"{min_price:,.0f} ₽" if best_option else "—"
)


# ============================================================
# 8. КАРТОЧКА РЕКОМЕНДАЦИИ
# ============================================================

if best_option:

    st.markdown(f"""
    <div class="recommendation">
        <div class="recommendation-label">
            🏆 OPTIMAL SOLUTION · РЕКОМЕНДАЦИЯ СИСТЕМЫ
        </div>
        <div class="recommendation-name">
            {html.escape(best_option)}
        </div>
        <div class="recommendation-price">
            {min_price:,.0f} ₽ / год
        </div>
        <div style="color:#64748B;font-size:13px;margin-top:8px;">
            Оптимальный тариф по стоимости среди доступных
            вариантов с учетом заданных требований.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 9. СРАВНЕНИЕ ТАРИФОВ И ГРАФИК
# ============================================================

st.markdown(
    '<div class="section-heading">📈 Сравнение облачных решений</div>',
    unsafe_allow_html=True
)

if results:

    col_table, col_chart = st.columns(
        [1.25, 1],
        gap="large"
    )

    with col_table:

        st.markdown("#### 🏆 Сравнительная таблица")

        table_html = """
        <div class="table-container">
        <table class="premium-table">
        <thead>
        <tr>
            <th>Платформа</th>
            <th>Цена / мес.</th>
            <th>Стоимость / год</th>
            <th>SSO</th>
        </tr>
        </thead>
        <tbody>
        """

        for r in results:

            is_best = r["name"] == best_option
            row_class = 'class="best-row"' if is_best else ""

            sso_html = (
                '<span class="sso-yes">✓ Да</span>'
                if r["sso"]
                else '<span class="sso-no">— Нет</span>'
            )

            name_html = html.escape(r["name"])

            if is_best:
                name_html += (
                    ' <span class="best-badge">BEST</span>'
                )

            table_html += f"""
            <tr {row_class}>
                <td>{r["icon"]} {name_html}</td>
                <td>{r["price"]:,} ₽</td>
                <td>{r["annual"]:,} ₽</td>
                <td>{sso_html}</td>
            </tr>
            """

        table_html += """
        </tbody>
        </table>
        </div>
        """

        st.markdown(
            table_html,
            unsafe_allow_html=True
        )

    with col_chart:

        st.markdown("#### 📊 Стоимость тарифов")

        chart_df = pd.DataFrame([
            {
                "Платформа": r["name"],
                "Годовая стоимость": r["annual"]
            }
            for r in results
        ]).sort_values(
            "Годовая стоимость",
            ascending=True
        )

        st.bar_chart(
            chart_df.set_index("Платформа"),
            color="#38A6DF",
            height=310,
            use_container_width=True
        )

else:

    st.warning(
        "⚠️ Для заданных параметров нет подходящих тарифов. "
        "Измените количество сотрудников или отключите требование SSO."
    )


# ============================================================
# 10. ДЕТАЛЬНАЯ АНАЛИТИКА
# ============================================================

if results:

    st.markdown(
        '<div class="section-heading">🔍 Детальная аналитика</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    average = sum(r["annual"] for r in results) / len(results)

    max_price = max(r["annual"] for r in results)

    savings = max_price - min_price

    col1.metric(
        "📊 Средняя стоимость",
        f"{average:,.0f} ₽"
    )

    col2.metric(
        "💸 Максимальная стоимость",
        f"{max_price:,.0f} ₽"
    )

    col3.metric(
        "🎯 Потенциальная экономия",
        f"{savings:,.0f} ₽"
    )


# ============================================================
# 11. МЕТОДОЛОГИЯ
# ============================================================

with st.expander("📚 О проекте и методологии расчета"):

    st.markdown("""
    ### 💎 SaaS Advisor

    Аналитический инструмент для выбора облачной
    среды совместной работы.

    **Какие параметры учитываются:**

    - 👥 Количество сотрудников.
    - 💰 Стоимость лицензии.
    - ☁️ Максимальное количество пользователей.
    - 🔐 Наличие поддержки SSO.
    - 📊 Совокупная годовая стоимость владения.

    **Формула расчета:**

    Годовая стоимость = Цена лицензии ×
    Количество сотрудников × 12.

    **Цель проекта:**

    Помочь организациям выбрать подходящую
    облачную платформу с учетом бюджета,
    размера команды и требований безопасности.

    ⚠️ Цены и ограничения представлены в демонстрационной
    базе проекта. Перед реальным внедрением необходимо
    проверить актуальные условия поставщиков.
    """)


# ============================================================
# 12. ФУТЕР
# ============================================================

st.markdown("""
<div style="
    border-top:1px solid #E2E8F0;
    margin-top:45px;
    padding:25px 10px;
    text-align:center;
">
    <div style="
        font-size:19px;
        font-weight:800;
        color:#172554;
    ">
        💎 SaaS Advisor
    </div>

    <div style="
        font-size:12px;
        color:#94A3B8;
        margin-top:7px;
    ">
        Intelligent SaaS Comparison Platform
    </div>

    <div style="
        font-size:11px;
        color:#CBD5E1;
        margin-top:10px;
    ">
        © 2026 Academic Project · Smart TCO Analytics
    </div>
</div>
""", unsafe_allow_html=True)
