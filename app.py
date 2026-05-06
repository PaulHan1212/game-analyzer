import streamlit as st
import pandas as pd

st.set_page_config(page_title="未達標名單工具", layout="wide")

st.title("同盟未達標名單分析")

uploaded_file = st.file_uploader("請上傳同盟統計 CSV 檔案", type=["csv"])

def get_required_score(power):
    if power < 20000:
        return 50000
    elif power < 25000:
        return 75000
    elif power < 30000:
        return 100000
    elif power < 35000:
        return 150000
    elif power < 40000:
        return 200000
    else:
        return 300000

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # 加上應達戰功
    df["應達戰功"] = df["勢力值"].apply(get_required_score)

    # 找未達標
    result = df[df["戰功本週"] < df["應達戰功"]]

    result = result[["成員", "勢力值", "戰功本週", "應達戰功", "分組"]]
    result = result.sort_values(by="分組").reset_index(drop=True)

    st.subheader("未達標名單")
    st.write(f"共有 {len(result)} 人未達標")

    st.dataframe(result, use_container_width=True)

    csv = result.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="下載未達標名單 CSV",
        data=csv,
        file_name="未達標名單.csv",
        mime="text/csv"
    )
else:
    st.info("請先上傳 CSV 檔案")
