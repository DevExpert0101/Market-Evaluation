# Algorithm

The function `cal_market_value` calculate salary about input information.

The model was trained on the dataset with the criterias like Age, Gender, Education Level, Job Title, Years of Experience.
Based on these 5 criterias, the model predict salary.

# Environment

For running this script, you have to install python libraries like
scikit-learn, fastapi and uvicorn.

# Input

```
{
  "age": 45,
  "gender": "Female",
  "education_level": "PhD",
  "job_title": "Senior UX Designer",
  "years_of_experience": 16
}
```

Input format should be like above.

gender: "Male" or "Female" \
education_level: "Bachelor's", "Master's" or "PhD"\
job_title: "Financial Analyst", "Senior Engineer", "Junior Developer" and so on.

Each category should be selected from dataset's category column.

# Output
```
15170
```

Output is the value of Predicted Salary