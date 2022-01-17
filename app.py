import nltk
from nltk import *
from nltk.corpus import wordnet
import json 
from rake_nltk import Rake
from flask import Flask, render_template, request

rake_nltk_var = Rake()
app = Flask(__name__)
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('punkt')
#installation command: python -m nltk.downloader punkt
def process(word):
    def get_key_words(text):
        rake_nltk_var.extract_keywords_from_text(text)
        keyword_extracted = rake_nltk_var.get_ranked_phrases()
        return keyword_extracted

    def get_alt_word(word):
        alt_word = []
        for ss in wordnet.synsets(word):
            alt_word = ss.lemma_names()
            break
        if len(alt_word)==0:
            return word
        for i in alt_word:
            if i!=word:
                return i 
        return word

    words_list = get_key_words(word)
    print(words_list)
    arr = []
    for i in words_list:
        get_alt = get_alt_word(i)
        if i!=get_alt:
            arr.append(get_alt)
            word = word.replace(i, f'<mark style="background-color: #B4D5FF;">{get_alt.strip()}</mark>')
        else:
            word = word.replace(i, get_alt)
    final = [word, arr]
    return final

"""
Test Output:
Initial Input:
Learn to ship software like a pro. There's no substitute for hands-on experience. But for most students, real world tools can be cost-prohibitive. That's why we created the GitHub Student Developer Pack with some of our partners and friends

Final Output:
Learn to ship software like a professional. There's no replacement for custody-on experience. But for most student, real world tools can be cost-professionalhibitory. That's why we make the GitHub Student Developer Pack with some of our spouse and friend
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="POST":
        original = request.form.get('fname')
        converted = process(original)
        print(original)
        return render_template("index.html", txt1=original, txt2=converted[0],indices=converted[1])
    return render_template("index.html", txt1="", txt2="")
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)