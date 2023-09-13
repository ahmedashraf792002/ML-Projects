import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Load Data
class Load_Data():
    def data(self, file):
        try:
            if file.type == 'application/vnd.ms-excel':
                return pd.read_excel(file)
            elif file.type == 'text/csv':
                return pd.read_csv(file)
            elif file.type == 'text/tab-separated-values':
                return pd.read_csv(file, sep='\t')
        except Exception as e:
            print(f"An error occurred: {e}")
#Handel Missing
def c_missing(data,col,categorical_imputation):
    for c in col:
        if categorical_imputation=='mode':
            mode_value = data[c].mode()[0]
            data[c].fillna(mode_value, inplace=True)
        elif categorical_imputation=='ffill':
            data[c].ffill(inplace=True)
        elif categorical_imputation=='bfill':
            data[c].bfill(inplace=True)
    st.success('Columns Handel successfully.')
    return data
def n_missing(data,col,numeric_imputation):
    for c in col:
        if numeric_imputation=='mean':
            mean_value = data[c].mean()
            data[c].fillna(mean_value, inplace=True)
        elif numeric_imputation=='median':
            median_value = data[c].median()
            data[c].fillna(median_value, inplace=True)
        elif numeric_imputation=='ffill':
            data[c].ffill(inplace=True)
        elif numeric_imputation=='bfill':
            data[c].bfill(inplace=True)
    st.success('Columns Handel successfully.')
    return data
class EDA:
    #Histogram For Numerical Feature
  def numerical_visualization_hist(self,data):
    col=data.select_dtypes(include='number').columns
    plt.figure(figsize=(20, int(10 *np.ceil(len(col)/2))))
    for i, col_name in enumerate(col):
        plt.subplot(int(np.ceil(len(col)/2)),2,i+1)
        data[col_name].plot(kind='hist',color='red')
        plt.title(f"histogram for {col_name}",fontsize=20)
        plt.ylabel('Count',fontsize=15)
        plt.xlabel('Value',fontsize=15)
        plt.grid(True)
        plt.xticks(rotation=15)
#BoxPlot For Numerical Feature 
  def numerical_visualization_box(self,data):
    col=data.select_dtypes(include='number').columns
    plt.figure(figsize=(20, int(10 *np.ceil(len(col)/2))))
    for i, col_name in enumerate(col):
        plt.subplot(int(np.ceil(len(col)/2)),2,i+1)
        sns.boxplot(data[col_name],color='y')
        plt.title(f"BoxPlot for {col_name}",fontsize=20)
        plt.ylabel('Count',fontsize=15)
        plt.xlabel('Value',fontsize=15)
        plt.grid(True)
        plt.xticks(rotation=15)
#Violin For Numerical Feature
  def numerical_visualization_violin(self,data):
    col=data.select_dtypes(include='number').columns
    plt.figure(figsize=(20, int(10 *np.ceil(len(col)/2))))
    for i, col_name in enumerate(col):
        plt.subplot(int(np.ceil(len(col)/2)),2,i+1)
        sns.violinplot(data[col_name],color='y')
        plt.title(f"ViolinPlot for {col_name}",fontsize=20)
        plt.ylabel('Count',fontsize=15)
        plt.xlabel('Value',fontsize=15)
        plt.grid(True)
        plt.xticks(rotation=15)
#BarPlot For Categorical Feature
  def categorical_visualization_bar(self,data):
    col=data.select_dtypes(include='object').columns
    plt.figure(figsize=(20, int(10 *np.ceil(len(col)/2))))
    for i, col_name in enumerate(col):
        plt.subplot(int(np.ceil(len(col)/2)),2,i+1)
        if len(data[col_name].value_counts())>15:
            data[col_name].value_counts().sort_values(ascending=False).head(20).plot(kind='bar',color=['r','b','y'])
            plt.title(f"BarPlot For top 20 values {col_name} to max 20",fontsize=20)
        else:
            data[col_name].value_counts().plot(kind='bar',color=['r','b','y'])
            plt.title(f"BarPlot for {col_name}",fontsize=20)             
        plt.ylabel('Count',fontsize=15)
        plt.xlabel('Value',fontsize=15)
        plt.grid(True)
        plt.xticks(rotation=15)
