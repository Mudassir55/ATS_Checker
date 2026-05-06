from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.keyword_extractor import clean_text

# Common technical skills
SKILLS_DATABASE = [
    'python',
    'java',
    'sql',
    'machine learning',
    'data analysis',
    'excel',
    'power bi',
    'tensorflow',
    'pandas',
    'numpy',
    'scikit-learn',
    'deep learning',
    'communication',
    'leadership',
    'html',
    'css',
    'javascript',
    'react',
    'nodejs',
    'django',
    'flask'
]

# Extract skills from text

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_DATABASE:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


# Calculate ATS score

def calculate_ats_score(resume_text, job_description):
     # TF-IDF Similarity
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    similarity_score = round(similarity[0][0] * 100, 2)

    # Skills Matching
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched_skills = list(set(resume_skills) & set(jd_skills))

    missing_skills = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        skills_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skills_score = 0

    # Final ATS Score
    ats_score = round(
        (similarity_score * 0.7) +
        (skills_score * 0.3),
        2
    )

    return {
        'ats_score': ats_score,
        'similarity_score': similarity_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'resume_skills': resume_skills,
        'jd_skills': jd_skills
    }