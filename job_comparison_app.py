import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ページ設定
st.set_page_config(
    page_title="就活管理アプリ - 統合版",
    page_icon="📊",
    layout="wide"
)

# セッションステートで投稿データを初期化
if 'companies' not in st.session_state:
    st.session_state.companies = []

def add_company_data(name, salary, employees, benefits):
    """企業データを追加する関数"""
    st.session_state.companies.append({
        '企業名': name,
        '平均年収': salary,
        '社員数': employees,
        '福利厚生': benefits
    })

def get_companies_dataframe():
    """企業データをDataFrameに変換する関数"""
    if not st.session_state.companies:
        return pd.DataFrame()
    return pd.DataFrame(st.session_state.companies)

def create_bar_chart(data, x_col, y_col, title, y_label, color='#1f77b4'):
    """棒グラフを作成する関数"""
    if data.empty:
        return None
    
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        title=title,
        color_discrete_sequence=[color]
    )
    
    # グラフのスタイル設定
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        xaxis_title="企業名",
        yaxis_title=y_label,
        showlegend=False,
        height=500,
        font=dict(size=14)
    )
    
    # バーの上に数値を表示
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        textfont_size=12
    )
    
    return fig

def parse_salary(salary_str):
    """年収文字列を数値に変換する関数"""
    if not salary_str:
        return 0
    # 数字以外の文字を除去して数値に変換
    import re
    numbers = re.findall(r'\d+', str(salary_str))
    if numbers:
        return int(numbers[0])
    return 0

def parse_employees(employees_str):
    """社員数文字列を数値に変換する関数"""
    if not employees_str:
        return 0
    import re
    numbers = re.findall(r'\d+', str(employees_str))
    if numbers:
        return int(numbers[0])
    return 0

