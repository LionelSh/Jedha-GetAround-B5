import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# STAGES OF WORK
# A). General statistics, display in general:
#     1. The delay distribution in general
#     2. The delta distribution in general
#     3. the contribution of the check_in type in the delay 
#    **charts used , histogram " normal, percent & commulative"

# B). Treat the data
#     1. Relate each rental with the delay of the previous rental
#     2. Relate each rental with the delta time planned to be between the current rental and previous
#     3. Display the impact for each threshold "interval 5 minutes"

# C). Executive summary for the management


#################################################################################################
##########                                                                              #########
##########                    Website contents and layouts                              #########
##########                                                                              #########
#################################################################################################
####### Page Config #########

st.set_page_config(
    page_title="Getaround Analysis",
    page_icon="🧊",
    #layout="wide",
    initial_sidebar_state="expanded",    
)
#######   Side bar ###########



#######   Main page ##########

progress_bar = st.progress(0, text="Operation in progress. Please wait.")

st.title('Getaround Case study')

st.subheader('The Objective')
st.markdown('Is to facilitate the study of finding the optimum setting for a **safety margin threshold** to prevent the collision between the upcoming reservation and the previous one due to _**:blue[check_in delay]**_')
st.subheader('Approach')
st.markdown('First we will start with General Statistics to view the delay and delta distribution, \
             then we will link each rental with the delay resulted from the previous rental and planned \
            delta time between them. Finally, we will introduce the laboratory where we can investigate \
            the impact of each threshold we choose ')

    

#################################################################################################
##########                                                                              #########
##########                    Loading the Data & Preparations                           #########
##########                                                                              #########
#################################################################################################




######   FUNCTION TO LOAD THE DATA  #############################

@st.cache_data          # st.cache is depricated use st.cache_data instead this is useful to prevent 
                        # re-executing loading the data each time, consequently it is cached
                        # it will only re-execute the loading if an input parameter of the function changed :)
                        # Note : in case of database connections and ML models like in the second project
                        # we will use the instruction st.cache_resource instead
def load_data():
   
   data_load_state = st.text('Loading data...')
   df = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx")
   data_load_state.text('Data loaded successfully..')

   return df 

progress_bar.progress(0, text='Downloading the data')
df = load_data()  # Load the data
count_1_total = df.shape[0] # saving the number of total records for executive summary
progress_bar.progress(5 , text='Generating General Analysis')

# we will use the technique of maintaining the data frame in the session state
# to be used by other pages when browsing, instead of downloading the data from the file each time

if 'my_data' not in st.session_state:
    st.session_state['my_data'] = df
    



#################################################################################################
##########                                                                              #########
##########                         A) GENERAL ANALYSIS                                  #########
##########                                                                              #########
#################################################################################################


                        ####### A.1 ) General delay distribution  #######

st.header('A) General Overview & Statistics')

st.subheader('1. How is the delay distribution?')

# We shall start with general analysis
# we filter the delays greater than 0
mask = df['delay_at_checkout_in_minutes'] >= 0
df_general = df.loc[mask,:].copy()
count_2_exclude_negative_delay = df_general.shape[0]

# Layout and organizing the outputs
# use the tabs to illustrate numbers and percentage
tab_numbers, tab_percentages = st.tabs(["Numbers", "Percentages"])

with tab_numbers:
   # plotly figure of type histogram
   fig = px.histogram(df_general, x="delay_at_checkout_in_minutes", range_x = [0,200])
   # BINNING: we chose the bining width equals to 5 meaning 5 minutes
   fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5      # binning width
        ))
   st.plotly_chart(fig)
   
   # storing number of rows after filtering the positive delays
   no_of_rows_after_delay_positive = df_general.shape[0]

with tab_percentages:

    fig = px.histogram(df_general, x="delay_at_checkout_in_minutes", range_x = [0,200],histnorm="percent")
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5
        ))
    st.plotly_chart(fig)
    st.caption("Each bin 'bar'resembles 5 minutes ")

# writing the delay general stats

col1,col2,col3,col4 = st.columns(4)

col1.metric('min',df_general['delay_at_checkout_in_minutes'].min())
col2.metric('median',int(df_general['delay_at_checkout_in_minutes'].median()))
col3.metric('mean',str(round(df_general['delay_at_checkout_in_minutes'].mean(),2)))
col4.metric('max',int(df_general['delay_at_checkout_in_minutes'].max()))

