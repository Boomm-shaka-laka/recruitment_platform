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

# === 1. 自定义CSS样式 (已优化) ===
st.markdown("""
<style>
/* 
   强制非粘性布局，解决移动端fixed定位问题
   为所有相关元素添加-webkit-前缀以支持旧版Webkit内核
*/
header[data-testid="stHeader"], div[data-testid="stToolbar"] {
    position: static !important;
    -webkit-transform: none !important;
    transform: none !important;
}

/* 为容器添加3D上下文，触发硬件加速 */
main > .block-container {
    -webkit-transform: translateZ(0);
    transform: translateZ(0);
}

/* 强制body和html高度为100%，防止某些移动端浏览器的布局问题 */
html, body {
    height: 100%;
    -webkit-text-size-adjust: 100%; /* 防止iOS Safari自动调整字体大小 */
    -webkit-tap-highlight-color: transparent; /* 移除点击高亮 */
}

/* ── HERO ── */
.hero {
    position: relative; 
    width: 100%; 
    height: 360px; /* 默认缩小高度 */
    overflow: hidden;
    background-size: 400% 400%;
    -webkit-animation: gradientFlow 12s ease infinite;
    animation: gradientFlow 12s ease infinite;
    display: -webkit-box; 
    display: -ms-flexbox;
    display: flex; 
    -webkit-box-align: center; 
    -ms-flex-align: center; 
    align-items: center; 
    -webkit-box-pack: center; 
    -ms-flex-pack: center; 
    justify-content: center;
}
.hero-particles {
    position: absolute; 
    top: 0; 
    left: 0; 
    right: 0; 
    bottom: 0; 
    overflow: hidden; 
    pointer-events: none;
}
.hero-particles span {
    position: absolute; 
    border-radius: 50%;
    background: -webkit-radial-gradient(circle, rgba(240,214,135,0.18), transparent 70%);
    background: radial-gradient(circle, rgba(240,214,135,0.18), transparent 70%);
    -webkit-animation: floatBubble ease-in-out infinite;
    animation: floatBubble ease-in-out infinite;
}
.hero-particles span:nth-child(1) { width:280px; height:280px; top:5%; left:3%; -webkit-animation-duration:7s; animation-duration:7s; }
.hero-particles span:nth-child(2) { width:190px; height:190px; top:50%; left:72%; -webkit-animation-duration:9s; animation-duration:9s; -webkit-animation-delay:1.2s; animation-delay:1.2s; }
.hero-particles span:nth-child(3) { width:130px; height:130px; top:18%; left:55%; -webkit-animation-duration:6s; animation-duration:6s; -webkit-animation-delay:2s; animation-delay:2s; }
.hero-particles span:nth-child(4) { width:100px; height:100px; top:68%; left:22%; -webkit-animation-duration:8.5s; animation-duration:8.5s; -webkit-animation-delay:0.5s; animation-delay:0.5s; }
.hero-grid {
    position: absolute; 
    top: 0; 
    left: 0; 
    right: 0; 
    bottom: 0;
    background-image:
        -webkit-linear-gradient(rgba(240,214,135,0.07) 1px, transparent 1px),
        -webkit-linear-gradient(90deg, rgba(240,214,135,0.07) 1px, transparent 1px);
    background-image:
        linear-gradient(rgba(240,214,135,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(240,214,135,0.07) 1px, transparent 1px);
    background-size: 54px 54px;
}
.hero-content {
    position: relative; 
    text-align: center; 
    color: white;
    padding: 0 24px; /* 缩小padding */
    -webkit-animation: fadeSlideUp 0.9s ease 0.2s both;
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
    font-size: 2.5rem; /* 缩小字体 */
    font-weight: 700;
    background: -webkit-linear-gradient(135deg, #f5e29a, #e8b84d, #f0d687, #fff3c0);
    background: linear-gradient(135deg, #f5e29a, #e8b84d, #f0d687, #fff3c0);
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.2em; 
    margin-bottom: 10px;
    -webkit-filter: drop-shadow(0 2px 22px rgba(232,184,77,0.4));
    filter: drop-shadow(0 2px 22px rgba(232,184,77,0.4));
}
.hero-title-en {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem; /* 缩小字体 */
    color: #7a9abf;
    letter-spacing: 0.22em; 
    text-transform: uppercase; 
    margin-bottom: 22px;
}
.hero-divider {
    display: -webkit-box; 
    display: -ms-flexbox; 
    display: flex; 
    -webkit-box-align: center; 
    -ms-flex-align: center; 
    align-items: center; 
    -webkit-box-pack: center; 
    -ms-flex-pack: center; 
    justify-content: center;
    gap: 10px; 
    margin-bottom: 20px;
}
.hero-divider-line { width: 64px; height: 1px; background: -webkit-linear-gradient(90deg, transparent, #f0d687); background: linear-gradient(90deg, transparent, #f0d687); }
.hero-divider-line.right { background: -webkit-linear-gradient(90deg, #f0d687, transparent); background: linear-gradient(90deg, #f0d687, transparent); }
.hero-divider-diamond { width: 8px; height: 8px; background: #f0d687; -webkit-transform: rotate(45deg); -ms-transform: rotate(45deg); transform: rotate(45deg); }
.hero-subtitle {
    font-size: 1rem; /* 缩小字体 */
    color: #6a90b8;
    letter-spacing: 0.07em; 
    max-width: 500px; 
    margin: 0 auto;
}
.hero-seal {
    display: none; /* 在移动端隐藏复杂的印章动画 */
}

/* ── Job Card Styles ── */
.job-card {
    position: relative;
    background: rgba(10, 22, 40, 0.95);
    border: 1px solid rgba(240, 214, 135, 0.25);
    border-radius: 16px;
    padding: 22px;
    color: #e0e7ff;
    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.4),
        inset 0 0 0 1px rgba(240, 214, 135, 0.1);
    -webkit-animation: cardIn 0.6s ease forwards;
    animation: cardIn 0.6s ease forwards;
    overflow: visible;
    -webkit-transition: all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    transition: all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    margin-bottom: 28px;
    isolation: isolate;
}

.job-card:hover {
    -webkit-transform: translateY(-6px) scale(1.01);
    -ms-transform: translateY(-6px) scale(1.01);
    transform: translateY(-6px) scale(1.01);
    box-shadow:
        0 16px 32px rgba(232, 184, 77, 0.35),
        inset 0 0 0 1px rgba(240, 214, 135, 0.35);
}

.job-card h3 {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.3rem;
    margin-bottom: 14px;
    color: #f0d687;
    line-height: 1.3;
}

.job-card p.overview {
    font-size: 0.92rem;
    line-height: 1.6;
    color: #a0b8d0;
    margin-bottom: 20px;
}

.job-card-footer {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-top: 12px;
    font-size: 0.8rem;
    color: #6a8ab8;
}

.job-card-meta span::before {
    content: "📅 ";
}

/* ── Custom Pagination Button Styles ── */
.pagination-container {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    gap: 12px;
    margin-top: 20px;
    padding: 0 10px;
}

.page-info {
    color: #a0b8d0;
    font-size: 0.9rem;
    text-align: center;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
}

.custom-btn {
    display: inline-block;
    background: linear-gradient(135deg, #1a2a4a, #0d1b33);
    border: 1px solid rgba(240, 214, 135, 0.3);
    color: #f0d687;
    padding: 10px 20px;
    border-radius: 8px; /* 改为圆角矩形，更易点击 */
    text-decoration: none;
    font-size: 0.9rem;
    cursor: pointer;
    -webkit-transition: all 0.2s ease;
    transition: all 0.2s ease;
    text-align: center;
    min-width: 100px;
    -webkit-user-select: none; /* 防止文本被意外选中 */
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.custom-btn:hover:not(.disabled) {
    background: linear-gradient(135deg, #223355, #121f3a);
    border-color: rgba(240, 214, 135, 0.6);
    color: #fff3c0;
    box-shadow: 0 0 12px rgba(232, 184, 77, 0.4);
}

.custom-btn.disabled {
    opacity: 0.4;
    cursor: not-allowed;
    border-color: rgba(240, 214, 135, 0.15);
}

/* ── Keyframe Animations (已添加-webkit-前缀) ── */
@-webkit-keyframes fadeSlideUp {
  from { opacity: 0; -webkit-transform: translateY(28px); transform: translateY(28px); }
  to   { opacity: 1; -webkit-transform: translateY(0); transform: translateY(0); }
}
@keyframes fadeSlideUp {
  from { opacity: 0; -webkit-transform: translateY(28px); transform: translateY(28px); }
  to   { opacity: 1; -webkit-transform: translateY(0); transform: translateY(0); }
}

@-webkit-keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@-webkit-keyframes rotateSeal {
  from { -webkit-transform: translateY(-50%) rotate(0deg); transform: translateY(-50%) rotate(0deg); }
  to   { -webkit-transform: translateY(-50%) rotate(360deg); transform: translateY(-50%) rotate(360deg); }
}
@keyframes rotateSeal {
  from { -webkit-transform: translateY(-50%) rotate(0deg); transform: translateY(-50%) rotate(0deg); }
  to   { -webkit-transform: translateY(-50%) rotate(360deg); transform: translateY(-50%) rotate(360deg); }
}

@-webkit-keyframes floatBubble {
  0%, 100% { -webkit-transform: translateY(0px) scale(1); transform: translateY(0px) scale(1); opacity: 0.5; }
  50%       { -webkit-transform: translateY(-20px) scale(1.05); transform: translateY(-20px) scale(1.05); opacity: 0.9; }
}
@keyframes floatBubble {
  0%, 100% { -webkit-transform: translateY(0px) scale(1); transform: translateY(0px) scale(1); opacity: 0.5; }
  50%       { -webkit-transform: translateY(-20px) scale(1.05); transform: translateY(-20px) scale(1.05); opacity: 0.9; }
}

@-webkit-keyframes gradientFlow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes gradientFlow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@-webkit-keyframes cardIn {
  from { opacity: 0; -webkit-transform: translateY(22px) scale(0.98); transform: translateY(22px) scale(0.98); }
  to   { opacity: 1; -webkit-transform: translateY(0) scale(1); transform: translateY(0) scale(1); }
}
@keyframes cardIn {
  from { opacity: 0; -webkit-transform: translateY(22px) scale(0.98); transform: translateY(22px) scale(0.98); }
  to   { opacity: 1; -webkit-transform: translateY(0) scale(1); transform: translateY(0) scale(1); }
}

/* 响应式设计 */
@media (min-width: 769px) {
    /* 桌面端样式 */
    .hero {
        height: 400px;
        margin-top: -70px;
    }
    .hero-title-zh {
        font-size: 4rem;
    }
    .hero-title-en {
        font-size: 1.18rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        max-width: 530px;
    }
    .hero-seal {
        display: block; /* 桌面端显示印章 */
        position: absolute; 
        right: 90px; 
        top: 50%;
        -webkit-transform: translateY(-50%);
        -ms-transform: translateY(-50%);
        transform: translateY(-50%);
        width: 132px; 
        height: 132px;
        -webkit-animation: fadeIn 1.2s ease 0.7s both;
        animation: fadeIn 1.2s ease 0.7s both;
    }
    .hero-seal-outer {
        position: absolute; 
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 1.5px solid rgba(240,214,135,0.38);
        border-radius: 50%;
        -webkit-animation: rotateSeal 20s linear infinite;
        animation: rotateSeal 20s linear infinite;
    }
    .hero-seal-outer::before {
        content: ''; 
        position: absolute; 
        top: 8px;
        left: 8px;
        right: 8px;
        bottom: 8px;
        border: 1px dashed rgba(240,214,135,0.2); 
        border-radius: 50%;
    }
    .hero-seal-inner {
        position: absolute; 
        top: 22px;
        left: 22px;
        right: 22px;
        bottom: 22px;
        border: 1px solid rgba(240,214,135,0.28);
        border-radius: 50%;
        display: -webkit-box; 
        display: -ms-flexbox; 
        display: flex; 
        -webkit-box-align: center; 
        -ms-flex-align: center; 
        align-items: center; 
        -webkit-box-pack: center; 
        -ms-flex-pack: center; 
        justify-content: center;
    }
    .hero-seal-text {
        font-family: 'Noto Serif SC', serif;
        color: rgba(240,214,135,0.72);
        font-size: 0.85rem; 
        text-align: center; 
        line-height: 1.9;
    }
    .job-card h3 {
        font-size: 1.4rem;
    }
    .job-card p.overview {
        font-size: 0.95rem;
    }
    .job-card-footer {
        font-size: 0.82rem;
    }
    .pagination-container {
        gap: 20px;
    }
    .custom-btn {
        min-width: 120px;
        padding: 12px 24px;
    }
}

/* 手机端样式 */
@media (max-width: 768px) {
    .hero {
        height: 320px;
        margin-top: -50px;
    }
    .hero-title-zh {
        font-size: 2rem;
    }
    .hero-title-en {
        font-size: 0.8rem;
    }
    .hero-subtitle {
        font-size: 0.85rem;
        padding: 0 12px;
    }
    .job-card {
        padding: 18px;
    }
    .job-card h3 {
        font-size: 1.15rem;
    }
    .job-card p.overview {
        font-size: 0.88rem;
    }
    .job-card-footer {
        font-size: 0.75rem;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        -webkit-box-align: start;
        -ms-flex-align: start;
        align-items: flex-start;
        gap: 10px;
    }
    .job-card-link {
        float: none;
        margin-top: 10px;
        margin-left: 0;
    }
    .page-info {
        font-size: 0.85rem;
    }
    .custom-btn {
        padding: 8px 16px;
        font-size: 0.85rem;
        min-width: 80px;
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
    
    # 构建 jobs 列表
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
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 计算当前页的数据切片
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_jobs = jobs[start_idx:end_idx]

    # 渲染当前页的卡片
    for idx, job in enumerate(current_jobs):
        st.markdown(f"""
        <div class="job-card" style="-webkit-animation-delay: {idx * 0.15}s; animation-delay: {idx * 0.15}s;">
            <h3>{job['title']}</h3>
            <p class="overview">{job['overview']}</p>
            <div class="job-card-footer">
                <div class="job-card-meta">
                    <span>{job['publish_time']}</span>
                </div>
                <a href="{job['link']}" target="_blank" class="job-card-link">🔍 查看详情</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === 渲染自定义分页器 (完全基于URL参数，无需JavaScript) ===
    query_params = st.query_params
    current_page_num = int(query_params.get("page", [1])[0])
    
    # 生成下一页和上一页的URL
    next_page_num = current_page_num + 1
    prev_page_num = current_page_num - 1

    st.markdown("<div class='pagination-container'>", unsafe_allow_html=True)
    
    # 上一页按钮
    if current_page_num > 1:
        st.markdown(f"<a href='?page={prev_page_num}' class='custom-btn'>⬅️ 上一页</a>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='custom-btn disabled'>⬅️ 上一页</span>", unsafe_allow_html=True)

    # 信息展示
    st.markdown(
        f"<div class='page-info'>"
        f"共 {total_items} 条岗位信息 | "
        f"第 {current_page_num} 页 / 共 {total_pages} 页"
        f"</div>",
        unsafe_allow_html=True
    )

    # 下一页按钮
    if current_page_num < total_pages:
        st.markdown(f"<a href='?page={next_page_num}' class='custom-btn'>下一页 ➡️</a>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='custom-btn disabled'>下一页 ➡️</span>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)


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