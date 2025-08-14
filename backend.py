# FastAPI backend for Customer Support RAG System
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import os
from textblob import TextBlob

app = FastAPI()



# Dummy Knowledge Base
KNOWLEDGE_BASE = [
    {"id": 1, "title": "Reset Password", "content": "To reset your password, click 'Forgot Password' on the login page."},
    {"id": 2, "title": "Update Email", "content": "Go to account settings to update your email address."},
    {"id": 3, "title": "Cancel Subscription", "content": "Contact support to cancel your subscription."}
]


class ChatRequest(BaseModel):
    message: str
    history: List[str] = []
    user_name: str = "Customer"
    category: str = "General"
    urgency: str = "Normal"
    feedback: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sentiment: str
    escalation: bool
    tone: str
    articles: List[dict]


# Fuzzy search for RAG
from fuzzywuzzy import fuzz



@app.post("/rag", response_model=ChatResponse)
def rag_endpoint(req: ChatRequest):
    query = req.message
    history = req.history
    user_name = req.user_name
    category = req.category
    urgency = req.urgency
    feedback = req.feedback
    # Sentiment analysis using TextBlob
    blob = TextBlob(query)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        sentiment = "positive"
    elif polarity < -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    # Escalation prediction (simple)
    escalation = sentiment == "negative" or history.count("negative") >= 2 or urgency.lower() == "high"
    # Fuzzy retrieve articles
    articles = []
    for a in KNOWLEDGE_BASE:
        title_score = fuzz.partial_ratio(query.lower(), a["title"].lower())
        content_score = fuzz.partial_ratio(query.lower(), a["content"].lower())
        if title_score > 70 or content_score > 70 or category.lower() in a["title"].lower():
            articles.append(a)
    # Tone calibration
    if escalation:
        tone = "apologetic"
    elif sentiment == "positive":
        tone = "cheerful"
    elif sentiment == "negative":
        tone = "reassuring"
    else:
        tone = "neutral"
    # Response generation using template
    rag_text = "\n".join([f"- {a['title']}: {a['content']}" for a in articles]) if articles else "No relevant articles found."
    if escalation:
        response = f"{user_name}, I'm really sorry you're having trouble. I've flagged this for our support team to help you as soon as possible."
    elif sentiment == "negative":
        response = f"{user_name}, I understand this can be frustrating. Let me help you with the following information:"
    elif sentiment == "positive":
        response = f"{user_name}, glad to hear things are going well! Here's some info that might help:"
    else:
        response = f"{user_name}, here's some information that might help you:"
    response += "\n" + rag_text
    if feedback:
        response += f"\nFeedback received: {feedback}"
    return ChatResponse(
        response=response,
        sentiment=sentiment,
        escalation=escalation,
        tone=tone,
        articles=articles
    )
