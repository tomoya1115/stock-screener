import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="配当スクリーナー", layout="centered")
st.title("📊 高配当株スクリーナー")
st.caption("カブタンから配当利回り4%以上の銘柄を表示")

CODES = [
    "1605", "1893", "2914", "4502", "5020",
    "5101", "5411", "6301", "7011", "8001",
    "8002", "8031", "8058", "9101", "9104",
    "9107", "9432", "9433", "9434", "9502"
]

def get_data(code):
    url = f"https://kabutan.jp/stock/?code={code}"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        name = soup.select_one("h1").text.strip() if soup.select_one("h1") else code
        tables = soup.find_all("table")
        for t in tables:
            for tr in t.find_all("tr"):
                if "配当利回り" in tr.text:
                    tds = tr.find_all("td")
                    if tds:
                        val = tds[0].text.strip().replace("%","")
                        return {"コード": code, "銘柄": name, "利回り(%)": float(val)}
    except:
        pass
    return None

if st.button("🔄 データ取得"):
    results = []
    bar = st.progress(0)
    for i, code in enumerate(CODES):
        d = get_data(code)
        if d and d["利回り(%)"] >= 4.0:
            results.append(d)
        bar.progress((i+1)/len(CODES))
    
    if results:
        df = pd.DataFrame(results).sort_values("利回り(%)", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("該当銘柄なし")
