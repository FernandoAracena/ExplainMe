from flask import Flask, render_template, request
from functions.article_processing import download_and_parse, process_chunks
from functions.summaries_translator import translate_summaries

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the URL from the form input
        url = request.form['url']

        # Download the webpage and parse it with BeautifulSoup
        content = download_and_parse(url)

        # Process the content into chunks and summaries
        summaries = process_chunks(content)

        translated_summaries = translate_summaries(summaries)

        return render_template('upload.html', summary=translated_summaries)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
