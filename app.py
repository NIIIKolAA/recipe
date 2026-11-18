import streamlit as st
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="SaaS Advisor | Premium", page_icon="💎", layout="wide")

# 2. Внедрение премиального CSS (Glassmorphism + Градиенты + Свечение)
st.markdown("""
<style>
    /* Импорт красивого шрифта */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Глубокий градиентный фон */
    .stApp {
        background: radial-gradient(circle at top left, #1e1b4b 0%, #0f172a 40%, #020617 100%) !important;
        color: #f8fafc !important;
    }
    
    /* Стеклянная панель для сайдбара */
    [data-testid="stSidebar"] {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Принудительно белый текст в сайдбаре */
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* Градиентные заголовки */
    h1 {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    /* Карточки метрик */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.2);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    /* Стилизация уведомления об успехе */
    .stAlert {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px;
        color: #34d399 !important;
    }
    .stAlert p {
        color: #34d399 !important;
        font-weight: 600;
    }

    /* Таблица */
    .stDataFrame {
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 3. Шапка сайта
st.title("💎 SaaS Advisor")
st.markdown("### Интеллектуальный подбор облачной среды")
st.markdown("<p style='color: #94a3b8; font-size: 16px;'>Премиальный калькулятор для расчета совокупной стоимости владения (TCO). Автоматизирует выбор Collaboration SaaS на основе актуальных тарифов 2026 года.</p>", unsafe_allow_html=True)

st.divider()

# 4. Ввод данных в боковой панели
with st.sidebar:
    st.markdown("### ⚙️ Параметры команды")
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

# 7. Вывод результатов
st.markdown("### 📊 Результаты анализа")

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
    
    # Стилизация таблицы
    def highlight_best(row):
        if row['Платформа и тариф'] == best_option:
            return ['background-color: rgba(56, 189, 248, 0.15); color: #38bdf8; font-weight: bold;'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_best, axis=1), 
        use_container_width=True,
        height=250
    )
    
    st.success(f"🏆 **Оптимальный выбор:** {best_option}. Данное решение обеспечивает наилучший баланс цены и безопасности.")
else:
    st.error("⚠️ **ВНИМАНИЕ:** Для заданных параметров нет подходящих тарифов.")
