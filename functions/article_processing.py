import requests
from bs4 import BeautifulSoup
import newspaper
import openai
from secret.keys import API_KEY


def download_and_parse(url):
    # Download the webpage and parse it with BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the article content
    article = newspaper.Article(url)
    article.download()
    article.parse()
    content = article.text

    return content


def process_chunks(content):
    # Authenticate with OpenAI API and summarize the article
    openai.api_key = API_KEY

    # Split the input text into smaller chunks and process each chunk separately
    text_chunks = [content[i:i+4096] for i in range(0, len(content), 4096)]
    summaries = []
    for chunk in text_chunks:
        prompt = f"Please summarize the following article:\n{chunk}\n\nSummary:"
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300,
        )
        summary = completions.choices[0].text.strip()
        summaries.append(summary)

    return summaries
