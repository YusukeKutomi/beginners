import streamlit as st
import pandas as pd

def app():
    st.set_page_config(layout="centered", page_title="就活管理アプリ")
    st.title("🏢就活管理アプリ")
    st.markdown("---")

    # セッションステートにデータフレームを初期化
    # アプリが起動したときに一度だけ実行され、データを永続化します
    if 'company_data' not in st.session_state:
        st.session_state.company_data = pd.DataFrame(columns=["企業名", "年収 (万円)", "社員数", "福利厚生"])

    # --- 企業情報入力フォーム ---
    st.header("🖊️ 企業情報入力")
    with st.form("company_info_form", clear_on_submit=True): # clear_on_submit=True で登録後にフォームをクリア
        company_name = st.text_input("**企業名**", help="企業の正式名称を入力してください")
        annual_salary = st.number_input("**年収 (万円)**", min_value=0, step=10, help="平均年収または想定年収を万円単位で入力してください")
        num_employees = st.number_input("**社員数**", min_value=0, step=1, help="現在の社員数を入力してください")
        benefits = st.text_area("**福利厚生**", help="代表的な福利厚生（例: 住宅手当、リモートワーク制度、研修制度など）を記述してください")

        submitted = st.form_submit_button("✅ 情報登録")

        if submitted:
            if company_name and annual_salary >= 0 and num_employees >= 0:
                # 新しいデータをデータフレームに追加
                new_data = pd.DataFrame([{
                    "企業名": company_name,
                    "年収 (万円)": int(annual_salary),
                    "社員数": int(num_employees),
                    "福利厚生": benefits
                }])
                st.session_state.company_data = pd.concat([st.session_state.company_data, new_data], ignore_index=True)
                st.success("企業情報を登録しました！")
            else:
                st.error("⚠️ 企業名、年収、社員数は必須項目です。正しく入力してください。")

    st.markdown("---")

    # --- 登録済み企業情報の一覧 ---
    st.header("📋 登録済み企業情報一覧")
    if not st.session_state.company_data.empty:
        # データフレームを表示
        st.dataframe(st.session_state.company_data)
        
        # CSVダウンロードボタン
        csv = st.session_state.company_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 CSVでダウンロード",
            data=csv,
            file_name="企業情報リスト.csv",
            mime="text/csv",
            help="現在表示されている企業情報をCSV形式でダウンロードします"
        )
    else:
        st.info("💡 まだ企業情報が登録されていません。上記フォームから登録してください。")

    st.markdown("---")

    # --- データクリアボタン (オプション) ---
    st.header("🗑️ データ操作")
    if st.button("全ての企業情報をクリア", type="secondary"): # type="secondary" でボタンの色を変える
        st.session_state.company_data = pd.DataFrame(columns=["企業名", "年収 (万円)", "社員数", "福利厚生"])
        st.success("全ての企業情報をクリアしました。")

if __name__ == "__main__":
    app()