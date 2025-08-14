# Customer Support RAG System with Sentiment Analysis (Advanced Demo)

import os
import json
try:
    from textblob import TextBlob
except ImportError:
    print("TextBlob not found. Please install with 'pip install textblob'.")
    exit(1)

# Dummy Knowledge Base
KNOWLEDGE_BASE = [
    {"id": 1, "title": "Reset Password", "content": "To reset your password, click 'Forgot Password' on the login page."},
    {"id": 2, "title": "Update Email", "content": "Go to account settings to update your email address."},
    {"id": 3, "title": "Cancel Subscription", "content": "Contact support to cancel your subscription."}
]

# Retrieve relevant articles (simple keyword search)
def retrieve_articles(query, kb):
    results = []
    for article in kb:
        if query.lower() in article["title"].lower() or query.lower() in article["content"].lower():
            results.append(article)
    return results

# Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    return "neutral"

# Emotion Detection (simple lexicon-based)
emotion_lexicon = {
    "angry": ["angry", "mad", "furious", "annoyed", "irritated"],
    "sad": ["sad", "upset", "unhappy", "depressed", "disappointed"],
    "happy": ["happy", "glad", "pleased", "satisfied", "joyful"],
    "frustrated": ["frustrated", "stuck", "confused", "lost", "overwhelmed"],
    "neutral": []
}

def detect_emotion(text):
    text_lower = text.lower()
    for emotion, keywords in emotion_lexicon.items():
        for word in keywords:
            if word in text_lower:
                return emotion
    return "neutral"

# Satisfaction Tracking
def update_satisfaction(history):
    if not history:
        return 0.0
    scores = [TextBlob(msg).sentiment.polarity for msg in history]
    return sum(scores) / len(scores)

# Advanced Escalation Prediction
def advanced_escalation(sentiment, emotion, satisfaction, history):
    negative_count = sum(1 for s in history if analyze_sentiment(s) == "negative")
    if sentiment == "negative" or emotion in ["angry", "frustrated"]:
        return True
    if satisfaction < -0.3:
        return True
    if negative_count >= 2:
        return True
    return False

# Response Tone Calibration
def calibrate_tone(sentiment, emotion, escalation):
    if escalation:
        return "apologetic"
    if emotion == "happy" or sentiment == "positive":
        return "cheerful"
    if emotion in ["angry", "frustrated", "sad"] or sentiment == "negative":
        return "reassuring"
    return "neutral"

# Empathetic Response Generation (advanced)
def generate_advanced_response(query, sentiment, emotion, escalation, tone, articles):
    if escalation:
        response = "I'm really sorry you're having trouble. I've flagged this for our support team to help you as soon as possible."
    elif tone == "reassuring":
        response = "I understand how you feel. Let's work together to solve this."
    elif tone == "cheerful":
        response = "Great to hear from you! Here's some info that might help:"
    else:
        response = "Here's some information that might help you:"
    if articles:
        response += "\n" + "\n".join(["- {}: {}".format(a['title'], a['content']) for a in articles])
    else:
        response += "\nSorry, I couldn't find any relevant articles."
    return response

# Multi-turn Conversation Analysis & Main Loop
def main():
    print("Customer Support RAG System (Advanced Demo)")
    history = []
    while True:
        user_input = input("Customer: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        history.append(user_input)
        sentiment = analyze_sentiment(user_input)
        emotion = detect_emotion(user_input)
        satisfaction = update_satisfaction(history)
        articles = retrieve_articles(user_input, KNOWLEDGE_BASE)
        escalation = advanced_escalation(sentiment, emotion, satisfaction, history)
        tone = calibrate_tone(sentiment, emotion, escalation)
        response = generate_advanced_response(user_input, sentiment, emotion, escalation, tone, articles)
        print("Support (sentiment={}, emotion={}, escalation={}, tone={}, satisfaction={:.2f}): {}\n".format(
            sentiment, emotion, escalation, tone, satisfaction, response))

if __name__ == "__main__":
    main()