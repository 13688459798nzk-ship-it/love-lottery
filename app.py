import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(page_title="💖 纪念日快乐", page_icon="🎁")

# --- CSS 美化 (增加一点粉色氛围) ---
st.markdown("""
<style>
    .stButton>button {
        color: white;
        background-color: #FF4B4B;
        border-radius: 10px;
    }
    .stSuccess {
        background-color: #ffebee;
    }
</style>
""", unsafe_allow_html=True)

st.title("💖 纪念日购物车清空计划 💖")
st.write("规则：女朋友上限400元无限抽，男朋友单次200元(首发<100可连抽)")

# --- 1. 初始化购物车数据 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- 2. 侧边栏：女朋友填写数据区域 ---
with st.sidebar:
    st.header("📝 第一步：填写心愿单")
    name = st.text_input("商品名称", placeholder="例如：海蓝之谜")
    price = st.number_input("价格", min_value=1, step=1)
    
    if st.button("加入购物车 🛒"):
        if name and price:
            st.session_state.cart.append({"name": name, "price": price})
            st.success(f"已添加：{name}")
        else:
            st.warning("名字和价格都要写哦！")

    st.divider()
    
    # 显示当前购物车
    st.subheader(f"当前清单 ({len(st.session_state.cart)}件)")
    if st.session_state.cart:
        for item in st.session_state.cart:
            st.text(f"- {item['name']}: {item['price']}元")
        
        if st.button("🗑️ 清空重写"):
            st.session_state.cart = []
            st.rerun()

# --- 3. 主界面：抽奖区域 ---
st.header("🎰 第二步：开始抽奖")

if not st.session_state.cart:
    st.info("👈 请先在左侧侧边栏添加购物车商品，然后在这里抽奖！")
else:
    # 选项卡：切换男女朋友身份
    tab1, tab2 = st.tabs(["👸 女朋友的回合", "🤴 男朋友的回合"])

    # === 女朋友逻辑 ===
    with tab1:
        st.subheader("预算上限：400元")
        if 'gf_budget' not in st.session_state:
            st.session_state.gf_budget = 400
        
        st.metric("剩余额度", f"{st.session_state.gf_budget} 元")

        if st.button("点击抽取 (女朋友) 🎁", key="btn_gf"):
            # 筛选买得起的
            pool = [i for i in st.session_state.cart if i['price'] <= st.session_state.gf_budget]
            
            if not pool:
                st.error("余额不足或没东西可买了！收手吧！")
            else:
                with st.spinner("正在选选中..."):
                    time.sleep(1) # 仪式感
                    gift = random.choice(pool)
                    st.session_state.gf_budget -= gift['price']
                    # 记录战利品
                    st.session_state.logs.append(f"👸 抽中：**{gift['name']}** (¥{gift['price']})")
                    st.balloons() # 撒花特效
                    st.rerun()

    # === 男朋友逻辑 ===
    with tab2:
        st.subheader("单次上限：200元 (连抽机制)")
        
        if st.button("点击抽取 (男朋友) 🎮", key="btn_bf"):
            pool = [i for i in st.session_state.cart if i['price'] <= 200]
            
            if not pool:
                st.error("购物车里没有200元以下的东西，你没得抽了...")
            else:
                with st.spinner("祈祷中..."):
                    time.sleep(1)
                    gift1 = random.choice(pool)
                    msg = f"🤴 第一发：**{gift1['name']}** (¥{gift1['price']})"
                    
                    # 连抽判定
                    if gift1['price'] < 100:
                        msg += " -> 🔥 **触发连抽！**"
                        # 排除刚才抽到的，再抽一次
                        pool2 = [i for i in pool if i['name'] != gift1['name']]
                        if pool2:
                            gift2 = random.choice(pool2)
                            msg += f" -> 第二发：**{gift2['name']}** (¥{gift2['price']})"
                        else:
                            msg += " (可惜没别的200以下商品了)"
                    
                    st.session_state.logs.append(msg)
                    st.snow() # 雪花特效
                    st.rerun()

# --- 4. 战利品展示区 ---
st.divider()
st.subheader("📜 战利品清单")
for log in reversed(st.session_state.logs):
    st.markdown(f"- {log}")