median_delay = df_general['delay_at_checkout_in_minutes'].mean()

st.markdown("Apparently there are **outliers** values, the maximum delay is greater than 11 hours!! \
            We shall use the following rule to exclue them, the max value in the range will include \
            1.5 times the median, we shall do that in the upcomming analysis.")

st.divider()  


                        ####### A.2) Delay distribution per Type  #######

st.subheader('2. The delay distribution per "check_in" type')

# organizing the results in tabs
tab_numbers, tab_percentages = st.tabs(["Numbers", "percentage"])  

with tab_numbers:        

    # to display the check in type within the histogram we used the color = checkin_type
    fig = px.histogram(df_general, x="delay_at_checkout_in_minutes", range_x = [0,200],  color='checkin_type')
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5      # bins five minutes
        ))
    st.plotly_chart(fig)

    st.markdown("**OBSERVATION :** It can be noticed easily that the check_in type **'mobile'** plays a big role in \
                producing the majority of the delay cases, unlike the check_in type **'connect'** \
                which has a negligable impact.")


with tab_percentages:
    # to display the check in type within the histogram we used the color = checkin_type
    fig = px.histogram(df_general, x="delay_at_checkout_in_minutes", range_x = [0,200],  color='checkin_type', histnorm='percent')
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5
        ))
    st.plotly_chart(fig)
    st.markdown(" **Important Note :**")
    st.markdown("Here, the percentages of each bin or 'bar'represent the percentage of the series \
                itself and **NOT** the total samples, example the first bar (0 to 4) miuntes are 10 percent of the \
                connect series ONLY and not the 'connect + mobile' combined.")
    

    st.caption("There were some cases where the car was returned earlier but had been filtered out \
            to focus on the delay ")
    

st.divider()

                        ####### A.3) Delta distribution   #######

st.subheader('3. What about the DELTA distribution?')

st.markdown('The delta is the planned difference in time between the bookings ')

# similar to the steps above except that here we display the delta instead of delay

fig = px.histogram(df_general, x="time_delta_with_previous_rental_in_minutes", range_x = [0,200])
fig.update_traces(xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5
    ))
st.plotly_chart(fig)

st.markdown("- **Another observation** Notice how the delta is **distributed evenly** in an integer around \
            30 minutes, i.e. 30 mins, 1 hour, 1.5 hour, 2hours, etc..,\
            this could be useful to solve the problem, we'll see how..  ")
st.markdown("- Also here we can see that there are outliers that need to be clipped out")

# displaying the general stats of the delta
col1,col2,col3,col4 = st.columns(4)

col1.metric('min',df_general['time_delta_with_previous_rental_in_minutes'].min())
col2.metric('median',int(df_general['time_delta_with_previous_rental_in_minutes'].median()))
mean_delta = str(round(df_general['time_delta_with_previous_rental_in_minutes'].mean(),2))
col3.metric('mean',mean_delta)
col4.metric('max',int(df_general['time_delta_with_previous_rental_in_minutes'].max()))

median_delta = df_general['time_delta_with_previous_rental_in_minutes'].median()

st.divider()


                             ####### A.4) Overlapping Delta and delay   #######

st.subheader("4. Let's overlap them")

# to implement the overlap we use the add.trace technique in go figure plotly as follows:
fig = go.Figure(layout_title_text="Histogram Delay vs. Delta distribution")
fig.add_trace(go.Histogram(x=df_general['delay_at_checkout_in_minutes'],xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5
    ), name='Check out Delay'))
fig.add_trace(go.Histogram(x=df_general['time_delta_with_previous_rental_in_minutes'],xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5), name='Delta difference between bookings', marker =dict(color='red')))

# Overlay both histograms
fig.update_layout(barmode='overlay',xaxis_title='Duration (minutes)', yaxis_title='Counts')
fig.update_xaxes(range=[0, 200])

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)
st.divider()



                             ####### A.5) Commulative Chart   #######

st.subheader("5. Commulative")

# overlap chart using add_trace and go.figure as below 
# IMPORTANT !! OF COURSE THE histnorm = percent to obtain percentage and valid comaprison
fig = go.Figure(layout_title_text="Histogram Delay vs. Delta distribution")
fig.add_trace(go.Histogram(x=df_general['delay_at_checkout_in_minutes'],
                           xbins=dict( # bins used for histogram
                                    start=0.0,
                                    end=200.0,
                                    size=5
                                ), 
    name='Check out Delay', 
    cumulative_enabled=True,   # cummulative enabled
    histnorm = "percent"))     # histnorm = percent to obtain percentage of samples 

