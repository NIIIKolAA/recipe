
import streamlit as st
import pandas as pd

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
# 2. ПРЕМИАЛЬНЫЙ ДИЗАЙН CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d19;
    --panel: #111a2b;
    --panel-light: #17243a;
    --accent: #38bdf8;
    --purple: #818cf8;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --green: #34d399;
    --border: rgba(148,163,184,0.14);
}

/* ОСНОВНОЙ ФОН */

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, rgba(56,189,248,0.10), transparent 35%),
        radial-gradient(ellipse at 90% 10%, rgba(129,140,248,0.10), transparent 35%),
        #080d19 !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* УБИРАЕМ ЛИШНИЕ ЭЛЕМЕНТЫ */

header[data-testid="stHeader"] {
    background: transparent;
}

footer {
    visibility: hidden;
}

/* БОКОВАЯ ПАНЕЛЬ */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a2c, #0b1220) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* ЗАГОЛОВКИ */

h1, h2, h3, h4 {
    color: #f8fafc !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
}

p, label {
    color: #cbd5e1;
}

/* ГЛАВНАЯ ШАПКА */

.hero {
    background:
        linear-gradient(120deg,
        rgba(30,41,59,0.95),
        rgba(23,37,65,0.85));
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 22px;
    padding: 35px 38px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
}

.hero:after {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    right: -70px;
    top: -110px;
    background: rgba(56,189,248,0.13);
    filter: blur(65px);
    border-radius: 50%;
}

