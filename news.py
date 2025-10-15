from flask import Flask, jsonify
import requests
import re

app= Flask(__name__)

def fetch_top_stories():
    URL="https://time.com/section/world/"
    headers ={ "User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64)"}
    html= requests.get(URL,headers = headers).text

    article_blocks= re.findall(r"<article.*?</article>", html, re.DOTALL)
    top_stories= []
    for i, article in enumerate(article_blocks[:6], 1):
        
        title_match = re.search(
            r'<a[^>]*href="([^"]+)"[^>]*>\s*<span>(.*?)</span>',
            article,
            re.DOTALL
        )
        author_match = re.search(
            r'<p[^>]*>\s*by\s*(?:<!--\s*-->)?\s*([^<]+)</p>',
            article,
            re.DOTALL | re.IGNORECASE
        )
        if not title_match:
            continue

        link, title = title_match.groups()
        link = f"https://time.com{link}" if link.startswith("/") else link
        title = re.sub(r"<.*?>", "", title).strip()
        author = author_match.group(1).strip() if author_match else "Unknown"

        top_stories.append({
            "rank": i,
            "title": title,
            "author": author,
            "url": link,
            "section": "World"
        })
    return {"top_stories": top_stories}
@app.route("/", methods=["GET"])
def top_news():
    try:
        data = fetch_top_stories()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)
