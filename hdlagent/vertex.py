#!/usr/bin/env/ python3
# gcloud auth application-default login

import vertexai
from vertexai.preview.generative_models import GenerativeModel
#from vertexai import generative_models
def generate():
    model = GenerativeModel("gemini-1.0-pro-001")

    chat = model.start_chat()
    q1 = "hello my name is mark"
    q2 = "my favorite animal is the cat"
    q3 = "my favorite food is candy"
    q4 = "can you tell me about myself?"
    print(chat.send_message([q1, q2, q3, q4]))


generate()
