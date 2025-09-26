# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="CSV 折线图查看器", layout="wide")
st.title("📈 CSV 折线图查看器")

@st.cache_data(show_spinner=False)
def load_csv(file):
    return pd.read_csv(file)

uploaded = st.file_uploader("上传 CSV 文件", type=["csv"])
if not uploaded:
    st.stop()

df = load_csv(uploaded)
all_cols = df.columns.tolist()
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

# ========== 数据预览：可折叠加载 ==========
preview_rows = st.session_state.get("preview_rows", 100)

with st.expander("📄 数据预览（点击展开）"):
    st.dataframe(df.head(preview_rows))
    if preview_rows < len(df):
        cols = st.columns([10, 20])          # 让按钮靠左
        with cols[0]:
            if st.button("load_more", help="点击预览下100行数据", key="load_more"):
                st.session_state.preview_rows = preview_rows + 100
                st.rerun()

# ========== 绘图配置 ==========
st.subheader("折线图配置")
col1, col2 = st.columns([1, 3])

with col1:
    # X 轴：可选 None
    x_sel = st.selectbox("X 轴（选 None 则用索引）", ["None"] + all_cols)

    # Y 轴：多选
    y_sel = st.multiselect("Y 轴（多选）", numeric_cols, default=numeric_cols[:3])

    if not y_sel:
        st.warning("请至少选择一列 Y 轴数据")
        st.stop()

# 准备 X 数据
if x_sel == "None":
    x_data = list(range(len(df)))
    x_name = "index"
else:
    x_data = df[x_sel]
    x_name = x_sel

# 画图
fig = go.Figure()
for col in y_sel:
    fig.add_trace(go.Scatter(x=x_data, y=df[col], mode="lines", name=col))

fig.update_layout(
    title=f"折线图：{', '.join(y_sel)}",
    xaxis_title=x_name,
    yaxis_title="值",
    hovermode="x unified",
    template="plotly_white",
)
st.plotly_chart(fig, use_container_width=True)