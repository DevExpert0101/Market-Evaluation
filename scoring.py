from fastapi import FastAPI

criteria_weights = {
    "Education Level": 0.2,
    "Years of Experience": 0.3,
    "Skills": 0.25,
    "Certifications": 0.1,
    "References": 0.1,
    "Cultural Fit": 0.05
}

required_skills = ["Python", "C++", "Java", "Machine Learning", "Deep Learning"]
required_certs = ["Cert1", "Cert2"]

candidate1 = {
    "Name": "Andre Cain",
    "Education Level": "Phd",
    "Years of Experience": 13,
    "Skills": ["Python", "Java", "Machine Learning"],
    "Certifications": ["AWS Certified Cloud Practitioner"],
    "References": ["Ref1", "Ref2"],
    "Cultural Fit": 8,
}
candidate2 = {
    "Name": "John Lee",
    "Education Level": "Master's",
    "Years of Experience": 8,
    "Skills": ["Python", "Java", "C++", "Machine Learning"],
    "Certifications": ["AWS Certified Computing Engineer"],
    "References": ["Ref1"],
    "Cultural Fit": 4,
}
candidate3 = {
    "Name": "Christopher Martin",
    "Education Level": "Bachelor's",
    "Years of Experience": 10,
    "Skills": ["Python", "Java", "Machine Learning", "Deep Learning", "C++", "Computer Vision", "NLP"],
    "Certifications": ["AWS Certified Cloud Practitioner", "Cert1", "Cert2"],
    "References": ["Ref1", "Ref2", "Ref3"],
    "Cultural Fit": 5,
}
candidate4 = {
    "Name": "Christopher Wilson",
    "Education Level": "Bachelor's",
    "Years of Experience": 12,
    "Skills": ["Python", "Java", "Machine Learning", "Deep Learning", "C++", "Computer Vision", "NLP"],
    "Certifications": ["AWS Certified Cloud Practitioner", "Cert1", "Cert2"],
    "References": ["Ref1", "Ref2", "Ref3"],
    "Cultural Fit": 5,
}

candidates = [candidate1, candidate2, candidate3, candidate4]


def cal_score(candidate):

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
    
    education_score = education_score(candidate["Education Level"])
    experience_score = experience_score(candidate["Years of Experience"])
    skills_score = skills_score(candidate["Skills"], required_skills)
    certification_score = certification_score(candidate["Certifications"], required_certs)
    references_score = references_score(candidate["References"])
    cultural_fit_score = cultural_fit_score(candidate["Cultural Fit"])

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
    if candidate["Education Level"] == requirements["Education Level"]:
        score += 3  # Adjust weight as needed
    elif candidate["Education Level"] in ("Master's", "PhD") and requirements["Education Level"] == "Bachelor's":
        score += 1  # Lower weight for exceeding minimum education

    # Experience (meeting or exceeding minimum experience gets a point)
    if candidate["Years of Experience"] >= requirements["Years of Experience"]:
        score += 2  # Adjust weight as needed

    # Skills (all required skills met get a point)
    required_skills = set(requirements["Skills"])
    candidate_skills = set(candidate["Skills"])
    if required_skills.issubset(candidate_skills):
        score += 1  # Adjust weight as needed

    # Certifications (having all required certifications gets a point)
    required_certs = set(requirements["Certifications"])
    candidate_certs = set(candidate["Certifications"])
    if required_certs.issubset(candidate_certs):
        score += 1  # Adjust weight as needed

    return score



scores = [cal_score(can) for can in candidates]

requirements = {
  "Education Level": "Master's",
  "Years of Experience": 10,
  "Skills": ["Python", "Machine Learning"],
  "Certifications": ["AWS Certified Cloud Practitioner"],
}

sorted_candidates = sort_candidates(candidates, scores, requirements)

print("Candidates sorted by score (highest to lowest) with requirement tiebreaker:")
for candidate in sorted_candidates:
  print(candidate["Name"])
