from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
from fastapi import FastAPI
import uvicorn
import numpy as np
from pydantic import BaseModel
from joblib import load
# model = pickle.load(open('weight.pickle', 'rb'))
model = load('weight.pickle')
le_gender = LabelEncoder()
le_education = LabelEncoder()
le_job = LabelEncoder()
le_gender.classes_ = np.load('encoder_gender.npy', allow_pickle=True)
le_education.classes_ = np.load('encoder_education.npy', allow_pickle=True)
le_job.classes_ = np.load('encoder_job.npy', allow_pickle=True)


app = FastAPI()


class Item(BaseModel):
    age: int
    gender: str
    education_level: str
    job_title: str
    years_of_experience: int


@app.post("/marketvalue")
def cal_market_value(item: Item):
    print(item.gender)
    encoded_gender = le_gender.transform([item.gender])
    encoded_education_level = le_education.transform([item.education_level])
    encoded_job_title = le_job.transform([item.job_title])

    data = np.array([[ item.age, encoded_gender[0], encoded_education_level[0], encoded_job_title[0], item.years_of_experience]])

    predicted_salary = model.predict(data)[0]
    
    return predicted_salary
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


