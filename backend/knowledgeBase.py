knowledge_base = [
    {
        "question": "how can i improve team productivity",
        "answer": "Use daily stand-ups, set clear OKRs, and encourage time-blocking.",
        "keywords": ["productivity", "team", "improve", "efficiency"]
    },
    {
        "question": "tips for remote work",
        "answer": "Maintain a fixed schedule, use video check-ins, and set clear boundaries.",
        "keywords": ["remote", "work", "tips", "home office"]
    },
    {
        "question": "how to prioritize tasks",
        "answer": "Use the Eisenhower Matrix: urgent-important, not urgent-important, etc.",
        "keywords": ["prioritize", "tasks", "matrix", "time management"]
    },
    {
        "question": "how to manage startup funding",
        "answer": "Track runway, maintain investor relations, and plan funding rounds early.",
        "keywords": ["startup", "funding", "finance", "investors"]
    },
    {
        "question": "best practices for code review",
        "answer": "Keep reviews small, provide constructive feedback, and focus on the code not the person.",
        "keywords": ["code review", "practices", "development", "quality"]
    },
    {
        "question": "how to handle project deadlines",
        "answer": "Break large tasks into smaller milestones, communicate risks early, and maintain buffer time.",
        "keywords": ["deadlines", "project", "time management", "planning"]
    },
    {
        "question": "ways to boost employee engagement",
        "answer": "Provide regular feedback, recognize achievements, offer growth opportunities, and create a positive work culture.",
        "keywords": ["engagement", "employees", "motivation", "culture"]
    },
    {
        "question": "how to scale a tech team",
        "answer": "Establish clear processes, invest in documentation, and hire for cultural fit.",
        "keywords": ["scale", "team", "tech", "growth"]
    },
    {
        "question": "what are good leadership skills",
        "answer": "Good leaders communicate clearly, show empathy, make decisive decisions, and empower their team.",
        "keywords": ["leadership", "skills", "management", "communication"]
    },
    {
        "question": "how to manage stress at work",
        "answer": "Take regular breaks, practice time management, exercise regularly, and maintain work-life balance.",
        "keywords": ["stress", "work", "management", "wellness"]
    }
]


#I will now create the first helper function that finds the best matching question in local knowledge base.
def find_best_match(user_q): 
    usrQLwr = user_q.lower().strip()
    
    # If the response is direct question match
    for item in knowledge_base:
        if item["question"] == usrQLwr:
            return {"answer": item["answer"], "confidence": 100, "matched": True}
    
    # I will implement the keyword matching logic here, because it will help us find the confidence by enhanced keyword matching
    best_score = 0
    best_answer = None
    best_item = None
    
    for item in knowledge_base:
        score = 0
        userWrds = set(usrQLwr.split())
        
        # Count keyword matches with weighted scoring
        for keyword in item["keywords"]:
            if keyword in usrQLwr:
                score += 3  # Exact keyword match
            elif any(word in userWrds for word in keyword.split()):
                score += 1  # Partial word match
        
        # Bonus for question similarity
        question_words = set(item["question"].split())
        common_words = userWrds.intersection(question_words)
        score += len(common_words) * 2
        
        if score > best_score:
            best_score = score
            best_answer = item["answer"]
            best_item = item
    
    # Only return KB(Knowledge Base) answer if confidence is high enough
    if best_score >= 4:  # I setup minimum threshold  t0 4 for KB usage
        return {"answer": best_answer, "confidence": best_score, "matched": True, "source_item": best_item}
    else:
        return {"answer": None, "confidence": 0, "matched": False}