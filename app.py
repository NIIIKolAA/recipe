import streamlit as st
import pandas as pd

# 1. НАСТРОЙКА СТРАНИЦЫ (Компактный режим)
st.set_page_config(page_title="SaaS Advisor", page_icon="💎", layout="wide")

# 2. ПРЕМИАЛЬНЫЙ CSS (Убираем лишние отступы, делаем темную тему)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Фон */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0%, #1e1b4b 50%, #020617 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Убираем лишние отступы сверху и снизу */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Заголовки и текст */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 800 !important; }
    p, span, label { color: #cbd5e1 !important; }
    
    /* Сайдбар */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }

    /* Карточки метрик */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 10px 15px;
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
    }

    /* Стилизация нативной таблицы Streamlit (делаем ее темной и аккуратной) */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        background-color: #0f172a !important;
    }
    [data-testid="stDataFrame"] * {
        color: #f8fafc !important;
        font-size: 14px !important;
    }
    [data-testid="stDataFrame"] th {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        text-align: center !important;
    }
    
    /* Уведомление */
    .stAlert {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        padding: 10px !important;
    }
    .stAlert p { color: #34d399 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# 3. ШАПКА
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>💎 SaaS Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px; margin-bottom: 20px;'>Интеллектуальный подбор облачной среды (TCO 2026)</p>", unsafe_allow_html=True)

# 4. БОКОВАЯ ПАНЕЛЬ
with st.sidebar:
    st.markdown("### ⚙️ Параметры")
    team_size = st.slider("Сотрудников", min_value=10, max_value=500, value=100, step=10)
    require_sso = st.checkbox("Нужен SSO")
    st.caption("© 2026 Курсовой проект")

# 5. БАЗА ТАРИФОВ И РАСЧЕТ
tariffs = {
    "VK WorkSpace Базовый": {"price": 309, "max": 300, "sso": False},
    "VK WorkSpace Расширенный": {"price": 499, "max": 500, "sso": True},
    "Яндекс 360 Минимальный": {"price": 319, "max": 250, "sso": False},
    "Яндекс 360 Основной": {"price": 549, "max": 250, "sso": True},
    "Р7 пространство": {"price": 320, "max": 50, "sso": False}
}

results = []
best_option = None
min_price = float('inf')

for name, params in tariffs.items():
    if team_size <= params["max"]:
        if require_sso and not params["sso"]:
            continue
        
        annual = params["price"] * team_size * 12
        results.append({
            "Платформа": name, 
            "Цена (мес)": f"{params['price']} ₽", 
            "Итого в год": f"{annual:,} ₽", 
            "SSO": "✅ Да" if params["sso"] else "❌ Нет"
        })
        
        if annual < min_price:
            min_price = annual
            best_option = name

# 6. МЕТРИКИ (В один ряд)
col1, col2, col3 = st.columns(3)
col1.metric("Размер команды", f"{team_size} чел.")
col2.metric("Требование SSO", "Да" if require_sso else "Нет")
col3.metric("Лучшая цена (в год)", f"{min_price:,} ₽" if best_option else "—")

st.markdown("<br>", unsafe_allow_html=True)

# 7. ДВА СТОЛБЦА: СЛЕВА ТАБЛИЦА, СПРАВА ГРАФИК
col_table, col_chart = st.columns([1.2, 1])

with col_table:
    st.markdown("#### 🏆 Сравнение тарифов")
    if results:
        # Используем нативную таблицу Streamlit (она не ломается)
        df = pd.DataFrame(results)
        
        # Подсветка лучшей строки
        def highlight_best(row):
            if row['Платформа'] == best_option:
                return ['background-color: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: bold;'] * len(row)
            return [''] * len(row)
        
        st.dataframe(df.style.apply(highlight_best, axis=1), use_container_width=True, hide_index=True)
        st.success(f"🏆 **Рекомендация:** {best_option}")
    else:
        st.error("Нет подходящих тарифов")

with col_chart:
    st.markdown("#### 📈 Структура расходов")
    if results:
        # Красивый график (берем только названия и суммы)
        chart_df = pd.DataFrame([{"Платформа": r["Платформа"], "Год": int(r["Итого в год"].replace(" ₽", "").replace(",", ""))} for r in results])
        
        # Настройка графика
        st.bar_chart(
            chart_df.set_index("Платформа"), 
            color="#38bdf8", 
            use_container_width=True,
            height=300
        )
