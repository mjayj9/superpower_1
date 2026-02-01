
import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# --- 초기 데이터 설정 (constants.ts 내용 변환) ---
INITIAL_DATA = {
    "stats": {
        "territory": "가상의 대륙 중심부",
        "flag": "https://images.unsplash.com/photo-1517059224940-d4af9eec41b7?auto=format&fit=crop&q=80&w=800",
        "coatOfArms": "https://images.unsplash.com/photo-1590073242685-c4ef8867550d?auto=format&fit=crop&q=80&w=400",
        "formalName": "슈퍼파워 연방 공화국",
        "englishName": "Federal Republic of SuperPower",
        "capital": "슈퍼파워 시티",
        "officialName": "슈퍼파워 연방",
        "language": "슈퍼파워어, 한국어",
        "currency": "슈퍼 (SPR)",
        "population": "55,000,000명",
        "totalGdp": "$2.4조",
        "hdi": "0.942 (최상급)",
        "area": "512,000 km²",
        "motto": "자유와 정의의 영원한 빛",
        "politicalSystem": "대통령제 공화국",
        "headOfState": "이슈퍼 대통령",
        "historyOverview": "고대 부족 국가에서 시작하여 연방제로 통합되었습니다.",
    },
    "details": {
        "history": {
            "ancient": "고대 슈퍼파워 부족들의 연맹체 형성 시기. 초기 문명이 강가에서 발원하였습니다.",
            "medieval": "중앙집권적 왕국으로의 발전과 문화적 번영. 주변국과의 교역이 활발했습니다.",
            "modern": "산업 혁명과 공화국 수립을 위한 혁명의 시대. 민주주의의 기틀이 마련되었습니다.",
            "contemporary": "글로벌 강국으로 도약하는 현대의 슈퍼파워. 첨단 기술과 문화의 중심지가 되었습니다."
        },
        "military": {
            "overview": "국민 개병제 기반의 현대적 정예 강군",
            "army": "최신형 전차와 포병 전력을 보유한 육군.",
            "navy": "대양 해군을 지향하며 항모 강습단을 보유한 해군.",
            "airforce": "스텔스 전투기와 독자적 위성 체계를 갖춘 공군.",
            "numerical": {
                "troopCount": 600000,
                "tankCount": 2500,
                "shipCount": 150,
                "aircraftCount": 450,
                "readinessLevel": 95
            }
        },
        "economy": {
            "overview": "첨단 제조업과 지식 기반 서비스업이 조화를 이루는 시장 경제.",
            "stats": {
                "gdpGrowthRate": "3.2%",
                "keyIndustries": ["반도체", "AI 로봇", "바이오", "에너지"]
            }
        }
    },
    "posts": [
        {
            "id": "1",
            "author": "대통령실",
            "title": "국가 포털 개설을 환영합니다",
            "content": "슈퍼파워 연방의 새로운 시작입니다.",
            "timestamp": 1709251200000,
            "category": "general"
        }
    ],
    "users": []
}

# --- 유틸리티 함수 ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

DATA_FILE = 'nation_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return INITIAL_DATA

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- 메인 앱 설정 ---
st.set_page_config(page_title="가상국가 통합 포털", page_icon="🏛️", layout="wide")

# 세션 상태 초기화
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'user' not in st.session_state:
    st.session_state.user = None # None, 'admin', or User dict

# --- 사이드바 (네비게이션 & 로그인) ---
with st.sidebar:
    st.title("🏛️ SUPERPOWER v1.0")
    
    # 로그인 상태 관리
    if st.session_state.user:
        user_display = "대통령 (관리자)" if st.session_state.user == 'admin' else f"{st.session_state.user['username']} 시민"
        st.success(f"접속 중: {user_display}")
        if st.button("로그아웃"):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("로그인이 필요합니다.")
        with st.expander("로그인 / 입장"):
            tab1, tab2 = st.tabs(["시민", "관리자"])
            with tab1:
                c_id = st.text_input("ID")
                c_pw = st.text_input("PW", type="password")
                if st.button("시민 로그인"):
                    users = st.session_state.data.get('users', [])
                    user = next((u for u in users if u['username'] == c_id and u['password'] == c_pw), None)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("정보가 일치하지 않습니다.")
            with tab2:
                a_pw = st.text_input("관리자 코드", type="password")
                if st.button("집무실 입장"):
                    # admin123 hash
                    if hash_password(a_pw) == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
                        st.session_state.user = 'admin'
                        st.rerun()
                    else:
                        st.error("승인 코드가 틀립니다.")

    st.divider()
    
    # 메뉴 선택
    menu = st.radio("메뉴 이동", 
        ["국가 개요", "역사 기록실", "국방부 포털", "경제/문화", "자유 광장", "대통령 집무실" if st.session_state.user == 'admin' else "마이 페이지"])

# --- 메인 페이지 로직 ---
data = st.session_state.data
stats = data['stats']
details = data['details']

