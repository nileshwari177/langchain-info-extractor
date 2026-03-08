from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

import os

load_dotenv()

from langchain_mistralai import ChatMistralAI

model=ChatMistralAI(model='mistral-small-2506')   

prompt=ChatPromptTemplate.from_messages([
    ("system", """You are an intelligent information extraction assistant.

Your task is to read the paragraph carefully and extract the most useful information from it.

Extract the following details if they are present:
- Movie Name
- Director
- Release Year
- Genre
- Main Cast
- Plot / Story Overview
- Key Themes
- Rating
- Music / Soundtrack Composer
- Notable Features (visuals, awards, scientific accuracy, etc.)

After extracting the information, also generate a **short summary (2–3 sentences)** of the paragraph.

Instructions:
- Only extract information that exists in the paragraph.
- If some information is missing, write "Not Mentioned".
- Keep the response clean and structured.

Paragraph:
{paragraph}

Return the result in the following format:

Movie Name:
Director:
Release Year:
Genre:
Main Cast:
Plot / Story Overview:
Key Themes:
Rating:
Soundtrack Composer:
Notable Features:

Short Summary:"""
     ),
    ("human", """ Extract information from the following paragraph:

{paragraph}""")

])

para=input("Enter a paragraph about a movie: ")
final_prompt=prompt.invoke({"paragraph": para})

response = model.invoke(final_prompt)
print(response.content)
