import re
from readability import Document
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


def get_index(list, index, default=None):
    try:
        if list == {}:
            return default
        return list[index]
    except IndexError:
        return default

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///search_results.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class SearchResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(350), nullable=False)
    title = db.Column(db.String(650))
    short_desc = db.Column(db.String(1000))
    full_text = db.Column(db.String(5000))
    date = db.Column(db.String(100))
    author = db.Column(db.String(250))
    keywords = db.Column(db.String(1000))

    # def __repr__(self):
    #     return f"{self.url} - {self.full_text}"


@app.route('/')
def root():
    # Clearing database
    db_rows = SearchResults()
    db_rows.query.delete()
    db.session.commit()
    return render_template('index.html')


@app.route('/harvest', methods=["Post"])
def harvest():
    id = request.form['se_id']
    key = request.form['api_key']
    urls = request.form['urls']
    keywords = request.form['keywords']
    idx = request.form['index']
    # date = request.form['date']
    # author = request.form['author']

    hasNextPage = True
    currentResults = 10
    page = 10

    while (hasNextPage):
        print("NextPage----> ",hasNextPage,"page------->,",page)

        api_url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={id}&q={keywords}&start={page}"
        # api_url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={id}&q={keywords}&start={page}&siteSearch={urls}"
        data = requests.get(api_url).json()
        print(data.get('queries',{}))

        if isinstance(data.get('error'), dict):
            error = data.get('error', {}).get('message')
            return render_template('index.html', error=error)

        else:
            totalResults = int(get_index(data.get('queries', {}).get('nextPage'), 0).get('totalResults'))
            for search_item in data.get("items", {}):
                url = search_item.get('link')
                title = search_item.get("title")
                shortDesc = search_item.get('snippet')
                date = get_index(search_item.get('pagemap', {}).get('metatags', {}), 0, {}).get('article:published_time')
                author = get_index(search_item.get('pagemap', {}).get('metatags', {}), 0, {}).get('article:publisher')
                response = requests.get(url)
                if response.status_code == 200:
                    full_text = cleanhtml(Document(response.text).summary())
                else:
                    full_text = ""
                results = SearchResults(url=url, title=title, short_desc=shortDesc,
                                        full_text=full_text, date=date, author=author, keywords='')
                db.session.add(results)
                db.session.commit()
            currentResults += len(data.get("items", {}))
            page += 90
            if currentResults > totalResults or page >= 100:
                hasNextPage = False
    return redirect(url_for('results',url=urls,keywords=keywords,idx=idx))


@app.route('/results')
def results():
    db_rows = SearchResults()
    data = db_rows.query.all()
    arr = []
    url = request.args["url"]  # counterpart for url_for()
    keyword = request.args["keywords"]  # counterpart for url_for()
    idx = request.args["idx"]  # counterpart for url_for()
    for row in data:
        item = dict()
        item['url'] = row.url[:50]
        item['title'] = row.title
        item['short_desc'] = row.short_desc
        item['full_text'] = row.full_text[:250]
        item['date'] = row.date
        item['author'] = row.author[:50] if row.author else ''
        item['keywords'] = row.keywords[:50]
        arr.append(item)
    return render_template('results.html', data=arr, target_url= url, keyword=keyword, tool=idx)


if __name__ == "__main__":
    app.run(debug=True)