if menu == "국가 개요":
    st.image(stats['flag'], use_container_width=True)
    st.title(stats['formalName'])
    st.caption(f"\"{stats['motto']}\"")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("인구", stats['population'])
    col2.metric("총 GDP", stats['totalGdp'])
    col3.metric("영토 면적", stats['area'])
    col4.metric("HDI", stats['hdi'])
    
    with st.expander("🔍 국가 상세 정보 확인", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**수도:** {stats['capital']}")
            st.write(f"**공용어:** {stats['language']}")
            st.write(f"**화폐:** {stats['currency']}")
        with c2:
            st.write(f"**정치 체제:** {stats['politicalSystem']}")
            st.write(f"**국가 원수:** {stats['headOfState']}")

    st.info(stats['historyOverview'])

elif menu == "역사 기록실":
    st.header("📜 국가 역사 연대기")
    tabs = st.tabs(["고대", "중세", "근대", "현대"])
    for i, era in enumerate(['ancient', 'medieval', 'modern', 'contemporary']):
        with tabs[i]:
            st.write(details['history'][era])

elif menu == "국방부 포털":
    st.header("⚔️ 국방 및 군사력")
    mil = details['military']
    num = mil['numerical']
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("전투 준비태세", f"{num['readinessLevel']}%", "정상")
        st.metric("현역 병력", f"{num['troopCount']:,}명")
        st.metric("전차 보유", f"{num['tankCount']:,}대")
    with col2:
        st.subheader("국방 백서 요약")
        st.write(mil['overview'])
        
        st.subheader("각 군 소개")
        st.write(f"**💂 육군:** {mil['army']}")
        st.write(f"**⚓ 해군:** {mil['navy']}")
        st.write(f"**✈️ 공군:** {mil['airforce']}")

elif menu == "경제/문화":
    st.header("📈 경제 및 문화 지표")
    eco = details['economy']
    
    st.subheader("주요 경제 지표")
    c1, c2 = st.columns(2)
    c1.metric("GDP 성장률", eco['stats']['gdpGrowthRate'])
    c2.write("**주요 산업:** " + ", ".join(eco['stats']['keyIndustries']))
    st.write(eco['overview'])

elif menu == "자유 광장":
    st.header("💬 대국민 자유 광장")
    
    # 글쓰기
    if st.session_state.user:
        with st.form("new_post"):
            title = st.text_input("제목")
            content = st.text_area("내용")
            submitted = st.form_submit_button("게시물 등록")
            if submitted and title and content:
                new_post = {
                    "id": str(datetime.now().timestamp()),
                    "author": "대통령실" if st.session_state.user == 'admin' else st.session_state.user['username'],
                    "title": title,
                    "content": content,
                    "timestamp": datetime.now().timestamp(),
                    "category": "general"
                }
                st.session_state.data['posts'].insert(0, new_post)
                save_data(st.session_state.data)
                st.success("등록되었습니다!")
                st.rerun()
    else:
        st.warning("글을 쓰려면 로그인이 필요합니다.")

    # 글 목록
    for post in st.session_state.data['posts']:
        with st.container(border=True):
            st.subheader(post['title'])
            st.caption(f"작성자: {post['author']} | {datetime.fromtimestamp(post['timestamp'] / 1000 if post['timestamp'] > 10000000000 else post['timestamp']).strftime('%Y-%m-%d')}")
            st.write(post['content'])

elif menu == "대통령 집무실":
    if st.session_state.user != 'admin':
        st.error("접근 권한이 없습니다.")
    else:
        st.header("👑 대통령 집무실 (관리자 모드)")
        st.info("여기서 변경하는 내용은 'nation_data.json' 파일에 즉시 저장됩니다.")
        
        with st.form("admin_form"):
            st.subheader("기본 정보 수정")
            new_name = st.text_input("국가 정식 명칭", stats['formalName'])
            new_pop = st.text_input("인구", stats['population'])
            new_gdp = st.text_input("GDP", stats['totalGdp'])
            
            st.subheader("군사 수치 수정")
            new_troops = st.number_input("병력 수", value=details['military']['numerical']['troopCount'])
            new_ready = st.slider("준비 태세", 0, 100, details['military']['numerical']['readinessLevel'])

            if st.form_submit_button("변경 사항 저장"):
                st.session_state.data['stats']['formalName'] = new_name
                st.session_state.data['stats']['population'] = new_pop
                st.session_state.data['stats']['totalGdp'] = new_gdp
                st.session_state.data['details']['military']['numerical']['troopCount'] = new_troops
                st.session_state.data['details']['military']['numerical']['readinessLevel'] = new_ready
                
                save_data(st.session_state.data)
                st.success("국가 정보가 성공적으로 업데이트되었습니다.")
                st.rerun()
        
        st.divider()
        st.subheader("시민 관리")
        users = st.session_state.data.get('users', [])
        st.write(f"총 시민 수: {len(users)}명")
        
        # 시민 추가
        with st.expander("시민 계정 발급"):
            with st.form("add_user"):
                new_u = st.text_input("ID")
                new_p = st.text_input("PW")
                if st.form_submit_button("발급"):
                    if new_u and new_p:
                        users.append({"username": new_u, "password": new_p, "createdAt": datetime.now().timestamp()})
                        st.session_state.data['users'] = users
                        save_data(st.session_state.data)
                        st.success("발급 완료")

elif menu == "마이 페이지":
    if not st.session_state.user:
        st.error("로그인이 필요합니다.")
    else:
        u = st.session_state.user
        st.header(f"👤 {u['username']}님의 시민권")
        st.json(u)

