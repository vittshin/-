import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# 定义各个页面的函数
def show_data_overview(df):
    st.header("📊 数据概览")
    
    # 显示数据预览
    st.subheader("📋 数据预览")
    st.dataframe(df.head(10))
    
    # 显示处理后的数据
    st.subheader("📊 处理后的数据")
    st.dataframe(df[['税务', '总分']].head(20))
    
    # 创建柱状图
    st.subheader("📈 税务人员评分柱状图")
    
    # 创建交互式柱状图
    fig = px.bar(
        df, 
        x='税务', 
        y='总分',
        title='税务人员评分分布',
        labels={'税务': '税务人员姓名', '总分': '评分'},
        color='总分',
        color_continuous_scale='Viridis',
        height=600
    )
    
    # 更新布局
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        xaxis_title="税务人员姓名",
        yaxis_title="评分",
        title_font_size=20
    )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示统计信息
    st.subheader("📊 统计信息")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总人数", len(df))
    
    with col2:
        st.metric("平均分", f"{df['总分'].mean():.2f}")
    
    with col3:
        st.metric("最高分", f"{df['总分'].max():.2f}")
    
    with col4:
        st.metric("最低分", f"{df['总分'].min():.2f}")
    
    # 显示排名
    st.subheader("🏆 评分排名")
    ranked_df = df[['税务', '总分']].sort_values('总分', ascending=False).reset_index(drop=True)
    ranked_df.index = ranked_df.index + 1
    st.dataframe(ranked_df, height=400)

def show_personal_analysis(df):
    st.header("👤 人员分数解析")
    
    # 选择特定人员
    selected_person = st.selectbox("选择税务人员", df['税务'].unique())
    
    if selected_person:
        person_data = df[df['税务'] == selected_person].iloc[0]
        
        # 显示个人信息
        col1, col2 = st.columns(2)
        with col1:
            st.metric("姓名", selected_person)
        with col2:
            st.metric("总分", f"{person_data['总分']:.2f}")
        
        # 显示该人员在所有人员中的排名
        ranked_df = df[['税务', '总分']].sort_values('总分', ascending=False).reset_index(drop=True)
        rank = ranked_df[ranked_df['税务'] == selected_person].index[0] + 1
        total_people = len(df)
        
        st.info(f"🏅 {selected_person} 在所有 {total_people} 名人员中排名第 {rank} 位")
        
        # 创建个人分数对比图
        st.subheader("📊 个人分数对比")
        
        # 创建水平条形图，显示该人员与平均分的对比
        fig = go.Figure()
        
        # 添加该人员的分数
        fig.add_trace(go.Bar(
            name=selected_person,
            x=[person_data['总分']],
            y=['个人分数'],
            orientation='h',
            marker_color='lightblue',
            text=[f"{person_data['总分']:.2f}"],
            textposition='auto',
        ))
        
        # 添加平均分
        avg_score = df['总分'].mean()
        fig.add_trace(go.Bar(
            name='平均分',
            x=[avg_score],
            y=['平均分'],
            orientation='h',
            marker_color='orange',
            text=[f"{avg_score:.2f}"],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f"{selected_person} 与平均分对比",
            xaxis_title="评分",
            yaxis_title="",
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示该人员与最高分和最低分的对比
        st.subheader("📈 分数区间分析")
        
        max_score = df['总分'].max()
        min_score = df['总分'].min()
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = person_data['总分'],
            delta = {'reference': avg_score, 'valueformat': '.2f'},
            gauge = {
                'axis': {'range': [min_score, max_score]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [min_score, avg_score], 'color': "lightgray"},
                    {'range': [avg_score, max_score], 'color': "lightgreen"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_score}}))
        
        fig2.update_layout(
            title=f"{selected_person} 评分仪表盘",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)

