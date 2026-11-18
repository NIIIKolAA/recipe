import streamlit as st
import pandas as pd
import plotly.express as px

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

/* ОСНОВНОЙ ФОН */
.stApp {
    background: radial-gradient(ellipse at 15% 0%, rgba(56,189,248,0.10), transparent 35%),
                radial-gradient(ellipse at 90% 10%, rgba(129,140,248,0.10), transparent 35%),
                #080d19 !important;
    font-family: 'Inter', sans-serif !important;
    color: #f1f5f9;
}

.block-container { padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; max-width: 1400px; }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* БОКОВАЯ ПАНЕЛЬ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a2c, #0b1220) !important;
    border-right: 1px solid rgba(148,163,184,0.14);
}
[data-testid="stSidebar"] * { color: #e2e8f0; }

/* ЗАГОЛОВКИ */
h1, h2, h3, h4 { color: #f8fafc !important; font-weight: 800 !important; }

/* ГЛАВНАЯ ШАПКА (HERO) */
.hero {
    background: linear-gradient(120deg, rgba(30,41,59,0.95), rgba(23,37,65,0.85));
    border: 1px solid rgba(56,189,248,0.22);
    border-radius: 22px;
    padding: 30px 35px;
    margin-bottom: 25px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
}
.hero h1 {
    font-size: 36px; margin: 0;
    background: linear-gradient(90deg,#ffffff,#7dd3fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #94a3b8; font-size: 14px; margin-top: 10px; margin-bottom: 0; }

/* КАРТОЧКИ МЕТРИК */
[data-testid="stMetric"] {
    background: linear-gradient(145deg,#142137,#101a2b) !important;
    border: 1px solid rgba(56,189,248,0.17) !important;
    border-radius: 17px !important;
    padding: 15px !important;
    min-height: 100px;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 13px !important; }
[data-testid="stMetricValue"] { color: #7dd3fc !important; font-size: 26px !important; font-weight: 800 !important; }

/* КАСТОМНАЯ ТАБЛИЦА */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    background: rgba(17,26,43,0.8);
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(56,189,248,0.18);
}
.custom-table th {
    background: rgba(30,41,59,0.9);
    color: #38bdf8;
    padding: 15px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    border-bottom: 1px solid rgba(56,189,248,0.2);
}
.custom-table td {
    padding: 15px;
    color: #e2e8f0;
    font-size: 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.custom-table tr:hover { background: rgba(56,189,248,0.05); }
.custom-table tr.best-row { background: rgba(56,189,248,0.1); }
.custom-table tr.best-row td { color: #38bdf8; font-weight: 700; }

/* УВЕДОМЛЕНИЯ */
.stAlert {
    background: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 12px;
}
.stAlert p { color: #34d399 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. ШАПКА САЙТА
# ============================================================
hero_html = """
<div class="hero">
    <h1>💎 SaaS Advisor</h1>
    <p>Интеллектуальная платформа для сравнения облачных сервисов. Анализируйте стоимость владения, проверяйте поддержку SSO и выбирайте оптимальное решение для вашей команды.</p>
</div>
"""
st.write(hero_html, unsafe_allow_html=True)


# ============================================================
# 4. БОКОВАЯ ПАНЕЛЬ
# ============================================================
with st.sidebar:
    st.markdown("## 💎 SaaS Advisor")
    st.caption("SMART TCO ANALYTICS")
    st.markdown("---")
    
    team_size = st.slider("Количество сотрудников", min_value=10, max_value=500, value=100, step=10)
    require_sso = st.checkbox("Требуется SSO", value=False)
    
    st.markdown("---")
    st.caption("Версия системы: 1.0")
    st.caption("© 2026 SaaS Advisor")


# ============================================================
# 5. БАЗА ТАРИФОВ
# ============================================================
tariffs = {
    "VK WorkSpace Базовый": {"price": 309, "max": 300, "sso": False},
    "VK WorkSpace Расширенный": {"price": 499, "max": 500, "sso": True},
    "Яндекс 360 Минимальный": {"price": 319, "max": 250, "sso": False},
    "Яндекс 360 Основной": {"price": 549, "max": 250, "sso": True},
    "Р7 пространство": {"price": 320, "max": 50, "sso": False}
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
            "Цена за польз.": f"{params['price']} ₽",
            "Стоимость в год": annual,
            "SSO": "✅ Да" if params["sso"] else "❌ Нет"
        })
        
        if annual < min_price:
            min_price = annual
            best_option = name


# ============================================================
# 7. ОСНОВНЫЕ МЕТРИКИ
# ============================================================
st.markdown("### 📊 Панель аналитики")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Размер команды", f"{team_size} чел.")
col2.metric("Требование SSO", "Включено" if require_sso else "Не требуется")
col3.metric("Доступные тарифы", len(results))
col4.metric("Минимум в год", f"{min_price:,.0f} ₽" if best_option else "—")

if best_option:
    st.success(f"🏆 **OPTIMAL SOLUTION:** {best_option} | Стоимость: **{min_price:,.0f} ₽ / год**")


# ============================================================
# 8. ТАБЛИЦА И ГРАФИК
# ============================================================
st.markdown("### 📈 Сравнение решений")

if results:
    col_table, col_chart = st.columns([1.1, 1], gap="large")

    with col_table:
        # Строим красивую HTML-таблицу вручную
        html_table = """
        <table class="custom-table">
            <tr>
                <th>Платформа и тариф</th>
                <th>Цена польз./мес.</th>
                <th>Стоимость в год</th>
                <th>SSO</th>
            </tr>
        """
        for row in results:
            is_best = row["Платформа"] == best_option
            row_class = "best-row" if is_best else ""
            
            html_table += f"""
            <tr class="{row_class}">
                <td>{row['Платформа']}</td>
                <td>{row['Цена за польз.']}</td>
                <td>{row['Стоимость в год']:,} ₽</td>
                <td>{row['SSO']}</td>
            </tr>
            """
        html_table += "</table>"
        
        # Выводим через st.write, чтобы не было тегов
        st.write(html_table, unsafe_allow_html=True)

    with col_chart:
        # Готовим данные для графика
        chart_df = pd.DataFrame({
            "Платформа": [r["Платформа"] for r in results],
            "Годовая стоимость": [r["Стоимость в год"] for r in results]
        }).sort_values("Годовая стоимость", ascending=True)
        
        # Создаем красивый график через Plotly
        fig = px.bar(
            chart_df, 
            x="Годовая стоимость", 
            y="Платформа", 
            orientation='h',
            text="Годовая стоимость",
            color_discrete_sequence=["#38bdf8"]
        )
        
        # Настраиваем дизайн графика (прозрачный фон, аккуратные подписи)
        fig.update_traces(
            texttemplate='%{text:,.0f} ₽', 
            textposition='outside',
            marker=dict(line=dict(color='rgba(56,189,248,0.5)', width=1))
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8', family="Inter"),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title=""),
            yaxis=dict(title="", tickfont=dict(size=13, color='#f1f5f9')),
            margin=dict(l=0, r=20, t=20, b=0),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

else:
    st.error("Для выбранных параметров нет доступных тарифов.")


# ============================================================
# 9. ФУТЕР
# ============================================================
footer_html = """
<div style="border-top: 1px solid rgba(148,163,184,0.14); margin-top: 40px; padding-top: 15px; text-align: center; color: #64748b; font-size: 11px;">
    <b>💎 SaaS Advisor</b> · © 2026 Academic Project
</div>
"""
st.write(footer_html, unsafe_allow_html=True)
