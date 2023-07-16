import streamlit as st

st.markdown('**Delta** is the planned diffence in time between this rental and the previous one')

st.markdown('**Returned Early** are the rentals that were returned ahead of time "negative delay values"')
st.markdown('**Problematic** are cases where the car was returned after the agreed time and exceeded the \
            delta between two consecutive rentals. This is harmful for the next client')
st.markdown('**Problematic Solved** the proposed thresholds solves this problematic rental')
st.markdown('**Problematic UnSolved** the proposed threshold soes not solve this problematic rental')
st.markdown('**Non Problematic** The delta between reservations is greater than the delay that happened')
st.markdown('**Non Problematic Affected** the proposed threshold affects this rental by pushing and delaying it')
st.markdown('**No Problematic Not affect** the proposed threshold did not delay this reservation')