import streamlit as st
import pandas as pd
import os

if os.path.exists('info.csv'):
    info_df = pd.read_csv('info.csv')
else:
    pd.DataFrame({
    'Date': pd.Series(dtype='datetime64[ns]'),
    'Water': pd.Series(dtype='float'),
    'Steps': pd.Series(dtype='int'),
    'Kcal': pd.Series(dtype='int'),
    'Sleep': pd.Series(dtype='float')
})
    info_df.to_csv('info.csv', index=False)

st.title('Personal Information')

if pd.notna(info_df.loc[0, 'Name']) and info_df.loc[0, 'Name'].strip() != '':
    st.write(f"Hi {info_df.loc[0, 'Name']}! Nice to see you!")
else:
    st.write("Hi! Let's fill some basic information about you!")


def Write_info():
    info_df.to_csv('info.csv', index=False)

if pd.notna(info_df.loc[0, 'Name']) and info_df.loc[0, 'Name'].strip() != '':
    st.write(f"Your Name: {info_df.loc[0, 'Name']}")
    st.write(f"Your Age: {info_df.loc[0, 'Age']}")


with st.form(key='info_form'):
    name = st.text_input('Your name:', value=info_df.loc[0, 'Name'])
    age = st.number_input('Your age:', value=0 if pd.isna(info_df.loc[0, 'Age']) else int(info_df.loc[0, 'Age']), step=1)
    submit_button = st.form_submit_button(label="Save")

    if submit_button:
        info_df.loc[0, 'Name'] = name
        info_df.loc[0, 'Age'] = age
        Write_info()