fig.add_trace(go.Histogram(x=df_general['time_delta_with_previous_rental_in_minutes'],
                           xbins=dict( # bins used for histogram
                               start=0.0,
                               end=200.0,
                               size=5
                               ),
    name='Delta difference between bookings',
    cumulative_enabled=True,
    histnorm ="percent"))

# Overlay both histograms
fig.update_layout(barmode='overlay',xaxis_title='Duration (minutes)', yaxis_title='Counts')
fig.update_xaxes(range=[0, 200])

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)

st.plotly_chart(fig)

st.markdown(" ###### Comparing the two plots together, take an example, if we choose \
             at 59 minutes is equivalent to around 60% of the delay samples and around 40% of the deltas \
            that were below 59 miuntes. But.. should we take the general distribution \
            as simple as that or try to find what really happened on ground, linking each \
            rental with the rentals that took place before it, let's have a look at the second \
                part of the analysis 'on ground analysis' ")
st.divider()




#################################################################################################
##########                                                                              #########
##########                            B) ON GROUND ANALYSIS                             #########
##########                                                                              #########
#################################################################################################


### layout

st.header('B) On the ground')

st.markdown("The previous analysis took the overall values in general, but actually, on the ground \
            the situation might differ because each rental case is related to to the delay of the previous \
            case, and is related to the delta time between them.")

st.markdown("Consequntly, we will re-organize the dataset linking each rental\
            with the delta time between it and the previous rental, in addition to the actual delay of the\
            previous rental")

progress_bar.progress(20, text='Re-Organizing the Dataframe')   
####  THE Preprocessing of the data frame and the necessary preparations

######   B.1) RE-ORGANIZING THE DATASET ##################

# this is a function to extract the delay of the previous request
# in order to compare it with the planned time difference between the two requests

def get_delay_of_previous(ref_id):
    
    # first check if the ref_is is not empty i.e. 'Nan' 
    if pd.notna(ref_id):
        
        # then filter the line which contains this ref_id value

        mask = df['rental_id'] == ref_id

        # take the column of that row which contains the delay value

        previous_delay = df.loc[mask,'delay_at_checkout_in_minutes']     
        

        return previous_delay.values[0]  # the values command plays a role in extracting 
                                         # the first value that we need, otherwise we get like a series object
                                         # this is important and according to pandas
    else :
        # This means that the ref_id is empty
        return 
    
# Execute the function for all rows using apply method and calling the "get_delay_of_previous" function
# this is to obtain the delay related to that id and place it in one row to do our calculations

df['delay_of_previous'] = df['previous_ended_rental_id'].apply(get_delay_of_previous)

#################################################################################################
###########                                                                            ##########
###########     Missing values statistics                                              ##########
#################################################################################################

#(1) count the number of referenced ref_id that were not found, or if found their delay values were nan:

mask = (df['previous_ended_rental_id'].notna()) & (df['delay_of_previous'].isna())
count_missing_ref_id = df.loc[mask,:].shape[0]  # to be used in management summary


#################################################################################################
##########                                                                              #########
########## THE cases to consider in the analysis                                        #########
##########                                                                              #########
#################################################################################################



#(1) in order to implement our analysis correctly we need to extract the cases 
# which contain real values and not empty ones Nan
# note that the data to be considered are put in a copy named ds instead of df
# to prevent confusion and bugs and modifying the original df because we need it

# it is meaningless to have an empty delta or delay
mask = (df['time_delta_with_previous_rental_in_minutes'].notna()) & (df['delay_of_previous'].notna())
ds = df.loc[mask,:].copy()

count_3_after_na_deltas_delay = ds.shape[0]   # to be used in management summary


# exclude the outliers
mask = df['delay_of_previous'] > 0  # exclude the negative
df = df.loc[mask,:]

median_delay = df['delay_of_previous'].median()
outlier_delay = median_delay * 1.5 

mask = ds['delay_of_previous'] < outlier_delay
ds = ds.loc[mask,:]

count_4_after_outliers_delay = df.shape[0]


# median_delta = df['time_delta_with_previous_rental_in_minutes'].median()
# outlier_delta = median_delta * 1.5 

# mask = ds['time_delta_with_previous_rental_in_minutes'] < outlier_delta
# ds = ds.loc[mask,:]
count_5_after_outliers_delta = df.shape[0]