def show_group_analysis(df):
    st.header("👥 组别维度计分")
    
    # 检查是否有组别信息
    if '组别' in df.columns:
        # 按组别统计
        group_stats = df.groupby('组别').agg({
            '总分': ['count', 'mean', 'max', 'min']
        }).round(2)
        
        group_stats.columns = ['人数', '平均分', '最高分', '最低分']
        group_stats = group_stats.reset_index()
        
        st.subheader("📊 各组别统计信息")
        st.dataframe(group_stats)
        
        # 创建组别平均分对比图
        st.subheader("📈 各组别平均分对比")
        
        fig = px.bar(
            group_stats,
            x='组别',
            y='平均分',
            title='各组别平均分对比',
            labels={'平均分': '平均分', '组别': '组别'},
            color='平均分',
            color_continuous_scale='Blues',
            height=500
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            xaxis_title="组别",
            yaxis_title="平均分",
            title_font_size=20
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示各组别人数分布
        st.subheader("👥 各组别人数分布")
        
        fig2 = px.pie(
            group_stats,
            values='人数',
            names='组别',
            title='各组别人数分布',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # 显示详细数据
        st.subheader("📋 各组别详细数据")
        
        for group in df['组别'].unique():
            with st.expander(f"📂 {group} 组详细数据"):
                group_df = df[df['组别'] == group][['税务', '总分']].sort_values('总分', ascending=False)
                st.dataframe(group_df)
                
                # 显示该组统计信息
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("人数", len(group_df))
                with col2:
                    st.metric("平均分", f"{group_df['总分'].mean():.2f}")
                with col3:
                    st.metric("最高分", f"{group_df['总分'].max():.2f}")
                with col4:
                    st.metric("最低分", f"{group_df['总分'].min():.2f}")
    else:
        st.warning("⚠️ 数据中没有找到'组别'列，无法进行组别维度分析。")
        st.info("请确保Excel文件中的'积分计算'工作表包含'组别'列。")

# 设置页面标题
st.set_page_config(page_title="税务合规岗计分统计", page_icon="📊", layout="wide")

# 侧边栏导航
st.sidebar.title("📊 导航菜单")
page = st.sidebar.radio("选择功能", ["数据概览", "人员分数解析", "组别维度计分"])

# 页面标题
st.title("📊 税务合规岗计分统计平台")
st.markdown("---")

# 文件上传组件（在侧边栏中）
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("请上传Excel文件", type=['xlsx', 'xls'], key="file_uploader")

# 全局变量存储数据
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.processed = False

# 处理上传的文件
if uploaded_file is not None:
    try:
        # 读取Excel文件中的"积分计算"工作表
        df = pd.read_excel(uploaded_file, sheet_name='积分计算')
        
        # 数据清洗：移除空行和标题行
        # 找到包含"税务"列名的行作为标题行
        header_row = None
        for i, row in df.iterrows():
            if '税务' in str(row.values):
                header_row = i
                break
        
        if header_row is not None:
            # 重新读取，指定标题行
            df = pd.read_excel(uploaded_file, sheet_name='积分计算', header=header_row)
            
            # 只保留有数据的行
            df = df.dropna(subset=['税务', '总分'])
            
            # 存储到session state
            st.session_state.df = df
            st.session_state.processed = True
            st.sidebar.success("✅ 文件上传并处理成功！")
        else:
            st.error("无法找到包含'税务'列的有效数据，请检查Excel文件格式。")
            
    except Exception as e:
        st.error(f"处理文件时出错：{str(e)}")
        st.info("请确保上传的文件包含名为'积分计算'的工作表，并且该工作表包含'税务'和'总分'列。")

# 根据选择的页面显示不同内容
if st.session_state.processed and st.session_state.df is not None:
    df = st.session_state.df
    
    if page == "数据概览":
        show_data_overview(df)
    elif page == "人员分数解析":
        show_personal_analysis(df)
    elif page == "组别维度计分":
        show_group_analysis(df)
else:
    # 显示欢迎信息和文件上传提示
    st.info("👈 请在左侧边栏上传Excel文件以开始使用")
    
    # 显示使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ### 使用步骤：
        1. 在左侧边栏点击"Browse files"按钮或拖拽文件到上传区域
        2. 选择包含税务合规岗计分数据的Excel文件
        3. 使用侧边栏导航选择不同功能页面
        
        ### 文件要求：
        - 文件格式：.xlsx 或 .xls
        - 必须包含名为"积分计算"的工作表
        - 工作表中必须包含"税务"(姓名)和"总分"(评分)列
        
        ### 功能页面：
        - **数据概览**：查看整体数据概览和统计信息
        - **人员分数解析**：分析个人评分详情
        - **组别维度计分**：按组别查看评分分布
        """)

# 添加底部信息
st.markdown("---")
st.caption("💡 提示：上传文件后，使用左侧导航栏切换不同功能页面")