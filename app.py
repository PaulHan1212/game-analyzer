import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="同盟未達標名單工具", layout="wide")

st.title("同盟未達標名單分析")

uploaded_file = st.file_uploader("請上傳同盟統計 CSV 檔案", type=["csv"])

def get_required_score(power):
    if power < 20000:
        return 20000
    elif power < 25000:
        return 30000
    elif power < 30000:
        return 40000
    elif power < 35000:
        return 50000
    elif power < 40000:
        return 80000
    else:
        return 120000

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    tab1, tab2 = st.tabs(["未達標名單", "貢獻排行名單"])

    with tab1:
        df["應達戰功"] = df["勢力值"].apply(get_required_score)

        result = df[df["戰功本週"] < df["應達戰功"]].copy()

        result["缺少戰功"] = result["應達戰功"] - result["戰功本週"]
        result["需繳資源"] = result["缺少戰功"].apply(
            lambda x: math.ceil(x / 10000) * 600000
        )

        total_resource = result["需繳資源"].sum()

        result = result[
            ["成員", "貢獻排行", "勢力值", "戰功本週", "應達戰功", "缺少戰功", "需繳資源", "分組"]
        ]

        result = result.sort_values(by="分組").reset_index(drop=True)

        result["成員"] = (
            result["成員"]
            + result["缺少戰功"].apply(lambda x: f"{math.ceil(x / 10000) * 80}萬")
        )

        st.subheader("未達標名單")
        st.write(f"共有 {len(result)} 人未達標")
        st.write(f"共須繳交資源：{total_resource:,}")

        st.dataframe(result, use_container_width=True)

        csv = result.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="下載未達標名單 CSV",
            data=csv,
            file_name="未達標名單.csv",
            mime="text/csv"
        )

    with tab2:
        rank_df = df.copy()

        rank_df = rank_df.sort_values(by="貢獻排行").reset_index(drop=True)

        rank_df["貢獻排名＋成員"] = (
            rank_df["成員"].astype(str)
        )

        rank_df = rank_df[
            ["貢獻排名＋成員", "貢獻本週", "戰功本週", "助攻本週", "捐獻本週", "勢力值", "分組"]
        ]

        st.subheader("貢獻排行名單")
        st.dataframe(rank_df, use_container_width=True)

        rank_csv = rank_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="下載貢獻排行名單 CSV",
            data=rank_csv,
            file_name="貢獻排行名單.csv",
            mime="text/csv"
        )

else:
    st.info("請先上傳 CSV 檔案")