#PiePlot For Categorical Feature
  def categorical_visualization_pie(self,data):
    col=data.select_dtypes(include='object').columns
    plt.figure(figsize=(20, int(10 *np.ceil(len(col)/2))))
    for i, col_name in enumerate(col):
        plt.subplot(int(np.ceil(len(col)/2)),2,i+1)
        if len(data[col_name].value_counts())>15:
            plt.pie(data[col_name].value_counts().sort_values(ascending=False).head(20),labels=list(data[col_name].value_counts().sort_values(ascending=False).head(20).index),autopct ='%1.2f%%')
            plt.title(f"PiePlot for top 20 values {col_name} to max 20",fontsize=20)
        else:
            plt.pie(data[col_name].value_counts(),labels=list(data[col_name].value_counts().index),autopct ='%1.2f%%')
            plt.title(f"BarPlot for {col_name}",fontsize=20)             
        plt.xticks(rotation=30)  
#HeatMap For Numerical Feature
  def heatmap_for_numerical(self,data):
    da=data[data.select_dtypes(include='number').columns]
    plt.figure(figsize=(20,10))
    sns.heatmap(da.corr(),annot=True,cbar=False,cmap='RdBu')
    return da.corr()
# Sidebar
with st.sidebar:
    choice = st.radio("Choose Your Operation", ["Upload Your Data", "Data Exploration","Data Preparing","EDA","Model"])
# Upload Your Data
if choice == "Upload Your Data":
    st.title("Upload Your Dataset please!")
    path = st.file_uploader("Upload Your Dataset")
    if path:
        obj = Load_Data()
        data = obj.data(path)
        data.to_csv("Data_auto.csv",index=None)
        st.dataframe(data)

# Data Exploration
elif choice == "Data Exploration":
    st.title("Data Exploration")
    box = st.selectbox('Exploration Operation', ['', 'Shape', 'Info', 'Describe', 'Describe Object', 'NULL Data', 'Columns',
                                               'Object Columns', 'Numerical Columns', 'Duplicate'])
    data=pd.read_csv('Data_auto.csv', index_col=None)
    if box == 'Shape':
        st.write(data.shape)
    elif box == 'Info':
        st.write(data.dtypes)
    elif box == 'Describe':
        st.write(data.describe())
    elif box == 'Describe Object':
        st.write(data.describe(include='O'))
    elif box == 'NULL Data':
        st.write(data.isna().sum())
    elif box == 'Columns':
        st.write(data.columns)
    elif box == 'Object Columns':
        st.write(data.select_dtypes(include='object').columns)
    elif box == 'Numerical Columns':
        st.write(data.select_dtypes(include='number').columns)
    elif box == 'Duplicate':
        st.write(data[data.duplicated()])
#Data Preparing 
elif choice=="Data Preparing":
    st.title("Data Preparing")
    data=pd.read_csv('Data_auto.csv', index_col=None)
    drop = st.selectbox('Do You Want To Drop Any Feature ?',['','YES','NO'])
    if drop == 'YES':
        column= st.multiselect('Please Select Columns Went To Drop', data.columns)
        if column:
            data = data.drop(column, axis=1)
            st.success('Columns dropped successfully.')
    target = st.selectbox('Choose Your Target',data.columns)
    t=open('target.txt',"w")
    t.write(target)
    t.close()
    fill_c = st.selectbox('How would You Like To Handle Your Missing Categorical Data?',
                                        ['', 'Most Frequent', 'Additional Class'])
    if fill_c == 'Most Frequent':
        c_fill=st.selectbox('Choose Your Method',[' ','mode','ffill','bfill'])
        col=data.select_dtypes(include='number').columns
        col=data[data[col].isna()].columns
        if c_fill==' ':
            pass
        else:
            data=c_missing(data,col,c_fill)
    elif fill_c == 'Additional Class':
        user_input = st.text_input("Enter Your Class:")
        fill=st.selectbox(f'To You Went Fill {user_input}',[' ','YES','NO'])
        if fill=='YES':
            data.fillna(user_input,inplace=True)
            st.success('Columns Handel successfully.')
    fill_n = st.selectbox('How would You Like To Handle Your Missing Numerical Data?',
                                        ['', 'Most Frequent', 'Additional Class'])
    if fill_n == 'Most Frequent':
        n_fill=st.selectbox('Choose Your Method',[' ','mean','median','ffill','bfill'])
        col = data.select_dtypes(include=['object', 'bool']).columns
        col=data[data[col].isna()].columns
        if n_fill==' ':
            pass
        else:
            data=c_missing(data,col,n_fill)
    elif fill_n == 'Additional Class':
        user_input = st.number_input("Enter Your Number:")
        fill=st.selectbox(f'To You Went Fill {user_input}',[' ','YES','NO'])
        if fill=='YES':
            data.fillna(user_input,inplace=True)
            st.success('Columns Handel successfully.')
    data.to_csv("Data_auto.csv",index=None)
