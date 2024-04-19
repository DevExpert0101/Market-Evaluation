# 1. Market Evaluation

This is implemented in `main.py`
## Algorithm

The function `cal_market_value` calculate salary about input information.

The model was trained on the dataset with the criterias like Age, Gender, Education Level, Job Title, Years of Experience.
Based on these 5 criterias, the model predict salary.

## Environment

For running this script, you have to install python libraries like
scikit-learn, fastapi and uvicorn.

## Input

```json
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

## Output
```
15170
```

Output is the value of Predicted Salary

# 2. Scoring and Ranking
This is implemented in `scoring.py`
## Scoring

According to each candidate's career, function `cal_score` calculates score.

```
Education Level:
    - Phd: 5
    - Master's: 4
    - Bachelor's: 3

Years of Experience:
    - >= 10: 5
    - >= 8: 4
    - >= 5: 3
    - >= 3: 2
    - >= 1: 1

Matching Skills:
    - > 4: 5
    - > 3: 4
    - > 2: 3
    - > 1: 2
    -      1
Matching Certifications:
    - > 4: 5
    - > 3: 4
    - > 2: 3
    - > 1: 2
    -      1
References:
    - Number of references
Cultural Fit:
    - Cultural Fit Score
```

For each candidate, calculate the score for each criterion and multiply it by the assigned weight.
Add up all the weighted scores to get the total score for each candidate.

```python
total_score = (
        education_score * criteria_weights["Education Level"]
        + experience_score * criteria_weights["Years of Experience"]
        + skills_score * criteria_weights["Skills"]
        + certification_score * criteria_weights["Certifications"]
        + references_score * criteria_weights["References"]
        + cultural_fit_score * criteria_weights["Cultural Fit"]
    )
```


## Ranking

Based on scores, funciton `sort_candidates` sort candidates.
If there are some who has same score, then the function `calculate_requirement_match_score` resort according to the requirements.

This is sample input JSON format.
```json
{
    "candidates": [
        {
            "name": "Andre Cain",
            "education_level": "Phd",
            "years_of_experience": 13,
            "skills": [
                "Python",
                "Java",
                "Machine Learning"
            ],
            "certifications": [
                "AWS Certified Cloud Practitioner"
            ],
            "references": [
                "Ref1",
                "Ref2"
            ],
            "cultural_fit": 8
        },
        {
            "name": "John Lee",
            "education_level": "Master's",
            "years_of_experience": 8,
            "skills": [
                "Python",
                "Java",
                "C++",
                "Machine Learning"
            ],
            "certifications": [
                "AWS Certified Computing Engineer"
            ],
            "references": [
                "Ref1"
            ],
            "cultural_fit": 4
        },
        {
            "name": "Christopher Martin",
            "education_level": "Bachelor's",
            "years_of_experience": 10,
            "skills": [
                "Python",
                "Java",
                "Machine Learning",
                "Deep Learning",
                "C++",
                "Computer Vision",
                "NLP"
            ],
            "certifications": [
                "AWS Certified Cloud Practitioner",
                "Cert1",
                "Cert2"
            ],
            "references": [
                "Ref1",
                "Ref2",
                "Ref3"
            ],
            "cultural_fit": 5
        },
        {
            "name": "Christopher Wilson",
            "education_level": "Bachelor's",
            "years_of_experience": 12,
            "skills": [
                "Python",
                "Java",
                "Machine Learning",
                "Deep Learning",
                "C++",
                "Computer Vision",
                "NLP"
            ],
            "certifications": [
                "AWS Certified Cloud Practitioner",
                "Cert1",
                "Cert2"
            ],
            "references": [
                "Ref1",
                "Ref2",
                "Ref3"
            ],
            "cultural_fit": 5
        }
    ],
    "requirements": {
        "education_level": "PhD",
        "years_of_experience": 10,
        "skills": [
            "Python",
            "Machine Learning"
        ],
        "certifications": [
            "AWS Certified Cloud Practitioner"
        ]
    }
}
```


