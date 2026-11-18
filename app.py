
import streamlit as st
import pandas as pd

# =====================================================
# 1. НАСТРОЙКА СТРАНИЦЫ
# =====================================================

st.set_page_config(
    page_title="SaaS Advisor | Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. ПРЕМИАЛЬНЫЙ CSS-ДИЗАЙН
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #172554 0%, transparent 45%),
        radial-gradient(ellipse at 90% 10%, #312e81 0%, transparent 35%),
        #080d1c;
    color: #f8fafc;
}

header[data-testid="stHeader"] {
    background: rgba(8, 13, 28, 0.7);
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.96);
    border-right: 1px solid rgba(129, 140, 248, 0.2);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

[data-testid="stSidebar"] h2 {
    color: #818cf8 !important;
}

/* HEADER */

.hero {
    background: linear-gradient(
        135deg,
        rgba(30, 41, 90, 0.85),
        rgba(49, 46, 129, 0.55)
    );
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 24px;
    padding: 40px 35px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 15px 50px rgba(0,0,0,0.25);
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

/* SECTION TITLES */

.section-title {
    color: #e0e7ff;
    font-size: 23px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 20px;
}

/* METRICS */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30, 41, 70, 0.9),
        rgba(30, 41, 59, 0.65)
    );
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #818cf8;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}

/* INPUTS */

.stSlider label,
.stCheckbox label {
    color: #e2e8f0 !important;
    font-weight: 500;
}

.stSlider [data-testid="stThumbValue"] {
    color: #38bdf8;
}

/* BUTTONS */

.stButton button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton button:hover {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transform: translateY(-2px);
}

/* TABLE */

.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    background: rgba(15, 23, 42, 0.85);
    border-radius: 15px;
    overflow: hidden;
    border: 1px solid rgba(99, 102, 241, 0.25);
}

.custom-table th {
    background: rgba(49, 46, 129, 0.55);
    color: #93c5fd;
    padding: 18px;
    text-align: left;
    font-size: 14px;
    border-bottom: 1px solid rgba(129, 140, 248, 0.3);
}

