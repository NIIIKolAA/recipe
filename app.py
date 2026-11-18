import streamlit as st
import pandas as pd

# 1. Настройка страницы
st.set_page_config(page_title="SaaS Advisor | Премиум выбор", page_icon="💎", layout="wide")

# 2. Внедрение кастомного CSS (Дизайн премиум-уровня)
st.markdown("""
<style>
    /* Темный фон и общий шрифт */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Стили для заголовков */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Стеклянная панель для сайдбара */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Карточки метрик */
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. Шапка сайта
st.title("💎 SaaS Advisor: Интеллектуальный подбор")
st.markdown(
    "**Премиальное решение для расчета совокупной стоимости владения (TCO)**. "
    "Прототип автоматизирует выбор облачной среды для распределенных команд "
    "на основе тарифов 2026 года."
)

# 4. Ввод данных в боковой панели
with st.sidebar:
    st.header("⚙️ Параметры команды")
    team_size = st.slider(
        "Количество сотрудников",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )
    require_sso = st.checkbox("Требуется SSO (единый вход)")
    st.markdown("---")
    st.caption("© 2026 Курсовой проект. Дисциплина: Управление IT-сервисом.")

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
min_price = float("inf")

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

if results:
    df = pd.DataFrame(results)

    # Подсветка самого дешевого тарифа
    def highlight_best(row):
        if row["Платформа и тариф"] == best_option:
            return [
                "background-color: rgba(56, 189, 248, 0.2); "
                "color: #38bdf8; font-weight: bold;"
            ] * len(row)
        return ["color: #e2e8f0;"] * len(row)

    st.dataframe(
        df.style.apply(highlight_best, axis=1),
        use_container_width=True
    )

    st.success(f"🏆 **Оптимальный выбор:** {best_option}")
else:
    st.error(
        "⚠️ ВНИМАНИЕ: Для заданных параметров нет подходящих тарифов. "
        "Увеличьте лимит бюджета или измените требования."
    )