def main():
    # タイトル
    st.title("📊 就活管理アプリ")
    # st.markdown("企業データの登録と比較ができるアプリです")
    st.markdown("---")
    
    # サイドバーでページを選択
    page = st.sidebar.selectbox(
        "ページを選択",
        ["企業登録", "企業比較", "登録済み企業一覧"]
    )
    
    if page == "企業登録":
        st.header("🏢 企業情報登録")
        
        # 入力フォーム
        with st.form(key='job_form'):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input('志望企業名', placeholder="例: 株式会社サンプル")
                employee_count = st.text_input('社員数', placeholder="例: 1000人")
            with col2:
                avg_salary = st.text_input('平均年収', placeholder="例: 500万円")
                benefits = st.text_area('福利厚生', placeholder="例: 健康保険、厚生年金、有給休暇、フレックスタイム")

            submitted = st.form_submit_button("登録する")
            if submitted:
                if not company_name:
                    st.warning("企業名を入力してください。")
                else:
                    add_company_data(company_name, avg_salary, employee_count, benefits)
                    st.success(f"「{company_name}」の登録が完了しました!")
                    st.balloons()
        
        # 現在の登録数を表示
        st.info(f"現在の登録企業数: {len(st.session_state.companies)}社")
    
    elif page == "企業比較":
        st.header("📊 企業比較")
        
        df = get_companies_dataframe()
        
        if df.empty:
            st.warning("比較するデータがありません。まず「企業登録」ページで企業情報を登録してください。")
            return
        
        # 比較項目を選択
        comparison_item = st.selectbox(
            "比較したい項目を選択してください",
            ["年収", "社員数", "福利厚生"]
        )
        
        if comparison_item == "年収":
            st.subheader("💰 年収比較")
            
            # 年収データを数値に変換
            df['年収_数値'] = df['平均年収'].apply(parse_salary)
            salary_data = df[df['年収_数値'] > 0]
            
            if not salary_data.empty:
                # 統計情報
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("最高年収", f"{salary_data['年収_数値'].max()}万円")
                with col2:
                    st.metric("最低年収", f"{salary_data['年収_数値'].min()}万円")
                with col3:
                    st.metric("平均年収", f"{salary_data['年収_数値'].mean():.0f}万円")
                with col4:
                    st.metric("年収差", f"{salary_data['年収_数値'].max() - salary_data['年収_数値'].min()}万円")
                
                # 棒グラフ
                fig = create_bar_chart(salary_data, '企業名', '年収_数値', "企業別年収比較", "年収（万円）", '#2E8B57')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # データテーブル
                st.subheader("詳細データ")
                display_data = salary_data[['企業名', '平均年収', '年収_数値']].sort_values('年収_数値', ascending=False)
                st.dataframe(display_data, use_container_width=True)
            else:
                st.warning("年収データが正しく入力されていません。数値で入力してください。")
        
        elif comparison_item == "社員数":
            st.subheader("👥 社員数比較")
            
            # 社員数データを数値に変換
            df['社員数_数値'] = df['社員数'].apply(parse_employees)
            employee_data = df[df['社員数_数値'] > 0]
            
            if not employee_data.empty:
                # 統計情報
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("最大社員数", f"{employee_data['社員数_数値'].max():,}人")
                with col2:
                    st.metric("最小社員数", f"{employee_data['社員数_数値'].min():,}人")
                with col3:
                    st.metric("平均社員数", f"{employee_data['社員数_数値'].mean():.0f}人")
                with col4:
                    total_employees = employee_data['社員数_数値'].sum()
                    st.metric("総社員数", f"{total_employees:,}人")
                
                # 棒グラフ
                fig = create_bar_chart(employee_data, '企業名', '社員数_数値', "企業別社員数比較", "社員数（人）", '#FF6347')
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # データテーブル
                st.subheader("詳細データ")
                display_data = employee_data[['企業名', '社員数', '社員数_数値']].sort_values('社員数_数値', ascending=False)
                st.dataframe(display_data, use_container_width=True)
            else:
                st.warning("社員数データが正しく入力されていません。数値で入力してください。")
        
        elif comparison_item == "福利厚生":
            st.subheader("🏢 福利厚生比較")
            
            # 福利厚生の文字数で比較（簡易的な充実度指標）
            df['福利厚生_充実度'] = df['福利厚生'].apply(lambda x: len(str(x)) if x else 0)
            benefits_data = df[df['福利厚生_充実度'] > 0]
            
            if not benefits_data.empty:
                # 統計情報
                col1, col2, col3 = st.columns(3)
                with col1:
                    best_idx = benefits_data['福利厚生_充実度'].idxmax()
                    best_company = benefits_data.loc[best_idx, '企業名']
                    st.metric("最も充実", best_company)
                
                with col2:
                    avg_score = benefits_data['福利厚生_充実度'].mean()
                    st.metric("平均文字数", f"{avg_score:.0f}文字")
                
                with col3:
                    companies_with_benefits = len(benefits_data)
                    st.metric("福利厚生記載企業", f"{companies_with_benefits}社")
                
                # 福利厚生詳細表示
                st.subheader("福利厚生詳細")
                for _, row in benefits_data.iterrows():
                    with st.expander(f"{row['企業名']} の福利厚生"):
                        st.write(row['福利厚生'])
                
                # 充実度ランキング
                st.subheader("福利厚生充実度ランキング")
                ranking_data = benefits_data[['企業名', '福利厚生_充実度']].sort_values('福利厚生_充実度', ascending=False)
                ranking_data.index = range(1, len(ranking_data) + 1)
                st.dataframe(ranking_data, use_container_width=True)
            else:
                st.warning("福利厚生データが入力されていません。")
    
    elif page == "登録済み企業一覧":
        st.header("📋 登録済み企業一覧")
        
        if not st.session_state.companies:
            st.info("まだ企業が登録されていません。「企業登録」ページから企業情報を登録してください。")
        else:
            # 企業数表示
            st.metric("登録企業数", f"{len(st.session_state.companies)}社")
            
            # 企業リストを表示
            for i, company in enumerate(st.session_state.companies, 1):
                with st.expander(f"{i}. {company['企業名']} の詳細"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**平均年収:** {company['平均年収']}")
                        st.write(f"**社員数:** {company['社員数']}")
                    with col2:
                        st.write(f"**福利厚生:**")
                        st.write(company['福利厚生'])
                    
                    # 削除ボタン
                    if st.button(f"削除", key=f"delete_{i}"):
                        st.session_state.companies.pop(i-1)
                        st.rerun()
            
            # 全データクリアボタン
            if st.button("全データをクリア", type="secondary"):
                if st.checkbox("本当に全データを削除しますか？"):
                    st.session_state.companies = []
                    st.success("全データを削除しました。")
                    st.rerun()
    
    # フッター
    st.markdown("---")
    st.markdown("💡 **使い方**: 企業登録 → 企業比較 の順で使用することをお勧めします！")

if __name__ == "__main__":
    main()