import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas_gbq

# Título do aplicativo
st.title("📊 Análise de Dados com Pandas + Streamlit")
# Carregar dataset
@st.cache_data
def carregar_dados(name):
   return pd.read_csv(name)
df = carregar_dados("insurance.csv")

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)
res=client.query("SELECT * FROM streamlit-473312.MVP.Users" )
rows=res.result()
resp=[dict(row) for row in rows]
for row in resp:
    st.write("✍️ " + row['Nome'])


    #df_2 = pd.read_gbq("SELECT * FROM streamlit-473312.MVP.Users" , dialect="standard") 
# Mostrar dados
st.subheader("🔍 Visualização da Tabela de Dados")
st.dataframe(df)
# Filtros interativos
st.sidebar.header("🔧 Filtros")
sexo = st.sidebar.multiselect("Sexo", options=df['sex'].unique(),
default=df['sex'].unique())
fumante = st.sidebar.selectbox("É fumante?",
options=df['smoker'].unique())
# Aplicar filtros
df_filtrado = df[(df['sex'].isin(sexo)) & (df['smoker'] == fumante)]
st.subheader("📌 Dados Filtrados")
st.dataframe(df_filtrado)

# Estatísticas
st.subheader("📈 Estatísticas Descritivas")
st.write(df_filtrado.describe())
# Gráfico 1: Dispersão
st.subheader("💸 Relação entre Total da Conta e Idade")
st.scatter_chart(
df_filtrado,
x="age",
y="charges",
color="bmi",
size="children",
)
# Gráfico 2: Bar
st.subheader("📦 Distribuição Custo x Idade")
st.bar_chart(
df_filtrado,
x="age",
y="charges",
color="smoker"
)
# Gráfico 3: Boxplot
st.subheader("📦Boxplot Custo x Idade")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df_filtrado, x="age", y="charges", ax=ax2)
st.pyplot(fig2)
st.header("Dados da Base SQL")
# Create API client.
#credentials_1 = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)

credentials = service_account.Credentials.from_service_account_file(
    '.streamlit/streamlit-473312-d5a1638cf6a2.json')

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "streamlit-473312"

client = bigquery.Client(credentials=credentials)
res=client.query("SELECT * FROM streamlit-473312.MVP.Users" )
rows=res.result()
resp=[dict(row) for row in rows]
df_2=pd.DataFrame(resp)
#for row in resp:
    #st.write("✍️ " + row['Nome'])
    #st.write(" " + row['Funcao'])


#sql = "SELECT * FROM MVP.Users"
#df_2 = pandas_gbq.read_gbq(sql)
st.dataframe(df_2)