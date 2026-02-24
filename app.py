import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="EduTrack PRO", layout="wide")

# ---------- BASE ----------
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

# ---------- DIMENSIONES ----------
DIMENSIONES = {
"Atencion": ["att1","att2","att3"],
"Compromiso": ["part1","part2","mot1","mot2"],
"Comunicacion": ["com1","com2"],
"Socioafectivo": ["soc1","soc2","ani1"],
"Autorregulacion": ["ani2","ani3","comp1"]
}

ITEMS_NEGATIVOS = ["att2","ani2","ani3","comp1"]

# ---------- SCORING ----------
def puntuar(resp,neg=False):
    if not neg:
        return {"SI":2,"A VECES":1,"NO":0}[resp]
    else:
        return {"SI":0,"A VECES":1,"NO":2}[resp]

def calcular_dim(row):
    scores={}
    for dim,items in DIMENSIONES.items():
        s=0
        for it in items:
            neg=it in ITEMS_NEGATIVOS
            s+=puntuar(row[it],neg)
        scores[dim]=s
    return scores

# ---------- PREGUNTAS ----------
def pregunta(key,texto):
    return st.radio(texto,
    ["SI","A VECES","NO"],
    key=key,
    horizontal=True)

# ---------- MENU ----------
menu = st.sidebar.selectbox(
"Menu",
["Registro Diario","Score Semanal",
"Comparación 2 Semanas","Score Mensual"])

# ---------- REGISTRO ----------
if menu=="Registro Diario":

    fecha = st.date_input("Fecha",datetime.now())
    alumno = st.selectbox("Alumno",
    [f"Alumno {i}" for i in range(1,21)])

    att1=pregunta("att1","¿Mantuvo la atención?")
    att2=pregunta("att2","¿Se distrajo?")
    att3=pregunta("att3","¿Cambio tareas?")

    part1=pregunta("part1","¿Participó?")
    part2=pregunta("part2","¿Preguntó?")

    com1=pregunta("com1","¿Expresión clara?")
    com2=pregunta("com2","¿Comunicación efectiva?")

    mot1=pregunta("mot1","¿Motivación?")
    mot2=pregunta("mot2","¿Actitud positiva?")

    soc1=pregunta("soc1","¿Relación positiva?")
    soc2=pregunta("soc2","¿Habilidades sociales?")

    ani1=pregunta("ani1","¿Expresión positiva?")
    ani2=pregunta("ani2","¿Cansancio?")
    ani3=pregunta("ani3","¿Cambios ánimo?")

    comp1=pregunta("comp1","¿Conducta disruptiva?")

    if st.button("Guardar"):

        registro={
        "Fecha":fecha,
        "Alumno":alumno,
        "att1":att1,"att2":att2,"att3":att3,
        "part1":part1,"part2":part2,
        "com1":com1,"com2":com2,
        "mot1":mot1,"mot2":mot2,
        "soc1":soc1,"soc2":soc2,
        "ani1":ani1,"ani2":ani2,"ani3":ani3,
        "comp1":comp1
        }

        st.session_state.data=pd.concat(
        [st.session_state.data,
        pd.DataFrame([registro])],
        ignore_index=True)

        st.success("Guardado")

# ---------- SEMANAL ----------
elif menu=="Score Semanal":

    df=st.session_state.data
    if df.empty:
        st.warning("Sin datos")
    else:
        df["Fecha"]=pd.to_datetime(df["Fecha"])
        df["Semana"]=df["Fecha"].dt.isocalendar().week

        weekly=[]

        for i,row in df.iterrows():
            sc=calcular_dim(row)
            sc["Semana"]=row["Semana"]
            weekly.append(sc)

        wdf=pd.DataFrame(weekly)
        prom=wdf.groupby("Semana").mean()

        st.line_chart(prom)

# ---------- 2 SEMANAS ----------
elif menu=="Comparación 2 Semanas":

    df=st.session_state.data
    if df.empty:
        st.warning("Sin datos")
    else:
        df["Fecha"]=pd.to_datetime(df["Fecha"])
        df["Semana"]=df["Fecha"].dt.isocalendar().week
        df["BiSem"]=df["Semana"]//2

        bi=[]

        for i,row in df.iterrows():
            sc=calcular_dim(row)
            sc["BiSem"]=row["BiSem"]
            bi.append(sc)

        bdf=pd.DataFrame(bi)
        prom=bdf.groupby("BiSem").mean()

        st.bar_chart(prom)

# ---------- MENSUAL ----------
elif menu=="Score Mensual":

    df=st.session_state.data
    if df.empty:
        st.warning("Sin datos")
    else:
        df["Fecha"]=pd.to_datetime(df["Fecha"])
        df["Mes"]=df["Fecha"].dt.month

        mes=[]

        for i,row in df.iterrows():
            sc=calcular_dim(row)
            sc["Mes"]=row["Mes"]
            mes.append(sc)

        mdf=pd.DataFrame(mes)
        prom=mdf.groupby("Mes").mean()

        st.bar_chart(prom)