#################################################################################################
##########                                                                              #########
##########                 THE REAL WORK                                               #########
##########                                                                              #########
#################################################################################################
progress_bar.progress(57, text='Classifying')
# classifications
    # case (A) If There is no delay => "previous delay" is negative => delivered early
    # case (B) There is delay 
        # if delta > delay are considered non-problemetic
        # if delta < delay are considered problematic cases
    # the non problematic cases will lose money when the threshold is greater than delta otherwise no losses will occur
    # the problmeatic cases will become solved when the threshold exceeds the delay

def classifier(row):
    # check if the car was returned early case (A)

    if row['delay_of_previous'] < 0:
        return 'returned early'  
    
    # check if although late, compare with delta (B)
    else:
        if row['delta-delay'] >= 0:   # the delay was less than delta
            return 'Non_Problematic'  # consequently non problematic
        else:
            return 'Problematic'  # this means delay bigger than delta => problem

def do_preparations(proposed_threshold = 0):
    # we will add in a column for the proposed margin delay
    ds['proposed_threshold'] = proposed_threshold
    ds['threshold-delay'] = ds['proposed_threshold'] - ds['delay_of_previous']

    
    # and status to indicate if the threshold solved the delay problem or not

    # How to classify if problematic or not
    ds['delta-delay'] = ds['time_delta_with_previous_rental_in_minutes'] - ds['delay_of_previous']
    
    
    # Losses calculation, 
    # losses to calculate the miuntes of loss for the non-problmeatic cases
    # The losses happen for the positive values only of the below equation, 
    # the negative values will be discarded and filtered out  
    ds['losses'] = ds['proposed_threshold'] - ds['time_delta_with_previous_rental_in_minutes']

    return ds

# finally the status column, whether solved or not
def define_status(row):
    if row['classification'] == 'Problematic':
        if row['threshold-delay'] >= 0 :
            return 'Solved'
        else:
            return 'UnSolved'
    elif row['classification'] == 'returned early':
            return ''
    else:
        if row['losses'] <= 0 :  # this means that the delta is greateer than the threshold
            return 'Not affected'
        else:
            return 'Affected'   # because the threshold pushed the booking

# initialize the dataframe for proposed threshold = 0
ds = do_preparations(0)
ds['classification'] = ds.apply(classifier, axis=1)
ds['status'] = ds.apply(define_status, axis=1)  # the status column:

count_6_problematic_cases =  ds['classification'].value_counts()['Problematic']
count_7_non_problematic_cases = ds['classification'].value_counts()['Non_Problematic']
count_8_returned_early_cases = ds['classification'].value_counts()['returned early']

#################################################################################################
##########                                                                              #########
##########                 create a petite dataframe called OBSERVER                    #########
##########                 to illustrate all the threshold possibilities                #########
#################################################################################################

# this table will contain the results for all the proposed thresholds

df_observer = pd.DataFrame(columns=['proposed_safety_margin',
                                          'problematic_cases',
                                          'non_problematic_cases',
                                          'solved_cases',
                                          'unsolved_cases',
                                          'affected_cases',
                                          'not_affected_cases',
                                          'affected_minutes',
                                          'problematic_cases_percent', 
                                          'non_problematic_cases_percent',                                       
                                          'solved_percent',
                                          'un_solved_percent',
                                          'affected_cases_percent',
                                          'not_affected_cases_percent',
                                          'checkin_type',
                                          'total cases',
                                          'verification'])



# let's make a loop to measure on ground how many would be satisfied
# affected rentals and losses if any for various values of thresholds
# each 5 minutes

