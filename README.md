# 🎬 CineSage - Movie Information Extractor

## Overview
A Streamlit application that extracts structured movie information from a free-text paragraph using LangChain, Mistral AI, and Pydantic.

## Features
- Extracts movie title
- Director
- Release year
- Genre
- Main cast
- Plot overview
- Key themes
- Rating (if available)
- Soundtrack composer
- Notable features

## Tech Stack
- Python
- Streamlit
- LangChain
- Mistral AI
- Pydantic
- python-dotenv

## Project Structure
langchain-info-extractor/
├── app.py
├── CineSage/
│   └── core.py
├── requirements.txt
├── README.md
└── .env

## Installation
1. Clone the repository
2. Install dependencies
   pip install -r requirements.txt
3. Create a `.env` file
   MISTRAL_API_KEY=your_api_key
4. Run
   streamlit run app.py

## Example Input
(Provide a short movie paragraph)

## Example Output
(Provide a sample JSON or screenshot)

## Future Improvements
- Multiple LLM support
- Export to JSON
- Movie poster integration
- Batch extraction

