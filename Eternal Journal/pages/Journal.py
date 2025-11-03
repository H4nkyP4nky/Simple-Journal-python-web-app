import streamlit as st
import os
import pandas as pd

if os.path.exists('journal.csv'):
    jour_df = pd.read_csv('journal.csv')
else:
    jour_df = pd.DataFrame({
    'Date': pd.Series(dtype='datetime64[ns]'),
    'Note': pd.Series(dtype='string')
})
    jour_df.to_csv('journal.csv', index=False)

st.title('Your journal notes')

with st.form(key='journ_form'):
    date = st.date_input(label='Pick the date of your entry', max_value='today')
    long_text = st.text_area(label='Your thougts of the day',height=250)

    jbutton = st.form_submit_button("Save the entry")
    if jbutton:
        jour_df['Date'] = pd.to_datetime(jour_df['Date']).dt.date

        jour_df.loc[len(jour_df)] = [date, long_text]
        jour_df = jour_df.sort_values('Date', ascending=False)
        jour_df.to_csv('journal.csv', index=False)
        st.write(f"**Note saved successfully!**")

journal_dict = dict(zip(jour_df['Date'], jour_df['Note']))
print(journal_dict)

for key, value in journal_dict.items():
    st.write(f'{key}:')
    st.write(f'{value}')
    st.divider()