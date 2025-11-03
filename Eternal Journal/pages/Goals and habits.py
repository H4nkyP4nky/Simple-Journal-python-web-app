import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

if os.path.exists('habits.csv'):
    hab_df = pd.read_csv('habits.csv')
else:
    hab_df = pd.DataFrame({
    'Date': pd.Series(dtype='datetime64[ns]'),
    'Water': pd.Series(dtype='float'),
    'Steps': pd.Series(dtype='int'),
    'Kcal': pd.Series(dtype='float'),
    'Sleep': pd.Series(dtype='float')
})
    hab_df.to_csv('habits.csv', index=False)

if 'step' not in st.session_state:
    st.session_state.step = 1

def go_step_1():
    st.session_state.step = 1

def go_step_2():
    st.session_state.step = 2

st.title("Your habits")
if st.session_state.step == 1:
    st.write("Let's fill your acomplishments of the day!")
    with st.form(key='hab_form'):
        date = st.date_input("Pick a day", max_value='today')
        water = st.slider("Water drank [l]:", min_value=0.0, max_value=6.0, step=0.25)
        steps = st.slider("Steps made:", min_value=0, max_value=50000, step=100)
        kcal = st.number_input("Kcal intake:",icon=':material/bakery_dining:')
        sleep = st.slider("Hours slept:", min_value=0.0, max_value=12.0, step=0.5)

        submit_button = st.form_submit_button(label="Save")

    if submit_button:
            hab_df['Date'] = pd.to_datetime(hab_df['Date']).dt.date

            if date in hab_df["Date"].values:
                st.warning("You already put in this day to the Journal")
            else:
                hab_df.loc[len(hab_df)] = [date, water, steps, kcal, sleep]
                hab_df = hab_df.sort_values('Date')
                hab_df.to_csv('habits.csv', index=False)
                st.write(f"**Data saved successfully!**")
    
    with st.form(key='delete_form'):
        st.write('Do you want to delete your whole journal information?')
        delete_button = st.form_submit_button("Delete")
        if delete_button:
            hab_df = pd.DataFrame({
            'Date': pd.Series(dtype='datetime64[ns]'),
            'Water': pd.Series(dtype='float'),
            'Steps': pd.Series(dtype='int'),
            'Kcal': pd.Series(dtype='float'),
            'Sleep': pd.Series(dtype='float')
        })
        hab_df.to_csv('habits.csv', index=False)
    
    next_button = st.button("Next", on_click=go_step_2)


elif st.session_state.step == 2:
    st.subheader("Visualizations of your progress")

    if not hab_df.empty:
        hab_df['Date'] = pd.to_datetime(hab_df['Date'])
        all_dates = pd.date_range(start=hab_df['Date'].min(), end=hab_df['Date'].max())

        hab_df_full = hab_df.set_index('Date').reindex(all_dates)
        hab_df_full = hab_df_full.reset_index()
        hab_df_full = hab_df_full.rename(columns={'index': 'Date'})

        fig = px.line(
            hab_df_full,
            x='Date',
            y='Water',
            labels={'Water': 'Liters of water drank', 'Date': 'Date'},
            color_discrete_sequence=['#66b4d9'],
            markers=True,
            title='Your water intake'
        ).update_traces(line=dict(width=10))

        fig.update_layout(
            title={
                'text': "Your water intake",
                'x': 0.55,
                'xanchor': 'center'
            }
        )

        fig.add_hline(
            y=round(hab_df['Water'].mean(), 2),
            line_dash="dash",      
            line_color="#590f29",
            annotation_text='',
            annotation_position="top right"
        )
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
        col1, col2 = st.columns([1,2])
        with col1:
            st.metric(label="Average water intake (in Liters)", value=round(hab_df['Water'].mean(), 2))
        with col2:
            if round(hab_df['Water'].mean(), 2) > 2:
                st.write("Good water intake! Congratulations!")
            else:
                st.write("You should drink more water!")

        fig_steps = px.line(
            hab_df_full,
            x='Date',
            y='Steps',
            labels={'Steps': 'Number of steps', 'Date': 'Date'},
            color_discrete_sequence=['#577866'],
            markers=True,
            title='Your amount of steps'
        ).update_traces(line=dict(width=10))

        fig_steps.update_layout(
            title={
                'text': 'Your amount of steps',
                'x': 0.55,
                'xanchor': 'center'
            }
        )

        fig_steps.add_hline(
            y=round(hab_df['Steps'].mean(), 2),
            line_dash="dash",      
            line_color="#590f29",
            annotation_text='',
            annotation_position="top right"
        )

        st.plotly_chart(fig_steps, use_container_width=True, config={'staticPlot': True})

        col1s, col2s = st.columns([1,2])
        with col1s:
            st.metric(label="Average amount of steps", value=round(hab_df['Steps'].mean(), 2))
        with col2s:
            if round(hab_df['Steps'].mean(), 2) > 10000:
                st.write("Good ammount of steps! Keep it up!")
            else:
                st.write("You should walk more!")

        fig_kcal = px.line(
            hab_df_full,
            x='Date',
            y='Kcal',
            labels={'Kcal': 'Kcal consumed', 'Date': 'Date'},
            color_discrete_sequence=['#2f0c4f'],
            markers=True,
            title='Your Kcal intake'
        ).update_traces(line=dict(width=10))

        fig_kcal.add_hline(
            y=round(hab_df['Kcal'].mean(), 2),
            line_dash="dash",      
            line_color="#590f29",
            annotation_text='',
            annotation_position="top right"
        )

        fig_kcal.update_layout(
            title={
                'text': 'Your calorie intake',
                'x': 0.55,
                'xanchor': 'center'
            }
        )

        st.plotly_chart(fig_kcal, use_container_width=True, config={'staticPlot': True})
        st.metric(label="Average calorie intake", value=round(hab_df['Kcal'].mean(), 2))

        fig_sleep = px.line(
            hab_df_full,
            x='Date',
            y='Sleep',
            labels={'Sleep': 'Hours of sleep', 'Date': 'Date'},
            color_discrete_sequence=['#4b4d4c'],
            markers=True,
            title='Your sleep time'
        ).update_traces(line=dict(width=10))

        fig_sleep.update_layout(
            title={
                'text': 'Your sleeping time',
                'x': 0.55,
                'xanchor': 'center'
            }
        )

        fig_sleep.add_hline(
            y=round(hab_df['Sleep'].mean(), 2),
            line_dash="dash",      
            line_color="#590f29",
            annotation_text='',
            annotation_position="top right"
        )

        st.plotly_chart(fig_sleep, use_container_width=True, config={'staticPlot': True})
        col1sl, col2sl = st.columns([1,2])
        with col1sl:
            st.metric(label="Average time of sleep", value=round(hab_df['Sleep'].mean(), 2))
        with col2sl:
            if round(hab_df['Sleep'].mean(), 2) > 8:
                st.write("Good ammount of sleep! You are rested well!")
            else:
                st.write("You should sleep more!")

    else:
        st.write("No data to show yet.")


    back_button = st.button("Back", on_click=go_step_1)
    
