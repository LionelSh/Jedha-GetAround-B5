import streamlit as st

st.markdown('# Executive Summary')



st.markdown('## The percentage of real problematic cases')
st.markdown('As per the funnel chart below: ')
st.markdown('- The percentage of problematic cases which really suffered from \
            the delay represent around 6% out of all the delay cases.')
st.markdown("- If we did not exclude the outliers this percentage would have been 12% because of extraordinary delay values")
st.markdown(' Compared to whole dataset of rentals that would be only 1% of the complete rentals \
            that took place in the dataset')


with st.expander("See details"):
    st.write('hjkhdkjashk')

st.divider()


st.markdown('## The type of check_in "mobile" vs "connect"')

st.markdown('It is true that the number of "mobile" check_in types are greater than the \
            "connect" type. _But_, **both types showed the same behaviour when plotting \
            the histogram**. Meaning that the delay behaviour for both was almost the same \
            i.e. no signifcant difference')
st.markdown('for example:at the first 5 minutes delay the percentage of mobile check_in type \
            was 9% where as for connect is was 9.6 ')
st.markdown('there was no decisive difference except after the miunte 90 where the mobile type \
            score higher percentage of smaples, eventhough they both remained at too low percentages \
            after that time')

st.markdown('## The Recommended Threshold"')

st.markdown('if the management wishes to solve all the possible delays, no matter what, \
            choosing a threshold of 65 minutes covers all the delay cases based on \
            the available statistics, **but at the cost of affecting 17 of the rental cases \
            with an average loss of 24 minutes per rental** "kindly refer to the laboratory" ')

st.markdown('- to solve above 80% of the delay problems a threshold of 45 miuntes would do it\
             with affecting only 7% of the non problematic cases')

st.markdown('in the end it is the management choice but here the objective of illustrating,\
            the various possibilities and impact has been fulfilled')
