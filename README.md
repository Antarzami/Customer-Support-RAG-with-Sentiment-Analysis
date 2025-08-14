# Customer Support RAG System with Sentiment Analysis

## Overview
This project is an advanced demo of a Customer Support Retrieval-Augmented Generation (RAG) system enhanced with sentiment analysis and emotion detection. It simulates a support agent that can retrieve relevant knowledge base articles, analyze customer sentiment and emotions, track satisfaction, predict escalation, and generate empathetic responses.

## Features
- **Knowledge Base Search:** Retrieves relevant articles using keyword search.
- **Sentiment Analysis:** Uses TextBlob to detect positive, negative, or neutral sentiment in customer messages.
- **Emotion Detection:** Lexicon-based detection of emotions such as angry, sad, happy, frustrated, and neutral.
- **Satisfaction Tracking:** Tracks customer satisfaction over multiple turns.
- **Escalation Prediction:** Predicts when a conversation should be escalated to human support.
- **Response Tone Calibration:** Adjusts the tone of responses based on sentiment, emotion, and escalation status.
- **Empathetic Response Generation:** Generates responses that are informative and empathetic.

## How It Works
1. The user interacts with the system via the command line.
2. Each message is analyzed for sentiment and emotion.
3. The system retrieves relevant articles from the knowledge base.
4. Satisfaction is tracked across the conversation.
5. Escalation is predicted if negative sentiment/emotion is detected or satisfaction drops.
6. The response tone is calibrated and an empathetic response is generated.

## Requirements
- Python 3.7+
- `textblob` library

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the main application:
```bash
python app.py
```
Type your queries as a customer. Type `exit` or `quit` to end the session.

## File Structure
- `app.py`: Main application logic and conversation loop
- `backend.py`: (Optional) Backend support functions
- `frontend.py`: (Optional) Frontend interface code
- `requirements.txt`: Python dependencies

## Example Interaction
```
Customer: I am angry because I can't reset my password
Support (sentiment=negative, emotion=angry, escalation=True, tone=apologetic, satisfaction=-0.50): I'm really sorry you're having trouble. I've flagged this for our support team to help you as soon as possible.
- Reset Password: To reset your password, click 'Forgot Password' on the login page.
```

## License
This project is for educational/demo purposes.
