import pickle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel  # This is used for classes and data verification
from typing import Literal, List, Union    # these are used for validating the entry during the post
import numpy as np
import pandas as pd
import joblib # to import both the scaler and our chosen model
import os
from sklearn.metrics import accuracy_score, f1_score, ConfusionMatrixDisplay, RocCurveDisplay


## configurations
description ="""
Welcome to cars rental estimator, 
kindly ass in the features that you like to estimate the price, 
"""
app = FastAPI(title="Rental cost estimator",description = description)

class CarFeatures(BaseModel):
    name:   str
    mileage:     int     
    engine_power:int
    fuel:        str
    paint_color: str
    car_type:    str
    private_parking_available: int
    has_gps:                        int
    has_air_conditioning:           int
    automatic_car:                  int
    has_getaround_connect:          int
    has_speed_regulator:            int
    winter_tires:                   int
   
class Test(BaseModel):
    title:str

# This function is to treat the incomming data i.e. the recieved features

def prepare_input_to_df(car: CarFeatures):

    # define the columns/fields of the dataframe series
    # there is no unnammed value and no label ofcourse
    df = pd.DataFrame(columns=['name','mileage', 'engine_power', 'fuel',
       'paint_color', 'car_type', 'private_parking_available', 'has_gps',
       'has_air_conditioning', 'automatic_car', 'has_getaround_connect',
       'has_speed_regulator', 'winter_tires'],
      )
    
    print('dataframe defined:')
    print(df)
    
    
    # set the entity values 
    entity = {'name' : car.name,
        'mileage' : car.mileage,
        'engine_power' : car.engine_power,
        'fuel': car.fuel,
        'paint_color': car.paint_color,
        'car_type' : car.car_type,
        'private_parking_available' : int(car.private_parking_available),
        'has_gps' : int(car.has_gps),
        'has_air_conditioning': int(car.has_air_conditioning),
        'automatic_car' : int(car.automatic_car),
        'has_getaround_connect' : int(car.has_getaround_connect),
        'has_speed_regulator' : int(car.has_speed_regulator),
        'winter_tires' : int(car.winter_tires) }

      
    # add the record
    df.loc[df.shape[0],:] = entity
    print(df)

    # Transfer the boolean field
    bool_list = ['private_parking_available','has_gps','has_air_conditioning','automatic_car',
                 'has_getaround_connect',
                 'has_speed_regulator','winter_tires','engine_power','mileage']
    
    for property in bool_list:
        #df[property] = df[property].apply(lambda x : 1 if x == True else 0)
        df[property] = df[property].astype(int)

    
    
    print(df)

    return df


       
### define the enpoints


@app.get("/")
async def index():

    message = "Hello... and welcome to the getaround rental price prediction/estimator"

    return message


@app.get("/Details")
async def index():

    message = "details"

    return message


# POST API
@app.post("/predict")
async def predict( features_recieved : CarFeatures):    # define an asynchro function that inherits from CarType class
    

    #1) Transform the input into pandas dataframe

    print('preparing:')
    df_input = prepare_input_to_df(features_recieved)
    

    #2)  load the scaler and our chosen model

    print('importing scaler and regressor')
    
    scaler = joblib.load('scaler_v3.joblib')
    print('imported')

    # model = joblib.load('regressor_ridge_v3.joblib')


    #3) Scaling (Transform)
    print('Scaling:')
    scaled_X = scaler.transform(df_input)
    print(scaled_X)
    

    # 4) IMport model
    model = pickle.load(open('model.pkl', 'rb'))
    
    
    #4) Predict
    print('predicting')
    y_pred = model.predict(scaled_X)

    #5) Format and return response
    print(y_pred.tolist())
    response =  {"prediction": y_pred.tolist()[0]}

    return response
 


# Execute if running as a main file
if __name__=="__main__":  
    uvicorn.run(app, host="0.0.0.0", port=4000) # The FastAPI instance will use host IP (0.0.0.0) and port (4000)

# snap of results for car:
{
  "name": "Peugeot",
  "mileage": 123886,
  "engine_power": 125,
  "fuel": "petrol",
  "paint_color": "black",
  "car_type": "convertible",
  "private_parking_available": 1,
  "has_gps": 0,
  "has_air_conditioning": 0,
  "automatic_car": 0,
  "has_getaround_connect": 0,
  "has_speed_regulator": 1,
  "winter_tires": 1
}

{
  "prediction": 97.21388681490158
}
#      
# TESTING CODE
# @app.post("/predict")
# async def predict( car : CarFeatures):    # define an asynchro function that inherits from CarType class
#     entity = pd.series({'name' : car.name})
        # 'mileage' : car.mileage,
        #       'engine_power' : car.engine_power,
        #       'fuel': car.fuel,
        #       'paint_color': car.paint_color,
        #        'car_type' : car.car_type,
        #       'private_parking_available' : car.private_parking_available,
        #     'has_gps' : car.has_gps,
        #     'has_air_conditioning': car.has_air_conditioning,
        #     'automatic_car' : car.automatic_car,
        #     'has_getaround_connect' : car.has_getaround_connect,
        #     'has_speed_regulator' : car.has_speed_regulator,
        #     'winter_tires' : car.winter_tires })
    
    #return entity.to_json()
    
     
# result = pd.Series({'cartype' : testing.title, 'flag': 1}) 
#     return result.to_json()




