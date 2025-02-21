import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(URL, dtype={'Quarter': str,
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})
st.title("Populația Canadei")
st.markdown("Tabelul sursă poate fi găsit [aici](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")
with st.expander("Vezi tabelul complet cu date"):
    st.write(df)
with st.form("population-form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Alege o dată de început")
        start_quarter = st.selectbox("Trimestru", options=["Q1", "Q2", "Q3", "Q4"], index=2, key="start_q")
        start_year = st.slider("Anul", min_value=1991, max_value=2023, value=1991, step=1, key="start_y")
    with col2:
        st.write("Alege o dată de sfârșit")
        end_quarter = st.selectbox("Trimestru", options=["Q1", "Q2", "Q3", "Q4"], index=0, key="end_q")
        end_year = st.slider("Anul", min_value=1991, max_value=2023, value=2023, step=1, key="end_y")
       
    with col3:
        st.write("Alege o locație")
        target = st.selectbox("Alege o locație", options=df.columns[1:], index=0)
    submit_btn = st.form_submit_button("Analizează")
    
start_date = f"{start_quarter} {start_year}"
end_date = f"{end_quarter} {end_year}"

def format_date_for_comparison(date):
    quarter, year = date.split()  # Separă "Q1 2024" în ["Q1", "2024"]
    year = float(year)  # Convertim anul în float
    quarter_number = int(quarter[1])  # Extragem numărul trimestrului (ex. "1" din "Q1")
    # Adăugăm o valoare fracționară pentru a diferenția trimestrele
    if quarter_number == 1:
        return year
    elif quarter_number == 2:
        return year + 0.25
    elif quarter_number == 3:
        return year + 0.50
    elif quarter_number == 4:
        return year + 0.75
def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

def format_number(value):
    """ Formatează numerele cu puncte pentru mii și milioane. """
    return "{:,.0f}".format(value).replace(",", ".")


def display_dashboard(start_date, end_date, target):
    tab1, tab2 = st.tabs(["Evoluția populației", "Compară"])
   
    with tab1:
        st.subheader(f"Evoluția populației din {start_date} până în {end_date}")

        col1, col2 = st.columns(2)
       
        with col1:
            initial = df.loc[df['Quarter'] == start_date, target].item()
            final = df.loc[df['Quarter'] == end_date, target].item()
            percentage_diff = round((final - initial) / initial * 100, 2)
            delta = f"{percentage_diff}%"
                # Formatăm numerele pentru afișare
            initial_formatted = format_number(initial)
            final_formatted = format_number(final)
             # Afișare metrici în Streamlit
            st.metric(start_date, value=initial_formatted)
            st.metric(end_date, value=final_formatted, delta=delta)
       
        with col2:
            start_idx = df.loc[df['Quarter'] == start_date].index.item()
            end_idx = df.loc[df['Quarter'] == end_date].index.item()
            filtered_df = df.iloc[start_idx: end_idx+1]
            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel('Timp')
            ax.set_ylabel('Populație')
            ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)
    with tab2:
        st.subheader('Compară cu alte locații')
        all_targets = st.multiselect("Alege alte locații", options=filtered_df.columns[1:], default=[target])
       
        fig, ax = plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel('Timp')
        ax.set_ylabel('Populație')
        ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
        fig.autofmt_xdate()
        st.pyplot(fig)

if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].tolist():
    st.error("Nu există date disponibile. Verifică selecția trimestrului și anului.")
elif end_before_start(start_date, end_date):
    st.error("Datele nu sunt valide. Data de început trebuie să fie înainte de data de sfârșit.")
else:
    display_dashboard(start_date, end_date, target)