#EDA
elif choice=='EDA':
    st.title("Data EDA")
    data=pd.read_csv('Data_auto.csv', index_col=None)
    eda_option = st.selectbox('Do You Want EDA?',['','numerical_visualization_hist','numerical_visualization_box','numerical_visualization_violin'
                                            ,'categorical_visualization_bar','categorical_visualization_pie','heatmap_for_numerical'])
    eda = EDA()
    
    if eda_option == 'numerical_visualization_hist':
        eda.numerical_visualization_hist(data)
        st.pyplot()
    
    elif eda_option == 'numerical_visualization_box':
        eda.numerical_visualization_box(data)
        st.pyplot()
    
    elif eda_option == 'numerical_visualization_violin':
        eda.numerical_visualization_violin(data)
        st.pyplot()
    
    elif eda_option == 'categorical_visualization_bar':
        eda.categorical_visualization_bar(data)
        st.pyplot()
    
    elif eda_option == 'categorical_visualization_pie':
        eda.categorical_visualization_pie(data)
        st.pyplot()
    
    elif eda_option == 'heatmap_for_numerical':
        correlation_matrix = eda.heatmap_for_numerical(data)
        st.pyplot()
    
    elif eda_option == 'pair_plot':
        eda.pair_plot(data)
        st.pyplot()
    
    elif eda_option == 'correlation_heatmap':
        eda.correlation_heatmap(data)
        st.pyplot()


#Model
elif choice=="Model":
    data=pd.read_csv('Data_auto.csv', index_col=None)
    t=open('target.txt')
    target=t.readline()
    print(target)
    if data[target].dtypes in ['object','bool'] or len(pd.unique(data[target])) <= 10:
        st.title('This Is A Classification Problem')
        from pycaret.classification import *
        option = st.selectbox("Choose An Your Method:", ['',"Auto Modeling", "Choose Specific Model"])
        if option=='Auto Modeling':
            setup(data, target=target)
            setup_df = pull()
            st.info("This is the ML experiment settings")
            st.dataframe(setup_df)
            best_model = compare_models()
            compare_df = pull()
            st.info("This is your ML model")
            st.dataframe(compare_df)
            save_model(best_model, 'best_model')
            with open('best_model.pkl', 'rb') as model_file:
                st.download_button('Download the model', model_file, 'best_model.pkl')
        else:
            setup(data, target=target)
            setup_df = pull()
            st.info("This is the ML experiment settings")
            st.dataframe(setup_df)
            model = models().index.tolist()
            model_choose = st.selectbox("Choose Model:", model)
            model = create_model(model_choose)
            compare_df = pull()
            st.info("This is your model scores")
            st.dataframe(compare_df)
    else:
        st.title('This Is A Regression Problem')
        from pycaret.regression import *
        option = st.selectbox("Choose An Your Method:", ['',"Auto Modeling", "Choose Specific Model"])
        if option=='Auto Modeling':
            setup(data, target=target)
            setup_df = pull()
            st.info("This is the ML experiment settings")
            st.dataframe(setup_df)
            best_model = compare_models()
            compare_df = pull()
            st.info("This is your ML model")
            st.dataframe(compare_df)
            save_model(best_model, 'best_model')
            with open('best_model.pkl', 'rb') as model_file:
                st.download_button('Download the model', model_file, 'best_model.pkl')
        else:
            setup(data, target=target)
            setup_df = pull()
            st.info("This is the ML experiment settings")
            st.dataframe(setup_df)
            model = models().index.tolist()
            model_choose = st.selectbox("Choose Model:", model)
            model = create_model(model_choose)
            compare_df = pull()
            st.info("This is your model scores")
            st.dataframe(compare_df)   


