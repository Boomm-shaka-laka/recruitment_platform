import time
import random
import streamlit as st
from interface import get_soe_data

# --- 页面配置 ---
st.set_page_config(
    page_title="甬才智聘 · State-owned Intelligence Recruitment",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 初始化当前页码（默认第1页）
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# === 1. 自定义CSS样式 ===
st.markdown("""
<style>
/* ── HERO ── */
.hero {
    position: relative; 
    width: 100%; 
    height: 400px;
    overflow: hidden;
    #background: linear-gradient(130deg, #0a1628 0%, #0d2452 35%, #183a7a 65%, #0a2240 100%);
    background-size: 300% 300%;
    animation: gradientFlow 12s ease infinite;
    display: flex; 
    align-items: center; 
    justify-content: center;
    margin-top: -70px;      
}
.hero-particles {
    position: absolute; 
    inset: 0; 
    overflow: hidden; 
    pointer-events: none;
}
.hero-particles span {
    position: absolute; 
    border-radius: 50%;
    background: radial-gradient(circle, rgba(240,214,135,0.18), transparent 70%);
    animation: floatBubble ease-in-out infinite;
}
.hero-particles span:nth-child(1) { width:280px; height:280px; top:5%; left:3%; animation-duration:7s; }
.hero-particles span:nth-child(2) { width:190px; height:190px; top:50%; left:72%; animation-duration:9s; animation-delay:1.2s; }
.hero-particles span:nth-child(3) { width:130px; height:130px; top:18%; left:55%; animation-duration:6s; animation-delay:2s; }
.hero-particles span:nth-child(4) { width:100px; height:100px; top:68%; left:22%; animation-duration:8.5s; animation-delay:0.5s; }
.hero-grid {
    position: absolute; 
    inset: 0;
    background-image:
        linear-gradient(rgba(240,214,135,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(240,214,135,0.07) 1px, transparent 1px);
    background-size: 54px 54px;
}
.hero-content {
    position: relative; 
    text-align: center; 
    color: white;
    padding: 0 32px;
    animation: fadeSlideUp 0.9s ease 0.2s both;
    z-index: 1;
}
.hero-badge {
    display: inline-block;
    background: rgba(240,214,135,0.13);
    border: 1px solid rgba(240,214,135,0.32);
    border-radius: 30px; 
    padding: 5px 20px; 
    margin-bottom: 18px;
    font-size: 0.85rem; 
    letter-spacing: 0.2em; 
    color: #f0d687;
    text-transform: uppercase;
}
.hero-title-zh {
    font-family: 'Noto Serif SC', serif;
    font-size: 4rem; 
    font-weight: 700;
    background: linear-gradient(135deg, #f5e29a, #e8b84d, #f0d687, #fff3c0);
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.2em; 
    margin-bottom: 10px;
    filter: drop-shadow(0 2px 22px rgba(232,184,77,0.4));
}
.hero-title-en {
    font-family: 'Playfair Display', serif;
    font-size: 1.18rem; 
    color: #7a9abf;
    letter-spacing: 0.22em; 
    text-transform: uppercase; 
    margin-bottom: 22px;
}
.hero-divider {
    display: flex; 
    align-items: center; 
    justify-content: center;
    gap: 10px; 
    margin-bottom: 20px;
}
.hero-divider-line { width: 64px; height: 1px; background: linear-gradient(90deg, transparent, #f0d687); }
.hero-divider-line.right { background: linear-gradient(90deg, #f0d687, transparent); }
.hero-divider-diamond { width: 8px; height: 8px; background: #f0d687; transform: rotate(45deg); }
.hero-subtitle {
    font-size: 1.05rem; 
    color: #6a90b8;
    letter-spacing: 0.07em; 
    max-width: 530px; 
    margin: 0 auto;
}
.hero-seal {
    position: absolute; 
    right: 90px; 
    top: 50%;
    transform: translateY(-50%);
    width: 132px; 
    height: 132px;
    animation: fadeIn 1.2s ease 0.7s both;
}
.hero-seal-outer {
    position: absolute; 
    inset: 0;
    border: 1.5px solid rgba(240,214,135,0.38);
    border-radius: 50%;
    animation: rotateSeal 20s linear infinite;
}
.hero-seal-outer::before {
    content: ''; 
    position: absolute; 
    inset: 8px;
    border: 1px dashed rgba(240,214,135,0.2); 
    border-radius: 50%;
}
.hero-seal-inner {
    position: absolute; 
    inset: 22px;
    border: 1px solid rgba(240,214,135,0.28);
    border-radius: 50%;
    display: flex; 
    align-items: center; 
    justify-content: center;
}
.hero-seal-text {
    font-family: 'Noto Serif SC', serif;
    color: rgba(240,214,135,0.72);
    font-size: 0.85rem; 
    text-align: center; 
    line-height: 1.9;
}

/* ── Job Card Styles ── */
.job-card {
    position: relative;
    background: rgba(10, 22, 40, 0.85);
    border: 1px solid rgba(240, 214, 135, 0.25);
    border-radius: 16px;
    padding: 24px;
    color: #e0e7ff;
    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.4),
        inset 0 0 0 1px rgba(240, 214, 135, 0.1);
    backdrop-filter: blur(8px);
    animation: cardIn 0.6s ease forwards;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    margin-bottom: 28px;
}
.job-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow:
        0 16px 32px rgba(232, 184, 77, 0.35),
        inset 0 0 0 1px rgba(240, 214, 135, 0.35);
    z-index: 10;
}
.job-card h3 {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.4rem;
    margin-bottom: 14px;
    color: #f0d687;
    line-height: 1.3;
}
/* ── Clickable Title Link ── */
.job-card-title-link {
    text-decoration: none !important;
    color: inherit !important;
    cursor: pointer;
    display: inline-block; /* 关键：确保可点击区域 */
    width: fit-content;
}
.job-card-title-link h3 {
    transition: color 0.2s ease;
}
.job-card-title-link:hover h3 {
    color: #fff3c0 !important;
    text-decoration: underline !important;
}
.job-card p.overview {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #a0b8d0;
    margin-bottom: 20px;
}
.job-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    font-size: 0.82rem;
    color: #6a8ab8;
}
.job-card-meta {
    display: flex;
    gap: 12px;
}
.job-card-meta span::before {
    content: "📅 ";
}
            
.job-card-link {
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #1a2a4a, #0d1b33);
    border: 1px solid rgba(240, 214, 135, 0.3);
    color: #f0d687;
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 0.88rem;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.25s ease;
    z-index: 2;
}
.job-card-link:hover {
    background: linear-gradient(135deg, #223355, #121f3a);
    border-color: rgba(240, 214, 135, 0.6);
    color: #fff3c0;
    box-shadow: 0 0 12px rgba(232, 184, 77, 0.4);
}

/* ── Keyframe Animations ── */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes rotateSeal {
  from { transform: translateY(-50%) rotate(0deg); }
  to   { transform: translateY(-50%) rotate(360deg); }
}
@keyframes floatBubble {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.5; }
  50%       { transform: translateY(-20px) scale(1.05); opacity: 0.9; }
}
@keyframes gradientFlow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(22px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .hero {
        height: 360px;
        margin-top: -60px;
    }
    .hero-title-zh {
        font-size: 2.3rem;
    }
    .hero-title-en {
        font-size: 0.85rem;
    }
    .hero-subtitle {
        font-size: 0.88rem;
        padding: 0 16px;
    }
    .hero-seal {
        display: none;
    }
    .job-card {
        padding: 18px;
    }
    .job-card h3 {
        font-size: 1.2rem;
    }
    .job-card-link {
        bottom: 16px;
        right: 16px;
        font-size: 0.82rem;
        padding: 5px 12px;
    }
    .job-card-meta {
        font-size: 0.78rem;
    }
}
</style>
""", unsafe_allow_html=True)

# === 2. 定义页面函数 ===
def state_owned_job_page():
    render_hero_section()
    job_list_page_impl('国企招聘')

def public_institution_job_page():
    render_hero_section()
    st.title("甬才智聘 - 事业单位招聘页面")
    st.markdown("情境期待。。。")

def chat_page():
    render_hero_section()
    prompt = st.chat_input()

def about_page():
    render_hero_section()
    st.title("关于我们")
    st.write("这里是关于我们的介绍内容。")

def job_list_page_impl(job_category='国企招聘'):
    subheader_col1, subheader_col2, subheader_col3 = st.columns([1, 2, 1])
    with subheader_col1:
        st.subheader(f"{job_category}")
    with subheader_col3:
        prompt = st.chat_input("智能查询")
    if prompt:
        pass
    posts = get_soe_data()
    
    # 构建 jobs 列表（和你原来一样）
    jobs = []
    for post in posts:
        title = post.get("title", "")
        publish_time = post.get("public_time", "未知")
        overview = post.get("summary", "")[:100] if post.get("summary") else ""
        link = post.get("href", "#")
        jobs.append({
            "title": title,
            "overview": overview,
            "publish_time": publish_time,
            "link": link
        })

    if not jobs:
        st.info("暂无该类别的招聘岗位信息。")
        return

    # === 分页逻辑 ===
    items_per_page = 5
    total_items = len(jobs)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # 向上取整

    # 计算当前页的数据切片
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_jobs = jobs[start_idx:end_idx]

    for idx, job in enumerate(current_jobs):
        safe_link = job['link'].replace("'", "\\'")  # 防止 JS 注入（基础防护）
        st.markdown(f"""
        <div class="job-card" style="animation-delay: {idx * 0.15}s;">
            <a href="{job['link']}" target="_blank" class="job-card-title-link">
                <h3>{job['title']}</h3>
            </a>
            <p class="overview">{job['overview']}</p>
            <div class="job-card-footer">
                <div class="job-card-meta">
                    <span>{job['publish_time']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === 渲染分页器 (使用 Streamlit 原生组件) ===
    # 创建多列布局以实现水平居中
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    # 上一页按钮
    with col1:
        prev_disabled = st.session_state.current_page <= 1
        if st.button("⬅️ 上一页", key="prev_btn", use_container_width=True, disabled=prev_disabled):
            st.session_state.current_page -= 1
            st.rerun()

    # 显示总条数和页数信息
    with col3:
        st.markdown(
            f"<div style='text-align: center; padding-top: 10px; color: #a0b8d0; font-size: 0.9rem;'>"
            f"共 {total_items} 条岗位信息 | "
            f"第 {st.session_state.current_page} 页 / 共 {total_pages} 页"
            f"</div>",
            unsafe_allow_html=True
        )

    # 下一页按钮
    with col5:
        next_disabled = st.session_state.current_page >= total_pages
        if st.button("下一页 ➡️", key="next_btn", use_container_width=True, disabled=next_disabled):
            st.session_state.current_page += 1
            st.rerun()


def render_hero_section():
    st.markdown("""
    <div class="hero">
      <div class="hero-grid"></div>
      <div class="hero-particles">
        <span></span><span></span><span></span><span></span>
      </div>
      <div class="hero-content">
        <div class="hero-badge">✦ 宁波国企人才招聘平台 ✦</div>
        <div class="hero-title-zh">甬才智聘</div>
        <div class="hero-title-en">State-owned Intelligence Recruitment</div>
        <div class="hero-divider">
          <div class="hero-divider-line"></div>
          <div class="hero-divider-diamond"></div>
          <div class="hero-divider-line right"></div>
        </div>
        <div class="hero-subtitle">汇聚宁波优质体制内岗位 · 精准匹配人才需求 · 助力职业腾飞</div>
      </div>
      <div class="hero-seal">
        <div class="hero-seal-outer"></div>
        <div class="hero-seal-inner">
          <div class="hero-seal-text">宁波<br>国企<br>人才</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# === 3. 导航配置 ===
pages = {
    "在招岗位": [
        st.Page(state_owned_job_page, title="国企招聘", icon="🏢"),
        st.Page(public_institution_job_page, title="事业单位招聘", icon="🏛️"),
    ],
    "关于": [
        st.Page(about_page, title="关于我们", icon="ℹ️"),
    ],
    "智能工具": [
        st.Page(chat_page, title="智能招聘助手", icon="ℹ️"),
    ],
}


# === 4. 运行应用 ===
nav = st.navigation(pages, position="top")
nav.run()