import streamlit as st
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="SaaS Advisor | Premium", page_icon="💎", layout="wide")

# 2. Максимально агрессивный CSS, чтобы убрать ВСЁ белое
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* Убираем верхнюю белую панель Streamlit */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Весь фон приложения */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0%, #1e1b4b 50%, #020617 100%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Сайдбар - темное стекло */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(56, 189, 248, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* Градиентные заголовки */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    p, label {
        color: #cbd5e1 !important;
    }

    /* Карточки метрик - идеально симметричные с градиентной обводкой */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.1);
        transition: all 0.3s ease;
        text-align: center;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
        transform: translateY(-3px);
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
    }

    /* ЖЕСТКАЯ ТЕМНАЯ ТАБЛИЦА (переопределяем всё) */
    [data-testid="stDataFrame"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 10px;
    }
    [data-testid="stDataFrame"] * {
        color: #e2e8f0 !important;
    }
    /* Делаем верхнюю строку таблицы темной */
    [data-testid="stDataFrame"] th {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
    }

    /* Красивое уведомление */
    .stAlert {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px;
    }
    .stAlert p {
        color: #34d399 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Шапка сайта (симметрично)
st.markdown("<h1 style='text-align: center;'>💎 SaaS Advisor</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Интеллектуальный подбор облачной среды</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Премиальный калькулятор для расчета совокупной стоимости владения (TCO).</p>", unsafe_allow_html=True)

st.divider()

# 4. Ввод данных в боковой панели
with st.sidebar:
    st.markdown("### ⚙️ Параметры")
    team_size = st.slider("Количество сотрудников", min_value=10, max_value=500, value=100, step=10)
    require_sso = st.checkbox("Требуется SSO (единый вход)")
    st.markdown("---")
    st.caption("© 2026 Курсовой проект. Управление IT-сервисом.")

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
        sso_status = "✅ Да" if params["sso"] else "❌ Нет"
        
        results.append({
            "Платформа и тариф": name, 
            "Стоимость в год (₽)": annual_cost, 
            "SSO": sso_status
        })
        
        if annual_cost < min_price:
            min_price = annual_cost
            best_option = name

# 7. Вывод результатов (симметрично)
st.markdown("<h3 style='text-align: center; margin-top: 20px;'>📊 Результаты анализа</h3>", unsafe_allow_html=True)

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

st.markdown("<br>", unsafe_allow_html=True)

# 8. Таблица и вывод
if results:
    df = pd.DataFrame(results)
    
    # Стилизация таблицы (подсветка лучшего)
    def highlight_best(row):
        if row['Платформа и тариф'] == best_option:
            return ['background-color: rgba(56, 189, 248, 0.2); color: #38bdf8; font-weight: bold;'] * len(row)
        return ['background-color: transparent; color: #e2e8f0;'] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_best, axis=1), 
        use_container_width=True,
        height=250
    )
    
    st.success(f"🏆 **Оптимальный выбор:** {best_option}. Данное решение обеспечивает наилучший баланс цены и безопасности.")
else:
    st.error("⚠️ **ВНИМАНИЕ:** Для заданных параметров нет подходящих тарифов.")