#@st.cache_data
def create_observer_results():
      
   # create a list of proposed delays
   p = 0
   proposed_list = []
   while p < 125:
      proposed_list.append(p)
      p +=5   

   # Declarations
   total_cases = ds.shape[0]
   no_unique_cars = len(df['car_id'].unique())
   

   # Loop through the proposed delays and calculate the result for each case 'proposed delay'
   for proposed_delay in proposed_list:    

      # the column with the proposed threshold
      ds['proposed_delay'] = proposed_delay   # set up the proposed delay

      # update the results
      do_preparations(proposed_delay)
      ds['status'] = ds.apply(define_status, axis=1)

      ## generate statistics
      # problematic_cases 

      mask = ds['classification'] == 'Problematic'
      problematic_cases = ds.loc[mask,].shape[0]
      
      # non_problematic_cases
      mask = ds['classification'] == 'Non_Problematic'
      non_problematic_cases = ds.loc[mask,].shape[0]

      # solved
      mask = ds['status'] == 'Solved'
      solved_cases = ds.loc[mask,].shape[0]       

      # unsolved
      mask = ds['status'] == 'UnSolved'
      Un_solved_cases = ds.loc[mask,].shape[0]  


      # total_loss
      mask = ds['losses'] > 0
      total_loss = ds.loc[mask,'losses'].sum()

      # affected_cases
      mask = ds['status'] == 'Affected'
      affected_cases = ds.loc[mask].shape[0]
      

      # non affected_cases
      mask = ds['status'] == 'Not affected'
      not_affected_cases = ds.loc[mask].shape[0]
      
      # calculate percentages
      problematic_cases_percent = problematic_cases / total_cases *100
      non_problematic_cases_percent = non_problematic_cases / total_cases * 100
      solved_percentage = solved_cases / problematic_cases * 100
      Un_solved_percentage = Un_solved_cases / problematic_cases * 100
      affected_cases_percent = affected_cases / non_problematic_cases * 100
      not_affected_cases_percent = not_affected_cases / non_problematic_cases *100
      
      new_value = dict({'proposed_safety_margin': proposed_delay,
                                          'problematic_cases': problematic_cases,
                                          'non_problematic_cases': non_problematic_cases,
                                          'solved_cases': solved_cases,
                                          'unsolved_cases': Un_solved_cases,
                                          'affected_cases':affected_cases,
                                          'not_affected_cases':not_affected_cases,
                                          'affected_minutes': total_loss,
                                          'problematic_cases_percent':int(problematic_cases_percent), 
                                          'non_problematic_cases_percent':int(non_problematic_cases_percent),                                       
                                          'solved_percent':int(solved_percentage),
                                          'un_solved_percent':int(Un_solved_percentage),
                                          'affected_cases_percent':int(affected_cases_percent),
                                          'not_affected_cases_percent':int(not_affected_cases_percent),
                                          'checkin_type':0,
                                          'total cases':total_cases,
                                          'verification':0})                                                                                                                                        

      last_row = df_observer.shape[0]
      df_observer.loc[last_row + 1] = new_value
   return df_observer

progress_bar.progress(73, text='Creating the observer')
df_observer = create_observer_results()
#st.dataframe(df_observer)


if 'observer_table' not in st.session_state:
    st.session_state['observer_table'] = df_observer


tab_numbers, tab_percentages = st.tabs(["Numbers", "Percentages"])


with tab_numbers:
    st.subheader("In numbers")
    st.bar_chart(data = df_observer, y = ['solved_cases','unsolved_cases'], x ='proposed_safety_margin',use_container_width=True)   

with tab_percentages:
    st.subheader("Percentage")
    st.bar_chart(data = df_observer, y = ['solved_percent','un_solved_percent'], x ='proposed_safety_margin',use_container_width=True)   

tab_numbers, tab_percentages = st.tabs(["Numbers", "Percentages"])

st.subheader("The number of affected cases due to the safety threshold")

with tab_numbers:
    st.subheader("Numbers...")
    st.bar_chart(data = df_observer, y = ['affected_cases','not_affected_cases'], x ='proposed_safety_margin',use_container_width=True)   

with tab_percentages:
   st.subheader("Percentages..")
   st.bar_chart(data = df_observer, y = ['affected_cases_percent','not_affected_cases_percent'], x ='proposed_safety_margin',use_container_width=True)   
 

#################################################################################################
##########                                                                              #########
##########                                  THE LAB                                     #########
##########                                                                              #########
#################################################################################################
progress_bar.progress(93, text='Creating the lab & Summary')

st.subheader("C) Welcome to the laboratory")
#st.markdown('In here you can investigate the impact when chaninging the threshold value ')


value = st.slider("Choose a threshold as a safety margin", 
          min_value= 0, 
          max_value= int(df_observer['proposed_safety_margin'].max()),
          value= 0, 
          step=5, 
          help= 'Change the threshold to observe the impact', 
          )


st.subheader(f"Chosen Threshold : {value}")

