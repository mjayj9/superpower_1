
import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# ==========================================
# 1. 초기 설정 및 유틸리티
# ==========================================

st.set_page_config(
    page_title="가상국가 통합 포털", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS로 React의 Tailwind 느낌 구현
st.markdown("""
<style>
    /* 전체 폰트 및 배경 */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* 카드 스타일 컨테이너 */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* 헤더 스타일 */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem 0.5rem 0 0;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    /* 메트릭 스타일 */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #4f46e5; /* Indigo-600 */
        font-weight: 700;
    }
    
    /* 사이드바 스타일 */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* Slate-900 */
        color: white;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] span {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 파일 경로 및 해시 함수
DATA_FILE = 'nation_data.json'
DEFAULT_HASH = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9" # admin123

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    if not os.path.exists(DATA_FILE):
        return None # Initial load handled by JSON file creation
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 세션 초기화
if 'data' not in st.session_state:
    loaded = load_data()
    if loaded:
        st.session_state.data = loaded
    else:
        st.error("데이터 파일(nation_data.json)이 없습니다. 코드를 다시 배포해주세요.")
        st.stop()

if 'user' not in st.session_state:
    st.session_state.user = None

if 'admin_pw_hash' not in st.session_state:
    st.session_state.admin_pw_hash = DEFAULT_HASH

# ==========================================
# 2. 사이드바 (네비게이션 & 로그인)
# ==========================================

with st.sidebar:
    st.markdown("<div style='padding:1rem; text-align:center;'><h1 style='color:white;'>🏛️ SUPERPOWER</h1><p style='color:#94a3b8;'>Virtual Nation System v2.0</p></div>", unsafe_allow_html=True)
    
    # 로그인 처리
    if st.session_state.user:
        u_name = "대통령 (관리자)" if st.session_state.user == 'admin' else f"{st.session_state.user['username']} 시민"
        st.success(f"🟢 접속 중: {u_name}")
        if st.button("로그아웃", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        with st.expander("🔒 로그인 / 입장", expanded=True):
            login_tab1, login_tab2 = st.tabs(["시민", "관리자"])
            with login_tab1:
                c_id = st.text_input("ID", key="cid")
                c_pw = st.text_input("PW", type="password", key="cpw")
                if st.button("시민 접속", use_container_width=True):
                    users = st.session_state.data.get('users', [])
                    user = next((u for u in users if u['username'] == c_id and u['password'] == c_pw), None)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("정보 불일치")
            with login_tab2:
                a_pw = st.text_input("관리자 코드", type="password", key="apw")
                if st.button("집무실 입장", use_container_width=True):
                    if hash_password(a_pw) == st.session_state.admin_pw_hash:
                        st.session_state.user = 'admin'
                        st.rerun()
                    else:
                        st.error("코드 오류")

    st.markdown("---")
    
    # 메뉴
    menu_options = ["국가 개요", "역사 기록실", "국방부 포털", "경제 통계", "문화/홍보", "자연/지리", "정부 조직", "자유 광장"]
    if st.session_state.user == 'admin':
        menu_options.append("👑 대통령 집무실")
    elif st.session_state.user:
        menu_options.append("👤 마이 페이지")
    
    menu = st.radio("이동할 장소", menu_options)
    
    st.markdown("---")
    st.caption(f"© 2024 {st.session_state.data['stats']['formalName']}")

# ==========================================
# 3. 메인 페이지 로직
# ==========================================

data = st.session_state.data
stats = data['stats']
details = data['details']

# --- [1] 국가 개요 ---
if menu == "국가 개요":
    # Hero Section
    with st.container():
        st.markdown(f"""
        <div class="card" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); color: white;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap;">
                <div>
                    <h1 style="font-size:3rem; font-weight:800; margin-bottom:0;">{stats['formalName']}</h1>
                    <p style="font-size:1.2rem; font-style:italic; opacity:0.8;">"{stats['motto']}"</p>
                </div>
                <img src="{stats['flag']}" style="width:150px; border-radius:10px; border:2px solid white; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1);">
            </div>
            <div style="margin-top:2rem; display:flex; gap:2rem; flex-wrap:wrap;">
                <div><span style="opacity:0.6; font-size:0.8rem; font-weight:bold;">수도</span><br/>{stats['capital']}</div>
                <div><span style="opacity:0.6; font-size:0.8rem; font-weight:bold;">인구</span><br/>{stats['population']}</div>
                <div><span style="opacity:0.6; font-size:0.8rem; font-weight:bold;">화폐</span><br/>{stats['currency']}</div>
                <div><span style="opacity:0.6; font-size:0.8rem; font-weight:bold;">언어</span><br/>{stats['language']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 GDP", stats['totalGdp'])
    col2.metric("1인당 GDP", stats['gdpPerCapita'])
    col3.metric("영토 면적", stats['area'])
    col4.metric("HDI (인간개발지수)", stats['hdi'])

    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(stats['coatOfArms'], caption="국가 상징(국장)")
        with st.expander("국가 정보 더보기"):
            st.write(f"**도메인:** {stats['domain']}")
            st.write(f"**국가번호:** {stats['intlPhone']}")
            st.write(f"**시간대:** {stats['timezone']}")
            st.write(f"**민족:** {stats['ethnicity']}")
    with c2:
        st.subheader("⚖️ 정치 및 정부")
        st.markdown(f"""
        - **정치 체제:** {stats['politicalSystem']}
        - **경제 체제:** {stats['economicSystem']}
        - **국가 원수:** {stats['headOfState']}
        - **정부 수반:** {stats['headOfGovernment']}
        - **집권 여당:** {stats['rulingParty']}
        - **의회:** {stats['parliament']}
        """)
        st.info(stats['historyOverview'])

# --- [2] 역사 기록실 ---
elif menu == "역사 기록실":
    st.title("📜 역사 기록실")
    st.markdown("국가의 유구한 역사를 기록하는 공간입니다.")
    
    eras = {
        "고대사 (Ancient)": details['history']['ancient'],
        "중세사 (Medieval)": details['history']['medieval'],
        "근대사 (Modern)": details['history']['modern'],
        "현대사 (Contemporary)": details['history']['contemporary']
    }
    
    for title, content in eras.items():
        with st.expander(title, expanded=True):
            st.write(content)

# --- [3] 국방부 포털 ---
elif menu == "국방부 포털":
    st.title("⚔️ 국방부 포털")
    
    mil = details['military']
    num = mil['numerical']
    
    # Dashboard
    st.markdown(f"""
    <div class="card" style="background-color: #1e293b; color: white;">
        <h3>🛡️ 국방 백서 요약</h3>
        <p>{mil['overview']}</p>
        <div style="margin-top:1rem; display:flex; gap:1rem;">
            <div style="background:#dc2626; padding:0.5rem 1rem; border-radius:0.5rem; font-weight:bold;">데프콘 4단계</div>
            <div style="background:#4f46e5; padding:0.5rem 1rem; border-radius:0.5rem; font-weight:bold;">준비태세 {num['readinessLevel']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("현역 병력", f"{num['troopCount']:,}")
    m2.metric("전차/기갑", f"{num['tankCount']:,}")
    m3.metric("함정", f"{num['shipCount']:,}")
    m4.metric("전술기", f"{num['aircraftCount']:,}")
    
    st.progress(num['readinessLevel'] / 100, text=f"전투 준비 태세 ({num['readinessLevel']}%)")
    
    tab1, tab2, tab3 = st.tabs(["육/해/공", "특수전력", "전략 보고서"])
    with tab1:
        st.info(f"**💂 육군:** {mil['army']}")
        st.info(f"**⚓ 해군:** {mil['navy']}")
        st.info(f"**✈️ 공군:** {mil['airforce']}")
    with tab2:
        st.warning(f"**🌊 해병대:** {mil['marines']}")
        st.warning(f"**🛰️ 우주군:** {mil['space']}")
        st.warning(f"**💻 사이버군:** {mil['cyber']}")
        st.error(f"**🚀 전략군(핵):** {mil['strategic']} (핵탄두: {num.get('nuclearWarheads', 0)}기)")
    with tab3:
        st.markdown(f"### 📄 2024 국방 백서\n{mil['whitePaper']}")

# --- [4] 경제 통계 ---
elif menu == "경제 통계":
    st.title("📈 경제 지표")
    eco = details['economy']
    estats = eco['stats']
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("성장률", estats['gdpGrowthRate'])
    c2.metric("물가상승률", estats['inflationRate'])
    c3.metric("실업률", estats['unemploymentRate'])
    c4.metric("무역수지", estats['tradeBalance'])
    
    st.markdown(f"**주요 산업:** {', '.join(estats['keyIndustries'])}")
    
    with st.expander("산업 상세 분석", expanded=True):
        st.write(f"**🏭 제조업:** {eco['manufacturing']}")
        st.write(f"**🏦 서비스업:** {eco['services']}")
        st.write(f"**🔬 기술/R&D:** {eco['technology']}")
        st.write(f"**🚢 무역:** {eco['trade']}")

# --- [5] 문화/홍보 ---
elif menu == "문화/홍보":
    st.title("🎭 문화 및 관광")
    cult = details['culture']
    cstats = cult['stats']
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1532439778267-3a1375765715?auto=format&fit=crop&q=80&w=800", caption="문화의 중심")
    with col2:
        st.metric("연간 관광객", cstats['annualTourists'])
        st.metric("소프트파워 순위", f"{cstats['globalSoftPowerRank']}위")
        st.write(f"**🍽️ 대표 요리:** {cstats['nationalDish']}")
        st.write(f"**🎉 주요 축제:** {cstats['majorFestivals']}")
    
    st.markdown("---")
    st.write(f"### 전통과 예절\n{cult['traditions']}")
    st.write(f"### 예술 및 미디어\n{cult['arts']}\n\n{cult['media']}")

# --- [6] 자연/지리 ---
elif menu == "자연/지리":
    st.title("🏞️ 자연 환경")
    nat = details['nature']
    nstats = nat['stats']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("평균 기온", nstats['averageTemp'])
    col2.metric("산림 비율", nstats['forestCover'])
    col3.metric("해안선", nstats['coastline'])
    
    st.info(f"**지리적 특성:** {nat['geography']}")
    st.success(f"**기후:** {nat['climate']} (기후대: {', '.join(nstats['climateZones'])})")
    st.warning(f"**자원:** {nat['resources']}")

# --- [7] 정부 조직 ---
elif menu == "정부 조직":
    st.title("🏢 중앙 정부 조직")
    gov = details['government']
    
    for section in gov:
        with st.container():
            st.markdown(f"### {section['title']}")
            st.caption(section['description'])
            cols = st.columns(len(section['items']) if len(section['items']) < 4 else 3)
            for i, item in enumerate(section['items']):
                cols[i % 3].success(item)
            st.divider()
            
    st.info("💡 시민권 신청은 '자유 광장'의 공지사항을 확인하세요.")

# --- [8] 자유 광장 ---
elif menu == "자유 광장":
    st.title("💬 자유 광장")
    
    # 글쓰기 폼
    if st.session_state.user:
        with st.expander("✏️ 새 글 작성하기", expanded=False):
            with st.form("post_form"):
                p_title = st.text_input("제목")
                p_cat = st.selectbox("카테고리", ["general", "petition"])
                p_content = st.text_area("내용")
                if st.form_submit_button("등록"):
                    new_post = {
                        "id": str(datetime.now().timestamp()),
                        "author": "대통령실" if st.session_state.user == 'admin' else st.session_state.user['username'],
                        "title": p_title,
                        "content": p_content,
                        "timestamp": datetime.now().timestamp(),
                        "category": p_cat,
                        "reports": []
                    }
                    st.session_state.data['posts'].insert(0, new_post)
                    save_data(st.session_state.data)
                    st.success("등록 완료!")
                    st.rerun()
    else:
        st.warning("로그인한 시민만 글을 쓸 수 있습니다.")

    # 필터
    cat_filter = st.selectbox("게시판 필터", ["전체", "자유", "신문고(청원)"])
    
    # 리스트 출력
    for post in st.session_state.data['posts']:
        if cat_filter == "자유" and post['category'] != "general": continue
        if cat_filter == "신문고(청원)" and post['category'] != "petition": continue
        
        with st.container():
            # 카드 스타일 적용
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="background-color:{'#fef3c7' if post['category']=='petition' else '#f1f5f9'}; color:{'#b45309' if post['category']=='petition' else '#64748b'}; padding:2px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">
                        {'📢 신문고' if post['category']=='petition' else '💬 자유'}
                    </span>
                    <span style="font-size:0.8rem; color:#94a3b8;">{datetime.fromtimestamp(post['timestamp'] / 1000 if post['timestamp'] > 10000000000 else post['timestamp']).strftime('%Y-%m-%d')}</span>
                </div>
                <h4 style="margin:0.5rem 0;">{post['title']}</h4>
                <p style="font-size:0.9rem; color:#475569;">{post['content']}</p>
                <div style="margin-top:0.5rem; font-size:0.8rem; color:#64748b;">
                    작성자: <b>{post['author']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 관리자 전용 삭제/신고 버튼
            col_a, col_b = st.columns([1, 5])
            if st.session_state.user == 'admin':
                if col_a.button("삭제", key=f"del_{post['id']}"):
                    st.session_state.data['posts'] = [p for p in st.session_state.data['posts'] if p['id'] != post['id']]
                    save_data(st.session_state.data)
                    st.rerun()
            elif st.session_state.user:
                 if col_a.button("🚨 신고", key=f"rep_{post['id']}"):
                     post['reports'].append({"reporter": st.session_state.user['username'], "reason": "사용자 신고", "timestamp": datetime.now().timestamp()})
                     save_data(st.session_state.data)
                     st.toast("신고가 접수되었습니다.")

# --- [9] 대통령 집무실 (관리자) ---
elif menu == "👑 대통령 집무실" and st.session_state.user == 'admin':
    st.title("👑 대통령 집무실")
    st.info("여기서 변경하는 모든 내용은 실시간으로 국가 데이터에 반영됩니다.")
    
    admin_tabs = st.tabs(["기본 정보", "군사력 조절", "경제/사회", "역사 편찬", "시민 관리", "시스템 초기화"])
    
    with admin_tabs[0]:
        with st.form("basic_stats"):
            st.subheader("국가 기본 정보")
            c1, c2 = st.columns(2)
            new_name = c1.text_input("국가명", stats['formalName'])
            new_pop = c2.text_input("인구", stats['population'])
            new_gdp = c1.text_input("GDP", stats['totalGdp'])
            new_sys = c2.text_input("정치 체제", stats['politicalSystem'])
            new_flag = st.text_input("국기 URL", stats['flag'])
            
            if st.form_submit_button("기본 정보 저장"):
                stats['formalName'] = new_name
                stats['population'] = new_pop
                stats['totalGdp'] = new_gdp
                stats['politicalSystem'] = new_sys
                stats['flag'] = new_flag
                save_data(data)
                st.success("저장되었습니다.")
                st.rerun()
    
    with admin_tabs[1]:
        with st.form("mil_stats"):
            st.subheader("국방력 수치 조절")
            mnum = details['military']['numerical']
            
            val_troops = st.number_input("현역 병력", value=mnum['troopCount'])
            val_tanks = st.number_input("전차", value=mnum['tankCount'])
            val_ships = st.number_input("함정", value=mnum['shipCount'])
            val_planes = st.number_input("항공기", value=mnum['aircraftCount'])
            val_nukes = st.number_input("핵탄두", value=mnum.get('nuclearWarheads', 0))
            val_ready = st.slider("전투 준비태세 (%)", 0, 100, mnum['readinessLevel'])
            
            if st.form_submit_button("국방 데이터 갱신"):
                mnum['troopCount'] = val_troops
                mnum['tankCount'] = val_tanks
                mnum['shipCount'] = val_ships
                mnum['aircraftCount'] = val_planes
                mnum['nuclearWarheads'] = val_nukes
                mnum['readinessLevel'] = val_ready
                save_data(data)
                st.success("국방력이 재설정되었습니다.")
                st.rerun()

    with admin_tabs[2]:
        with st.form("eco_soc"):
            st.subheader("경제 및 사회 지표")
            e_gdp = st.text_input("GDP 성장률", details['economy']['stats']['gdpGrowthRate'])
            e_ind = st.text_input("주요 산업 (콤마 구분)", ", ".join(details['economy']['stats']['keyIndustries']))
            
            if st.form_submit_button("경제 지표 저장"):
                details['economy']['stats']['gdpGrowthRate'] = e_gdp
                details['economy']['stats']['keyIndustries'] = [x.strip() for x in e_ind.split(",")]
                save_data(data)
                st.success("저장 완료")

    with admin_tabs[3]:
        with st.form("hist_edit"):
            st.subheader("역사 기록 수정")
            h_ancient = st.text_area("고대사", details['history']['ancient'])
            h_modern = st.text_area("현대사", details['history']['contemporary'])
            if st.form_submit_button("역사 수정"):
                details['history']['ancient'] = h_ancient
                details['history']['contemporary'] = h_modern
                save_data(data)
                st.success("역사가 다시 쓰여졌습니다.")

    with admin_tabs[4]:
        st.subheader("시민 계정 관리")
        users = data.get('users', [])
        st.write(f"총 시민 수: {len(users)}명")
        
        # 시민 리스트
        for u in users:
            c1, c2, c3 = st.columns([1, 2, 1])
            c1.write(u['username'])
            c2.caption(f"가입일: {datetime.fromtimestamp(u['createdAt']).strftime('%Y-%m-%d')}")
            if c3.button("추방", key=f"ban_{u['username']}"):
                data['users'] = [x for x in users if x['username'] != u['username']]
                save_data(data)
                st.rerun()
        
        st.divider()
        st.write("#### 신규 시민 발급")
        with st.form("new_citizen"):
            nc_id = st.text_input("ID")
            nc_pw = st.text_input("PW")
            if st.form_submit_button("발급"):
                if any(u['username'] == nc_id for u in users):
                    st.error("이미 존재하는 ID")
                else:
                    users.append({"username": nc_id, "password": nc_pw, "createdAt": datetime.now().timestamp()})
                    save_data(data)
                    st.success(f"{nc_id} 시민 발급 완료")
                    st.rerun()

    with admin_tabs[5]:
        st.error("🚨 위험 구역")
        if st.button("국가 초기화 (Factory Reset)"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.session_state.data = None
            st.session_state.user = None
            st.success("초기화되었습니다. 새로고침하세요.")

# --- [10] 마이 페이지 (시민) ---
elif menu == "👤 마이 페이지" and st.session_state.user:
    u = st.session_state.user
    st.title("👤 시민 신분증")
    
    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <div style="width:100px; height:100px; background-color:#4f46e5; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:3rem; margin:0 auto;">
            {u['username'][0].upper()}
        </div>
        <h2 style="margin-top:1rem;">{u['username']}</h2>
        <p style="color:#64748b;">슈퍼파워 연방 정식 시민</p>
        <p style="font-size:0.8rem; color:#94a3b8;">가입일: {datetime.fromtimestamp(u['createdAt']).strftime('%Y-%m-%d')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("비밀번호 변경"):
        with st.form("pw_change"):
            new_pw = st.text_input("새 비밀번호", type="password")
            if st.form_submit_button("변경"):
                # Update user list
                for user in data['users']:
                    if user['username'] == u['username']:
                        user['password'] = new_pw
                save_data(data)
                st.success("변경되었습니다. 다시 로그인해주세요.")
                st.session_state.user = None
                st.rerun()

