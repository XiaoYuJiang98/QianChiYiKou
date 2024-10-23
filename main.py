import streamlit
import pandas

df = pandas.read_csv("https://raw.githubusercontent.com/XiaoYuJiang98/QianChiYiKou/refs/heads/main/data/v1.csv")

streamlit.set_page_config(
    page_title="自主查询",
    page_icon="🌟",
    layout="wide",
)

def init_filter(df):
    ndf = df.query(
    """
    状态 != '已发货'
    """
    )
    return ndf


def query_data(name=None, series=None, item=None):
    query_str = []
    
    if name:
        query_str.append(f"CN == '{name}'")
        
    if series:
        query_str.append(f"谷子名 == '{series}'")
    
    if item:
        query_str.append(f"制品 == '{item}'")
        
    if query_str:
        query_str_combined = " and ".join(query_str)
        ndf = df.query(query_str_combined)
    else:
        ndf = df
    
    return ndf


def reorder_df(df):
    temp_df_1 = df[df["状态"] == "完成"].copy()
    temp_df_2 = df[df["状态"] == "退补进行中"].copy()
    temp_df_3 = df[df["状态"] == "已到马来西亚"].copy()
    temp_df_4 = df[df["状态"] == "回国中"].copy()
    temp_df_5 = df[df["状态"] == "收国际均摊中"].copy()
    temp_df_6 = df[df["状态"] == "日本仓库排发中"].copy()
    temp_df_7 = df[df["状态"] == "到库"].copy()
    temp_df_8 = df[df["状态"] == "出荷准备中"].copy()
    temp_df_9 = df[df["状态"] == "未出荷"].copy()
    temp_df_10 = df[df["状态"] == "囤货"].copy()
    temp_df_11 = df[df["状态"] == "已发货"].copy()

    ndf = pandas.concat(
        [
            temp_df_1, 
            temp_df_2, 
            temp_df_3,
            temp_df_4,
            temp_df_5,
            temp_df_6,
            temp_df_7,
            temp_df_8,
            temp_df_9,
            temp_df_10,
            temp_df_11,
        ], 
        axis=0
    )
    return ndf.reset_index(drop=True)


name_input = streamlit.selectbox(
    label="CN",
    options=tuple(df["CN"].unique()),
    index=None,
    placeholder="Name to search..."
)

# series_input = streamlit.selectbox(
#     label='谷子名',
#     options=tuple(df["谷子名"].unique()),
#     index=None,
#     placeholder="Series to search..."
# )

# item_input = streamlit.selectbox(
#     label='制品',
#     options=tuple(df["制品"].unique()),
#     index=None,
#     placeholder="Item to search..."
# )


df = init_filter(df)

ndf = query_data(
    name=name_input, 
    series=None,
    item=None
)
ndf = reorder_df(ndf)
streamlit.dataframe(
    ndf, 
    width=1200, 
    height=600,
    use_container_width=False,
)