def update_charts(v1): 
    
    #update the table with the chosen threshold
    
    ds = do_preparations(v1)
    ds['status'] = ds.apply(define_status, axis=1)

    fig = px.histogram(ds, x="classification", color="status")
    st.plotly_chart(fig)
    
    mask = df_observer['proposed_safety_margin'] == (v1)    

    col1, col2, col3 = st.columns(3)

    
    col1.metric("**Problematic**", df_observer.loc[mask,['problematic_cases']].values[0])
    col2.metric("**Solved**", df_observer.loc[mask,['solved_cases']].values[0])
    col3.metric("Solved percentage %", df_observer.loc[mask,['solved_percent']].values[0])

    

    col1.metric("Non Problematic", df_observer.loc[mask,['non_problematic_cases']].values[0])
    col2.metric("Affected Cases", df_observer.loc[mask,['affected_cases']].values[0])
    col3.metric("Affected percentage", df_observer.loc[mask,['affected_cases_percent']].values[0])

    st.divider()
    
    col1.metric("Loss in minutes", df_observer.loc[mask,['affected_minutes']].values[0])



update_charts(value)



#Appendix
# if st.checkbox('Hide raw data') != True:
#     st.subheader('Raw data')
#     st.dataframe(df)


####### A.5) Commulative Chart   #######

st.subheader("5. Commulative")

# overlap chart using add_trace and go.figure as below 
# IMPORTANT !! OF COURSE THE histnorm = percent to obtain percentage and valid comaprison
fig = go.Figure(layout_title_text="Histogram Delay vs. Delta distribution")
fig.add_trace(go.Histogram(x=ds['delay_at_checkout_in_minutes'],
                           xbins=dict( # bins used for histogram
                                    start=0.0,
                                    end=200.0,
                                    size=5
                                ), 
    name='Check out Delay', 
    cumulative_enabled=True,   # cummulative enabled
    histnorm = "percent"))     # histnorm = percent to obtain percentage of samples 

fig.add_trace(go.Histogram(x=ds['time_delta_with_previous_rental_in_minutes'],
                           xbins=dict( # bins used for histogram
                               start=0.0,
                               end=200.0,
                               size=5
                               ),
    name='Delta difference between bookings',
    cumulative_enabled=True,
    histnorm ="percent"))

# Overlay both histograms
fig.update_layout(barmode='overlay',xaxis_title='Duration (minutes)', yaxis_title='Counts')
fig.update_xaxes(range=[0, 200])

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)

st.plotly_chart(fig)


                        ####### A.1 ) General delay distribution  #######

st.header('A) General Overview & Statistics')

st.subheader('1. How is the delay distribution?')

# We shall start with general analysis
# we filter the delays greater than 0
mask = df['delay_at_checkout_in_minutes'] >= 0
ds = df.loc[mask,:].copy()

# Layout and organizing the outputs
# use the tabs to illustrate numbers and percentage
tab_numbers, tab_percentages = st.tabs(["Numbers", "Percentages"])

with tab_numbers:
   # plotly figure of type histogram
   fig = px.histogram(ds, x="delay_at_checkout_in_minutes", range_x = [0,200])
   # BINNING: we chose the bining width equals to 5 meaning 5 minutes
   fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5      # binning width
        ))
   st.plotly_chart(fig)
   
   # storing number of rows after filtering the positive delays
   no_of_rows_after_delay_positive = ds.shape[0]

with tab_percentages:

    fig = px.histogram(ds, x="delay_at_checkout_in_minutes", range_x = [0,200],histnorm="percent")
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5
        ))
    st.plotly_chart(fig)
    st.caption("Each bin 'bar'resembles 5 minutes ")

# writing the delay general stats

col1,col2,col3,col4 = st.columns(4)

col1.metric('min',int(ds['delay_at_checkout_in_minutes'].min()))
col2.metric('median',int(ds['delay_at_checkout_in_minutes'].median()))
col3.metric('mean',str(round(ds['delay_at_checkout_in_minutes'].mean(),2)))
col4.metric('max',int(ds['delay_at_checkout_in_minutes'].max()))

median_delay = ds['delay_at_checkout_in_minutes'].mean()

st.markdown("Apparently there are **outliers** values, the maximum delay is greater than 11 hours!! \
            We shall use the following rule to exclue them, the max value in the range will include \
            1.5 times the median, we shall do that in the upcomming analysis.")

st.divider()  


                        ####### A.2) Delay distribution per type  #######

st.subheader('2. The delay distribution per "check_in" type')

# organizing the results in tabs
tab_numbers, tab_percentages = st.tabs(["Numbers", "percentage"])  

