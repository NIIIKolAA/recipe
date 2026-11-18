import streamlit as st
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="SaaS Advisor | Premium", page_icon="💎", layout="wide")

# 2. Жесткий CSS (читаемые числа, компактность, темный фон)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    header[data-testid="stHeader"] { background: transparent !important; }
    
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0%, #1e1b4b 50%, #020617 100%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* Карточки метрик */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 15px;
        border-radius: 16px;
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }

    /* Кастомная HTML-таблица (вместо глючной встроенной) */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .custom-table th {
        background: rgba(15, 23, 42, 0.9);
        color: #38bdf8;
        padding: 15px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid rgba(56, 189, 248, 0.3);
    }
    .custom-table td {
        padding: 12px 15px;
        color: #e2e8f0;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    /* Подсветка лучшего тарифа */
    .custom-table tr.best-row {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8 !important;
        font-weight: bold;
    }
    .custom-table tr.best-row td {
        color: #38bdf8 !important;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Шапка сайта
st.markdown("<h1 style='text-align: center;'>💎 SaaS Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Интеллектуальный калькулятор TCO на основе тарифов 2026 года.</p>", unsafe_allow_html=True)

# 4. Ввод данных (сделаем по центру, чтобы не было пустот)
col_input, _ = st.columns([1, 2])
with col_input:
    team_size = st.slider("Количество сотрудников", min_value=10, max_value=500, value=100, step=10)
    require_sso = st.checkbox("Требуется SSO (единый вход)")

# 5. База тарифов
tariffs = {
    "VK WorkSpace Базовый": {"price": 309, "max_users": 300, "sso": False},
    "VK WorkSpace Расширенный": {"price": 499, "max_users": 500, "sso": True},
    "Яндекс 360 Минимальный": {"price": 319, "max_users": 250, "sso": False},
    "Яндекс 360 Основной": {"price": 549, "max_users": 250, "sso": True},
    "Р7 пространство": {"price": 320, "max_users": 50, "sso": False}
}

# 6. Логика расчета
results = []
best_option = None
min_price = float('inf')

for name, params in tariffs.items():
    if team_size <= params["max_users"]:
        if require_sso and not params["sso"]:
            continue
        
        annual_cost = params["price"] * team_size * 12
        
        results.append({
            "name": name, 
            "cost": annual_cost, 
            "sso": "✅ Да" if params["sso"] else "❌ Нет"
        })
        
        if annual_cost < min_price:
            min_price = annual_cost
            best_option = name

# 7. Результаты (Карточки)
st.markdown("<h3 style='margin-top: 30px;'>📊 Результаты анализа</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Размер команды", value=f"{team_size} чел.")
with col2:
    st.metric(label="Требование SSO", value="Да" if require_sso else "Нет")
with col3:
    if best_option:
        st.metric(label="Лучшая цена (в год)", value=f"{min_price:,} ₽")
    else:
        st.metric(label="Лучшая цена", value="—")

# 8. Вывод таблицы (вручную через HTML)
if results:
    html_table = "<table class='custom-table'>"
    html_table += "<tr><th>Платформа и тариф</th><th>Стоимость в год (₽)</th><th>SSO</th></tr>"
    
    for row in results:
        # Если это лучший тариф, подсвечиваем его
        row_class = "class='best-row'" if row['name'] == best_option else ""
        html_table += f"<tr {row_class}>"
        html_table += f"<td>{row['name']}</td>"
        html_table += f"<td>{row['cost']:,} ₽</td>"
        html_table += f"<td>{row['sso']}</td>"
        html_table += "</tr>"
        
    html_table += "</table>"
    
    # Выводим таблицу
    st.markdown(html_table, unsafe_allow_html=True)
    
    st.success(f"🏆 **Оптимальный выбор:** {best_option}. Данное решение обеспечивает наилучший баланс цены и безопасности.")
else:
    st.error("⚠️ **ВНИМАНИЕ:** Для заданных параметров нет подходящих тарифов.")
