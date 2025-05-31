import streamlit as st

# セッションステートで投稿データを初期化
if 'posts' not in st.session_state:
    st.session_state.posts = []

# アプリケーションのタイトル
st.title('就活管理アプリ')

# 入力フォーム
with st.form(key='job_form'):
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input('志望企業名')
        employee_count = st.text_input('社員数')
    with col2:
        avg_salary = st.text_input('平均年収')
        benefits = st.text_input('福利厚生')

    submitted = st.form_submit_button("登録する")
    if submitted:
        if not company_name:
            st.warning("企業名を入力してください。")
        else:
            st.session_state.posts.append({
                '企業名': company_name,
                '平均年収': avg_salary,
                '社員数': employee_count,
                '福利厚生': benefits
            })
            st.success("登録が完了しました!")

# 登録済みの企業リストを表示
st.subheader("登録済みの志望企業")
for i, post in enumerate(st.session_state.posts, 1):
    with st.expander(f"{i}. {post['企業名']} の詳細"):
        st.write(f"**平均年収:** {post['平均年収']}")
        st.write(f"**社員数:** {post['社員数']}")
        st.write(f"**福利厚生:** {post['福利厚生']}")
