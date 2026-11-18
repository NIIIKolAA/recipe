import streamlit as st
import pandas as pd

# 1. НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="SaaS Advisor", page_icon="💎", layout="wide")

# 2. КРАСИВЫЙ И НАДЕЖНЫЙ CSS (без ломки нативных таблиц)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Темный фон */
    .stApp {
        background: radial-gradient(circle at 10% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Сайдбар */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    /* Заголовки */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 800 !important; }
    
    /* Шапка */
    .hero {
        background: linear-gradient(120deg, rgba(30,41,59,0.9), rgba(23,37,65,0.8));
        border: 1px solid rgba(56,189,248,0.3);
        border-radius: 16px;
        padding: 25px 30px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero h1 { margin: 0; font-size: 32px; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero p { color: #94a3b8; font-size: 14px; margin-top: 8px; margin-bottom: 0; }

    /* Карточки метрик */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 15px !important;
        text-align: center;
    }
    [data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 24px !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 13px !important; }

    /* Нативная таблица (делаем темной) */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        background-color: #0f172a !important;
    }
    [data-testid="stDataFrame"] * { color: #f8fafc !important; font-size: 14px !important; }
    [data-testid="stDataFrame"] th { background-color: #1e293b !important; color: #38bdf8 !important; text-align: center !important; }

    /* Нативный график */
    [data-testid="stVegaLiteChart"] {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 10px;
    }

    /* Уведомление */
    .stAlert {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px;
    }
    .stAlert p { color: #34d399 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# 3. ШАПКА (Безопасный HTML)
hero_html = """
<div class="hero">
    <h1>💎 SaaS Advisor</h1>
    <p>Интеллектуальная платформа для сравнения облачных сервисов и расчета совокупной стоимости владения (TCO).</p>
</div>
"""
st.write(hero_html, unsafe_allow_html=True)

# 4. ПАРАМЕТРЫ
with st.sidebar:
    st.markdown("### ⚙️ Параметры команды")
    team_size = st.slider("Количество сотрудников", min_value=10, max_value=500, value=100, step=10)
    require_sso = st.checkbox("Требуется SSO")
    st.caption("© 2026 Курсовой проект")

# 5. ЛОГИКА
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
            "Цена (мес.)": f"{params['price']} ₽",
            "В год (₽)": annual,
            "SSO": "✅ Да" if params["sso"] else "❌ Нет"
        })
        
        if annual < min_price:
            min_price = annual
            best_option = name

# 6. МЕТРИКИ
st.markdown("### 📊 Результаты анализа")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Размер команды", f"{team_size} чел.")
col2.metric("Требование SSO", "Да" if require_sso else "Нет")
col3.metric("Доступно тарифов", len(results))
col4.metric("Минимум в год", f"{min_price:,.0f} ₽" if best_option else "—")

if best_option:
    st.success(f"🏆 **Оптимальный выбор:** {best_option} (Стоимость: {min_price:,.0f} ₽ / год)")

st.markdown("---")

# 7. ТАБЛИЦА И ГРАФИК
if results:
    col_table, col_chart = st.columns([1.2, 1], gap="large")

    with col_table:
        st.markdown("#### Сравнение тарифов")
        df = pd.DataFrame(results)
        
        def highlight_best(row):
            if row["Платформа"] == best_option:
                return ['background-color: rgba(56,189,248,0.15); color: #38bdf8; font-weight: bold;'] * len(row)
            return [''] * len(row)
            
        st.dataframe(
            df.style.apply(highlight_best, axis=1), 
            use_container_width=True, 
            hide_index=True
        )

    with col_chart:
        st.markdown("#### Годовые расходы")
        # Берем только названия и суммы для графика
        chart_df = pd.DataFrame({
            "Платформа": [r["Платформа"] for r in results],
            "Стоимость": [r["В год (₽)"] for r in results]
        }).sort_values("Стоимость", ascending=True)
        
        st.bar_chart(
            chart_df.set_index("Платформа"), 
            color="#38bdf8", 
            height=280, 
            use_container_width=True
        )
else:
    st.error("Для выбранных параметров нет доступных тарифов. Измените размер команды или уберите требование SSO.")