.hero-tag {
    display: inline-block;
    padding: 6px 12px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 30px;
    color: #7dd3fc;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 38px;
    margin: 0;
    background: linear-gradient(90deg,#ffffff,#7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 12px;
    margin-bottom: 0;
    max-width: 650px;
    line-height: 1.7;
}

/* КАРТОЧКИ МЕТРИК */

[data-testid="stMetric"] {
    background: linear-gradient(145deg,#142137,#101a2b) !important;
    border: 1px solid rgba(56,189,248,0.17) !important;
    border-radius: 17px !important;
    padding: 20px !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.16);
    min-height: 115px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #7dd3fc !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* ЗАГОЛОВКИ РАЗДЕЛОВ */

.section-title {
    font-size: 19px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 32px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #64748b;
    font-size: 12px;
    margin-bottom: 17px;
}

/* ПАНЕЛЬ РЕКОМЕНДАЦИИ */

.recommendation {
    background: linear-gradient(120deg,
        rgba(6,78,100,0.35),
        rgba(30,41,59,0.9));
    border: 1px solid rgba(52,211,153,0.35);
    border-radius: 18px;
    padding: 23px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.recommendation-label {
    color: #34d399;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.recommendation-name {
    color: #f0fdf4;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 8px;
}

.recommendation-price {
    color: #6ee7b7;
    font-size: 27px;
    font-weight: 800;
}

.recommendation-description {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}

/* ТАБЛИЦА */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(56,189,248,0.18);
    border-radius: 14px;
    overflow: hidden;
}

/* ГРАФИК */

[data-testid="stVegaLiteChart"] {
    background: rgba(17,26,43,0.7);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 12px;
}

/* КНОПКИ */

.stButton button {
    background: linear-gradient(90deg,#0284c7,#6366f1);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 700;
    padding: 10px 20px;
    transition: 0.2s;
}

.stButton button:hover {
    border: none;
    filter: brightness(1.15);
}

/* ПОЛЯ ВВОДА */

.stSlider, .stCheckbox {
    padding-top: 8px;
    padding-bottom: 8px;
}

/* ИНФОРМАЦИОННЫЕ БЛОКИ */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* НИЖНИЙ КОЛОНТИТУЛ */

.footer {
    border-top: 1px solid var(--border);
    margin-top: 45px;
    padding-top: 20px;
    text-align: center;
    color: #64748b;
    font-size: 11px;
}

@media(max-width: 768px) {
    .hero {
        padding: 24px;
    }
    .hero h1 {
        font-size: 28px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. ШАПКА САЙТА
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-tag">
        ✦ SMART BUSINESS ANALYTICS
    </div>

    <h1>💎 SaaS Advisor</h1>

    <p>
        Интеллектуальная платформа для сравнения облачных сервисов.
        Анализируйте стоимость владения, проверяйте поддержку SSO
        и выбирайте оптимальное решение для вашей команды.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# 4. БОКОВАЯ ПАНЕЛЬ
# ============================================================

with st.sidebar:

    st.markdown("## 💎 SaaS Advisor")

    st.caption("SMART TCO ANALYTICS")

    st.markdown("---")

    st.markdown("### ⚙️ Параметры команды")

    team_size = st.slider(
        "Количество сотрудников",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )

    require_sso = st.checkbox(
        "Требуется SSO",
        value=False,
        help="Показывать только тарифы с поддержкой единого входа."
    )

    st.markdown("---")

    st.markdown("### 📋 Информация")

    st.caption("Версия системы: 1.0")
    st.caption("Расчетный период: 2026 год")
    st.caption("Методология: TCO")

    st.markdown("---")

    st.caption("© 2026 SaaS Advisor")
    st.caption("Academic project | IT Service Management")


# ============================================================
# 5. БАЗА ТАРИФОВ
# ============================================================

tariffs = {

    "VK WorkSpace Базовый": {
        "price": 309,
        "max": 300,
        "sso": False
    },

    "VK WorkSpace Расширенный": {
        "price": 499,
        "max": 500,
        "sso": True
    },

    "Яндекс 360 Минимальный": {
        "price": 319,
        "max": 250,
        "sso": False
    },

    "Яндекс 360 Основной": {
        "price": 549,
        "max": 250,
        "sso": True
    },

    "Р7 пространство": {
        "price": 320,
        "max": 50,
        "sso": False
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

        monthly = params["price"] * team_size

        results.append({

            "Платформа": name,

            "Цена за пользователя": params["price"],

            "Стоимость в месяц": monthly,

            "Стоимость в год": annual,

            "SSO": "Да" if params["sso"] else "Нет"

        })

        if annual < min_price:

            min_price = annual

            best_option = name


# ============================================================
# 7. ОСНОВНЫЕ МЕТРИКИ
# ============================================================

st.markdown("""
<div class="section-title">📊 Панель аналитики</div>
<div class="section-subtitle">
    Основные показатели выбранной конфигурации
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Размер команды",
        f"{team_size} чел."
    )

with col2:

    st.metric(
        "Требование SSO",
        "Включено" if require_sso else "Не требуется"
    )

with col3:

    st.metric(
        "Доступные тарифы",
        len(results)
    )

with col4:

    st.metric(
        "Минимум в год",
        f"{min_price:,.0f} ₽" if best_option else "—"
    )


# ============================================================
# 8. РЕКОМЕНДАЦИЯ
# ============================================================

if best_option:

    st.markdown(f"""
    <div class="recommendation">

        <div class="recommendation-label">
            🏆 OPTIMAL SOLUTION
        </div>

        <div class="recommendation-name">
            {best_option}
        </div>

        <div class="recommendation-price">
            {min_price:,.0f} ₽ / год
        </div>

        <div class="recommendation-description">
            Оптимальный тариф по критерию минимальной годовой стоимости
            среди доступных вариантов с учетом заданных ограничений.
        </div>

    </div>
    """, unsafe_allow_html=True)

else:

    st.error(
        "Для выбранных параметров нет доступных тарифов. "
        "Измените количество сотрудников или требования SSO."
    )


# ============================================================
# 9. СРАВНЕНИЕ ТАРИФОВ И ГРАФИК
# ============================================================

st.markdown("""
<div class="section-title">📈 Сравнение решений</div>
<div class="section-subtitle">
    Сопоставление стоимости и функциональных возможностей платформ
</div>
""", unsafe_allow_html=True)


if results:

    col_table, col_chart = st.columns(
        [1.3, 1],
        gap="large"
    )

    with col_table:

        st.markdown("#### 🏆 Сравнение тарифов")

        df = pd.DataFrame(results)

        display_df = df.copy()

        display_df["Цена за пользователя"] = (
            display_df["Цена за пользователя"].map(
                lambda x: f"{x:,.0f} ₽"
            )
        )

        display_df["Стоимость в месяц"] = (
            display_df["Стоимость в месяц"].map(
                lambda x: f"{x:,.0f} ₽"
            )
        )

        display_df["Стоимость в год"] = (
            display_df["Стоимость в год"].map(
                lambda x: f"{x:,.0f} ₽"
            )
        )

        def highlight_best(row):

            if row["Платформа"] == best_option:

                return [
                    "background-color: rgba(56,189,248,0.18); "
                    "color: #38bdf8; font-weight: bold;"
                ] * len(row)

            return [""] * len(row)

        st.dataframe(

            display_df.style.apply(
                highlight_best,
                axis=1
            ),

            use_container_width=True,

            hide_index=True

        )

        st.caption(
            "Голубым цветом выделено наиболее экономичное решение."
        )

    with col_chart:

        st.markdown("#### 📊 Годовые расходы")

        chart_df = pd.DataFrame({

            "Платформа": [r["Платформа"] for r in results],

            "Годовая стоимость": [
                r["Стоимость в год"] for r in results
            ]

        })

        chart_df = chart_df.sort_values(
            "Годовая стоимость",
            ascending=True
        )

        st.bar_chart(

            chart_df.set_index("Платформа"),

            color="#38bdf8",

            height=340,

            use_container_width=True

        )

        st.caption(
            "Сравнение совокупных годовых расходов на команду."
        )


# ============================================================
# 10. ДОПОЛНИТЕЛЬНАЯ АНАЛИТИКА
# ============================================================

if results:

    st.markdown("""
    <div class="section-title">🔍 Детальная аналитика</div>
    <div class="section-subtitle">
        Дополнительные показатели стоимости обслуживания
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        average_price = sum(
            r["Стоимость в год"] for r in results
        ) / len(results)

        st.metric(
            "Средняя стоимость в год",
            f"{average_price:,.0f} ₽"
        )

    with col2:

        max_price = max(
            r["Стоимость в год"] for r in results
        )

        difference = max_price - min_price

        st.metric(
            "Разница между тарифами",
            f"{difference:,.0f} ₽"
        )


# ============================================================
# 11. МЕТОДОЛОГИЯ ПРОЕКТА
# ============================================================

with st.expander("📚 О проекте и методологии расчета"):

    st.markdown("""
    ### SaaS Advisor

    SaaS Advisor — аналитический инструмент для выбора
    облачной среды совместной работы.

    **Система учитывает:**

    - Количество сотрудников организации.
    - Стоимость лицензии на одного пользователя.
    - Максимально допустимое количество пользователей.
    - Наличие поддержки SSO.
    - Совокупную годовую стоимость владения (TCO).

    **Формула расчета:**

    Годовая стоимость = Цена лицензии × Количество сотрудников × 12.

    **Критерий выбора:**

    Система выбирает тариф с минимальной годовой стоимостью
    среди вариантов, удовлетворяющих заданным ограничениям.

    Примечание: цены и ограничения в базе являются исходными
    данными прототипа. Перед реальным использованием необходимо
    проверить их по актуальным предложениям поставщиков.
    """)


# ============================================================
# 12. ФУТЕР
# ============================================================

st.markdown("""
<div class="footer">

    <b>💎 SaaS Advisor</b><br><br>

    Intelligent SaaS Comparison Platform<br>

    © 2026 Academic Project | IT Service Management

</div>
""", unsafe_allow_html=True)
