import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(page_title="🐔 & 🐷 的纪念日", page_icon="💖", layout="wide")

# --- CSS 美化 (配色微调) ---
st.markdown("""
<style>
    .stButton>button {
        color: white;
        background-color: #FF69B4; /* 换个更粉嫩的颜色 */
        border-radius: 12px;
        height: 50px;
        width: 100%;
        font-weight: bold;
    }
    .stSuccess {
        background-color: #fff0f5;
    }
</style>
""", unsafe_allow_html=True)

st.title("💖 爱酱鸡 & 臭拉黄考猪的纪念日庆典 💖")
st.info("规则：🐔 爱酱鸡上限400元无限抽，🐷 臭拉黄考猪单次200元(首发<100可连抽)")

# --- 1. 初始化两辆购物车 ---
if 'cart_chicken' not in st.session_state:
    st.session_state.cart_chicken = [] # 爱酱鸡的购物车
if 'cart_pig' not in st.session_state:
    st.session_state.cart_pig = [] # 臭拉黄考猪的购物车
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- 2. 侧边栏：分开进货 ---
with st.sidebar:
    st.header("📝 第一步：填写心愿单")
    
    # 核心修改：专属昵称选择
    who = st.radio("🎁 这个礼物是给谁的？", ["🐔 爱酱鸡", "🐷 臭拉黄考猪"])
    
    name = st.text_input("礼物名称", placeholder="例如：SK-II / 机械键盘")
    price = st.number_input("价格", min_value=1, step=1)
    
    # 新增功能：上传图片
    img_file = st.file_uploader("上传礼物图片 (可选)", type=['png', 'jpg', 'jpeg', 'webp'])
    
    if st.button("加入心愿单 🛒"):
        if name and price:
            # 把图片对象也存进去
            new_item = {"name": name, "price": price, "image": img_file}
            
            if who == "🐔 爱酱鸡":
                st.session_state.cart_chicken.append(new_item)
                st.success(f"已加入【爱酱鸡】清单：{name}")
            else:
                st.session_state.cart_pig.append(new_item)
                st.success(f"已加入【臭拉黄考猪】清单：{name}")
        else:
            st.warning("名字和价格都要写哦！")

    st.divider()
    
    # 分开展示两个清单
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🐔 爱酱鸡清单")
        if st.session_state.cart_chicken:
            for item in st.session_state.cart_chicken:
                st.caption(f"{item['name']} (¥{item['price']})")
                # 如果有图，显示一个小缩略图
                if item['image']:
                    st.image(item['image'], width=100)
        else:
            st.caption("空空如也")
            
    with col2:
        st.subheader("🐷 臭猪清单")
        if st.session_state.cart_pig:
            for item in st.session_state.cart_pig:
                st.caption(f"{item['name']} (¥{item['price']})")
                if item['image']:
                    st.image(item['image'], width=100)
        else:
            st.caption("空空如也")

    if st.button("🗑️ 清空所有数据"):
        st.session_state.cart_chicken = []
        st.session_state.cart_pig = []
        st.session_state.logs = []
        st.rerun()

# --- 3. 主界面：分开抽奖 ---
st.header("🎰 第二步：开始抽奖")

# 选项卡：切换身份
tab1, tab2 = st.tabs(["🐔 爱酱鸡的主场", "🐷 臭拉黄考猪的主场"])

# === 爱酱鸡逻辑 ===
with tab1:
    st.subheader("预算上限：400元")
    if 'chicken_budget' not in st.session_state:
        st.session_state.chicken_budget = 400
    
    st.metric("爱酱鸡剩余额度", f"{st.session_state.chicken_budget} 元")

    if not st.session_state.cart_chicken:
        st.warning("👈 你的购物车是空的，爱酱鸡快去侧边栏加礼物！")
    else:
        if st.button("✨ 爱酱鸡点击抽取 ✨", key="btn_chicken"):
            # 筛选买得起的
            pool = [i for i in st.session_state.cart_chicken if i['price'] <= st.session_state.chicken_budget]
            
            if not pool:
                st.error("余额不足，或者清单里没有买得起的了！")
            else:
                with st.spinner("正在为爱酱鸡挑选礼物..."):
                    time.sleep(1.5) 
                    gift = random.choice(pool)
                    st.session_state.chicken_budget -= gift['price']
                    
                    # 移出购物车
                    st.session_state.cart_chicken.remove(gift)
                    
                    st.session_state.logs.append(f"🐔 爱酱鸡抽中：**{gift['name']}** (¥{gift['price']})")
                    
                    # 赢了大奖展示区
                    st.balloons()
                    st.success(f"🎉 恭喜爱酱鸡抽中：{gift['name']}！")
                    if gift['image']:
                        st.image(gift['image'], caption="快让他买单！", use_container_width=True)
                    
                    time.sleep(2) # 停留一下让用户看完
                    st.rerun()

# === 臭拉黄考猪逻辑 ===
with tab2:
    st.subheader("单次上限：200元 (连抽机制)")
    
    if not st.session_state.cart_pig:
        st.warning("👈 你的购物车是空的，臭猪快去侧边栏加礼物！")
    else:
        if st.button("🔨 臭拉黄考猪点击抽取 🔨", key="btn_pig"):
            pool = [i for i in st.session_state.cart_pig if i['price'] <= 200]
            
            if not pool:
                st.error("你的购物车里没有200元以下的东西了...")
            else:
                with st.spinner("臭猪祈祷中..."):
                    time.sleep(1.5)
                    gift1 = random.choice(pool)
                    st.session_state.cart_pig.remove(gift1)
                    
                    msg = f"🐷 臭猪第一发：**{gift1['name']}** (¥{gift1['price']})"
                    st.success(f"第一发抽中：{gift1['name']}")
                    if gift1['image']:
                        st.image(gift1['image'], width=300)

                    # 连抽判定
                    if gift1['price'] < 100:
                        msg += " -> 🔥 **触发连抽！**"
                        st.info("🔥 价格低于100，触发连抽奖励！正在抽第二发...")
                        time.sleep(1)
                        
                        pool2 = [i for i in st.session_state.cart_pig if i['price'] <= 200]
                        if pool2:
                            gift2 = random.choice(pool2)
                            st.session_state.cart_pig.remove(gift2)
                            msg += f" -> 第二发：**{gift2['name']}** (¥{gift2['price']})"
                            st.success(f"第二发抽中：{gift2['name']}")
                            if gift2['image']:
                                st.image(gift2['image'], width=300)
                        else:
                            msg += " (可惜没别的200以下商品了)"
                            st.warning("没东西可连抽了...")
                    
                    st.session_state.logs.append(msg)
                    st.snow()
                    time.sleep(3) # 停留久一点
                    st.rerun()

# --- 4. 战利品展示区 ---
st.divider()
st.subheader("📜 战利品清单")
for log in reversed(st.session_state.logs):
    st.markdown(f"- {log}")