with tab_numbers:        

    # to display the check in type within the histogram we used the color = checkin_type
    fig = px.histogram(ds, x="delay_at_checkout_in_minutes", range_x = [0,200],  color='checkin_type')
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5      # bins five minutes
        ))
    st.plotly_chart(fig)

    st.markdown("**OBSERVATION :** It can be noticed easily that the check_in type **'mobile'** plays a big role in \
                producing the majority of the delay cases, unlike the check_in type **'connect'** \
                which has a negligable impact.")


with tab_percentages:
    # to display the check in type within the histogram we used the color = checkin_type
    fig = px.histogram(ds, x="delay_at_checkout_in_minutes", range_x = [0,200],  color='checkin_type', histnorm='percent')
    fig.update_traces(xbins=dict( # bins used for histogram
            start=0.0,
            end=200.0,
            size=5
        ))
    st.plotly_chart(fig)
    st.markdown(" **Important Note :**")
    st.markdown("Here, the percentages of each bin or 'bar'represent the percentage of the series \
                itself and **NOT** the total samples, example the first bar (0 to 4) miuntes are 10 percent of the \
                connect series ONLY and not the 'connect + mobile' combined.")
    

    st.caption("There were some cases where the car was returned earlier but had been filtered out \
            to focus on the delay ")
    

st.divider()

                        ####### A.3) Delta distribution   #######

st.subheader('3. What about the DELTA distribution?')

st.markdown('The delta is the planned difference in time between the bookings ')

# similar to the steps above except that here we display the delta instead of delay

fig = px.histogram(ds, x="time_delta_with_previous_rental_in_minutes", range_x = [0,200])
fig.update_traces(xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5
    ))
st.plotly_chart(fig)

st.markdown("- **Another observation** Notice how the delta is **distributed evenly** in an integer around \
            30 minutes, i.e. 30 mins, 1 hour, 1.5 hour, 2hours, etc..,\
            this could be useful to solve the problem, we'll see how..  ")
st.markdown("- Also here we can see that there are outliers that need to be clipped out")

# displaying the general stats of the delta
col1,col2,col3,col4 = st.columns(4)

col1.metric('min',int(ds['time_delta_with_previous_rental_in_minutes'].min()))
col2.metric('median',int(ds['time_delta_with_previous_rental_in_minutes'].median()))
mean_delta = str(round(ds['time_delta_with_previous_rental_in_minutes'].mean(),2))
col3.metric('mean',mean_delta)
col4.metric('max',int(ds['time_delta_with_previous_rental_in_minutes'].max()))

median_delta = ds['time_delta_with_previous_rental_in_minutes'].median()

st.divider()


                             ####### A.4) Overlapping Delta and delay   #######

st.subheader("4. Let's overlap them")

# to implement the overlap we use the add.trace technique in go figure plotly as follows:
fig = go.Figure(layout_title_text="Histogram Delay vs. Delta distribution")
fig.add_trace(go.Histogram(x=ds['delay_at_checkout_in_minutes'],xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5
    ), name='Check out Delay'))
fig.add_trace(go.Histogram(x=ds['time_delta_with_previous_rental_in_minutes'],xbins=dict( # bins used for histogram
        start=0.0,
        end=200.0,
        size=5), name='Delta difference between bookings', marker =dict(color='red')))

# Overlay both histograms
fig.update_layout(barmode='overlay',xaxis_title='Duration (minutes)', yaxis_title='Counts')
fig.update_xaxes(range=[0, 200])

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
st.plotly_chart(fig)
st.divider()


st.dataframe(ds)
#################################################################################################
##########                                                                              #########
##########                    C) Executive Summary                                      #########
##########                                                                              #########
#################################################################################################

st.markdown('#Executive summary')


data = dict(
    number=[count_1_total,
            count_2_exclude_negative_delay,
            count_3_after_na_deltas_delay, 
            count_4_after_outliers_delay, 
            count_5_after_outliers_delta, 
            count_6_problematic_cases],

    stage=["Total rental records", 
           "After excluding negative delays", 
           "Exlcuding the empty reference ids and delays", 
           "After excluding the delay outliers", 
           "After excluding the delta outliers",
           "Problematic cases"],
           
    textinfo = "value+percent initial",
           )

fig_funnel = px.funnel(data, x='number', y='stage')


st.plotly_chart(fig_funnel)

progress_bar.progress(100, text='Completed Successfully')
progress_bar.empty()
