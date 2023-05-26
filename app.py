from flask import Flask, render_template, request
from functions.article_processing import download_and_parse, process_chunks
from functions.summaries_translator import translate_summaries
import openai

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url.strip() == '':
            return render_template('index.html', explainme_error='URL field cannot be empty.')

        if 'language' in request.form:
            # Translation request
            selected_language = request.form['language']
            if url.strip() == '':
                return render_template('upload.html', translate_error='URL field cannot be empty.')

            try:
                content = download_and_parse(url)
                summaries = process_chunks(content)
                translated_summaries = translate_summaries(
                    summaries, selected_language)
                return render_template('upload.html', summary=translated_summaries, url=url)
            except Exception as e:
                return render_template('upload.html', explainme_error=str(e))

    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    url = request.form['url']
    if url.strip() == '':
        return render_template('upload.html', explainme_error='URL field cannot be empty.')

    try:
        content = download_and_parse(url)
        summaries = process_chunks(content)
        return render_template('upload.html', summary=summaries, url=url, translate_error=None)
    except Exception as e:
        return render_template('upload.html', explainme_error=str(e))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
