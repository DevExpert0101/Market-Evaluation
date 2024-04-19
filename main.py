from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
from fastapi import FastAPI
import uvicorn
import numpy as np
from pydantic import BaseModel
from joblib import load
from typing import List, Union
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
    

criteria_weights = {
    "Education Level": 0.2,
    "Years of Experience": 0.3,
    "Skills": 0.25,
    "Certifications": 0.1,
    "References": 0.1,
    "Cultural Fit": 0.05
}

class RequirementsSchema(BaseModel):
    education_level: str
    years_of_experience: int
    skills: List[str]
    certifications: List[str]

class CandidateSchema(BaseModel):
    name: str
    education_level: str
    years_of_experience: int
    skills: List[str]
    certifications: List[str]
    references: List[str]
    cultural_fit: int

class ScoringItem(BaseModel):
    candidates: List[CandidateSchema]
    requirements: RequirementsSchema



def cal_score(candidate, requirements):

    # dic_data = candidate.to_dict()
    dic_data = candidate
    score = 0
    
    def education_score(Education_Level):
        scores = {"Bachelor's": 3, "Master's": 4, "Phd": 5}
        return scores.get(Education_Level, 0)
    
    def experience_score(years):
        if years >= 10:
            return 5
        elif years >= 8:
            return 4
        elif years >= 5:
            return 3
        elif years >= 3:
            return 2
        else:
            return 1
        
    def skills_score(candidate_skills, required_skills):
        matched_skills = len(set(candidate_skills) & set(required_skills))
        if matched_skills > 4:
            return 5
        elif matched_skills > 3:
            return 4
        elif matched_skills > 2:
            return 3
        elif matched_skills > 1:
            return 2
        else:
            return 1
        
    def certification_score(certifications, required_certs):
        matched_certs = len(set(certifications) & set(required_certs))
        if matched_certs > 4:
            return 5
        elif matched_certs > 3:
            return 4
        elif matched_certs > 2:
            return 3
        elif matched_certs > 1:
            return 2
        else:
            return 1

    def references_score(references):
        return len(references)
    
    def cultural_fit_score(cultural_fit):
        return cultural_fit
    
    education_score = education_score(candidate.education_level)
    experience_score = experience_score(candidate.years_of_experience)
    skills_score = skills_score(candidate.skills, requirements.skills)
    certification_score = certification_score(candidate.certifications, requirements.certifications)
    references_score = references_score(candidate.references)
    cultural_fit_score = cultural_fit_score(candidate.cultural_fit)

    # Calculate weighted total score
    total_score = (
        education_score * criteria_weights["Education Level"]
        + experience_score * criteria_weights["Years of Experience"]
        + skills_score * criteria_weights["Skills"]
        + certification_score * criteria_weights["Certifications"]
        + references_score * criteria_weights["References"]
        + cultural_fit_score * criteria_weights["Cultural Fit"]
    )


    return total_score


@app.post("/scoring")
def scoring(item: ScoringItem):
    candidates = item.candidates
    requirements = item.requirements


    scores = [cal_score(cand, requirements) for cand in candidates]    
    print("--", scores)
    sorted_candidates = sort_candidates(candidates, scores, requirements)

    print("Candidates sorted by score (highest to lowest) with requirement tiebreaker:")
    for candidate in sorted_candidates:
        print(candidate.name)
    
    return sorted_candidates

def sort_candidates(candidates, scores, requirements):
    """
    Sorts a list of candidates based on scores and requirements (in case of ties).

    Args:
        candidates (list): A list of dictionaries representing candidates.
        scores (list): A list of floats containing the scores for each candidate.
        requirements (dict): A dictionary specifying the required skills, experience,
                            and education level for the position.

    Returns:
        list: A new list of candidates sorted by score and then by requirements (highest to lowest).
    """

    # Ensure candidates and scores lists have the same length
    if len(candidates) != len(scores):
        raise ValueError("Number of candidates and scores must match.")

    # Create a list of tuples (candidate, score, requirement_match_score)
    candidate_scores_requirements = []
    for candidate, score in zip(candidates, scores):
        requirement_match_score = calculate_requirement_match_score(candidate, requirements)
        candidate_scores_requirements.append((candidate, score, requirement_match_score))

    # Sort based on score (descending) and requirement match score (ascending)
    sorted_candidates = sorted(candidate_scores_requirements,
                                key=lambda x: (x[1], -x[2]), reverse=True)

    # Extract the sorted list of candidates
    return [candidate for candidate, _, _ in sorted_candidates]

def calculate_requirement_match_score(candidate, requirements):
    """
    Calculates a score based on how well the candidate meets the requirements.

    Args:
        candidate (dict): A dictionary representing a candidate.
        requirements (dict): A dictionary specifying the required skills, experience,
                            and education level for the position.

    Returns:
        int: A score reflecting the candidate's match with the requirements (higher is better).
    """

    score = 0

    # Education (higher education has higher weight)
    if candidate.education_level == requirements.education_level:
        score += 3  # Adjust weight as needed
    elif candidate.education_level in ("Master's", "PhD") and requirements.education_level == "Bachelor's":
        score += 1  # Lower weight for exceeding minimum education

    # Experience (meeting or exceeding minimum experience gets a point)
    if candidate.years_of_experience >= requirements.years_of_experience:
        score += 2  # Adjust weight as needed

    # Skills (all required skills met get a point)
    required_skills = set(requirements.skills)
    candidate_skills = set(candidate.skills)
    if required_skills.issubset(candidate_skills):
        score += 1  # Adjust weight as needed

    # Certifications (having all required certifications gets a point)
    required_certs = set(requirements.certifications)
    candidate_certs = set(candidate.certifications)
    if required_certs.issubset(candidate_certs):
        score += 1  # Adjust weight as needed

    return score


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


