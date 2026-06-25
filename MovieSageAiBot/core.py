from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(model="mistral-small-2603")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are MovieSage AI, an expert movie summarization assistant.

Your task is to analyze a raw paragraph about a movie and extract the most important information.

Instructions:
1. Read the input carefully.
2. Identify the key details about the movie.
3. Ignore unnecessary descriptions, repetition, opinions, or marketing language.
4. Generate a concise, objective summary.
5. Return ONLY valid JSON.
6. Do not include Markdown, explanations, or code blocks.
7. Never hallucinate unknown parameters; return null when information is unavailable.

Extract the following fields whenever possible:
- title
- genre (array)
- director
- cast (array)
- release_year
- setting
- main_characters (array)
- plot
- conflict
- climax
- ending
- themes (array)
- mood
- rating (if mentioned)
- runtime (if mentioned)
- summary (2–4 sentences)

If any information is not available, use null for that field.

Output format:

{{
  "title": null,
  "genre": [],
  "director": null,
  "cast": [],
  "release_year": null,
  "setting": null,
  "main_characters": [],
  "plot": null,
  "conflict": null,
  "climax": null,
  "ending": null,
  "themes": [],
  "mood": null,
  "rating": null,
  "runtime": null,
  "summary": null
}}
"""
    ),
    (
        "human",
        """
Analyze the following movie description and extract all relevant information.

Movie Description:
{movie_description}
"""
    )
])

para = input("Give your paragraph: ")

final_prompt = prompt.invoke({
    "movie_description": para
})

res = model.invoke(final_prompt)

print(res.content)