.custom-table td {
    padding: 17px 18px;
    color: #e2e8f0;
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.custom-table tr:hover {
    background: rgba(99, 102, 241, 0.1);
}

.custom-table tr.best-row {
    background: rgba(14, 165, 233, 0.14);
}

.custom-table tr.best-row td {
    color: #38bdf8;
    font-weight: 700;
}

/* WINNER CARD */

.winner {
    background: linear-gradient(
        120deg,
        rgba(14, 116, 144, 0.25),
        rgba(79, 70, 229, 0.25)
    );
    border: 1px solid rgba(56, 189, 248, 0.45);
    border-radius: 18px;
    padding: 24px;
    margin-top: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.winner h3 {
    color: #38bdf8;
    margin-bottom: 10px;
}

.winner p {
    color: #e2e8f0;
    margin-bottom: 0;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin-top: 50px;
}

@media (max-width: 768px) {
    .hero {
        padding: 25px 15px;
    }

    .hero h1 {
        font-size: 29px;
    }

    .custom-table th,
    .custom-table td {
        padding: 10px;
        font-size: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. ШАПКА САЙТА
# =====================================================

st.markdown("""
<div class="hero">
    <h1>💎 SaaS Advisor</h1>
    <p>
        Интеллектуальная платформа для выбора облачных решений
        и расчёта совокупной стоимости владения (TCO).
    </p>
    <p>
        PREMIUM EDITION · 2026
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 4. ВВОД ДАННЫХ
# =====================================================

with st.sidebar:

    st.markdown("## ⚙️ Настройки проекта")

    st.markdown("---")

    st.markdown("### 👥 Параметры команды")

    team_size = st.slider(
        "Количество сотрудников",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )

    require_sso = st.checkbox(
        "Требуется SSO (единый вход)"
    )

    st.markdown("---")

    st.markdown("### 🔐 Безопасность")

    if require_sso:
        st.info("Учитываются только тарифы с поддержкой SSO.")
    else:
        st.caption("SSO не является обязательным требованием.")

    st.markdown("---")

    st.caption("SaaS Advisor Premium")
    st.caption("© 2026 Курсовой проект")
    st.caption("Управление IT-сервисом")


# =====================================================
# 5. БАЗА ТАРИФОВ
# =====================================================

tariffs = {

    "VK WorkSpace Базовый": {
        "price": 309,
        "max_users": 300,
        "sso": False
    },

    "VK WorkSpace Расширенный": {
        "price": 499,
        "max_users": 500,
        "sso": True
    },

    "Яндекс 360 Минимальный": {
        "price": 319,
        "max_users": 250,
        "sso": False
    },

    "Яндекс 360 Основной": {
        "price": 549,
        "max_users": 250,
        "sso": True
    },

    "Р7 пространство": {
        "price": 320,
        "max_users": 50,
        "sso": False
    }

}


# =====================================================
# 6. ЛОГИКА РАСЧЁТА
# =====================================================

results = []

best_option = None

min_price = float("inf")

for name, params in tariffs.items():

    if team_size <= params["max_users"]:

        if require_sso and not params["sso"]:
            continue

        annual_cost = params["price"] * team_size * 12

        results.append({

            "name": name,

            "price": params["price"],

            "cost": annual_cost,

            "sso": "Да" if params["sso"] else "Нет"

        })

        if annual_cost < min_price:

            min_price = annual_cost

            best_option = name


# =====================================================
# 7. РЕЗУЛЬТАТЫ АНАЛИЗА
# =====================================================

st.markdown(
    '<div class="section-title">📊 Аналитика и результаты</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="👥 Размер команды",
        value=f"{team_size} чел."
    )

with col2:

    st.metric(
        label="🔐 Требование SSO",
        value="Да" if require_sso else "Нет"
    )

with col3:

    if best_option:

        st.metric(
            label="💰 Лучшая цена за год",
            value=f"{min_price:,} ₽"
        )

    else:

        st.metric(
            label="💰 Лучшая цена",
            value="—"
        )


# =====================================================
# 8. ТАБЛИЦА И ОПТИМАЛЬНЫЙ ВЫБОР
# =====================================================

st.markdown(
    '<div class="section-title">🏆 Сравнение облачных платформ</div>',
    unsafe_allow_html=True
)

if results:

    html_table = """
    <table class="custom-table">
        <tr>
            <th>Платформа и тариф</th>
            <th>Цена за пользователя / месяц</th>
            <th>Стоимость за год</th>
            <th>Поддержка SSO</th>
            <th>Статус</th>
        </tr>
    """

    for row in results:

        is_best = row["name"] == best_option

        row_class = "best-row" if is_best else ""

        status = "🏆 Лучший выбор" if is_best else "Доступен"

        html_table += f"""
        <tr class="{row_class}">
            <td>{row['name']}</td>
            <td>{row['price']:,} ₽</td>
            <td>{row['cost']:,} ₽</td>
            <td>{'✅ Да' if row['sso'] == 'Да' else '❌ Нет'}</td>
            <td>{status}</td>
        </tr>
        """

    html_table += "</table>"

    st.markdown(
        html_table,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="winner">
        <h3>🏆 Оптимальный выбор</h3>
        <p>
            Рекомендуемая платформа:
            <b>{best_option}</b>
        </p>
        <p>
            Годовая стоимость обслуживания:
            <b>{min_price:,} ₽</b>
        </p>
        <p>
            Размер команды: {team_size} сотрудников.
        </p>
        <p>
            Требование SSO: {"Да" if require_sso else "Нет"}.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Дополнительная аналитика

    st.markdown(
        '<div class="section-title">📈 Структура расходов</div>',
        unsafe_allow_html=True
    )

    chart_data = pd.DataFrame({

        "Платформа": [r["name"] for r in results],

        "Годовая стоимость": [r["cost"] for r in results]

    })

    st.bar_chart(
        chart_data.set_index("Платформа"),
        color="#38bdf8"
    )

    # Экспорт результатов

    st.markdown("### 📥 Экспорт результатов")

    export_df = pd.DataFrame([

        {
            "Платформа": r["name"],
            "Цена за пользователя в месяц": r["price"],
            "Стоимость за год": r["cost"],
            "SSO": r["sso"],
            "Рекомендация": "Лучший выбор"
            if r["name"] == best_option else "Доступен"
        }

        for r in results

    ])

    csv = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Скачать отчёт CSV",
        data=csv,
        file_name="saas_advisor_report.csv",
        mime="text/csv"
    )

else:

    st.error(
        "⚠️ Для заданных параметров нет подходящих тарифов. "
        "Измените количество сотрудников или требования SSO."
    )


# =====================================================
# 9. ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ
# =====================================================

with st.expander("ℹ️ О проекте"):

    st.write("""
    SaaS Advisor — инструмент для сравнительного анализа
    облачных платформ и выбора оптимального тарифа.

    **Программа учитывает:**

    - Количество сотрудников.
    - Стоимость тарифов.
    - Максимальное количество пользователей.
    - Наличие поддержки SSO.
    - Совокупную годовую стоимость владения (TCO).

    Расчёт производится на основе встроенной базы тарифов.
    Перед практическим использованием необходимо проверить
    актуальность цен и условий поставщиков.
    """)


# =====================================================
# 10. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    💎 SaaS Advisor Premium · 2026<br>
    Интеллектуальный подбор облачных решений<br>
    Курсовой проект · Управление IT-сервисом
</div>
""", unsafe_allow_html=True)
