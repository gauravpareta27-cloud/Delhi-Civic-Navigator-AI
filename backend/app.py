# -*- coding: utf-8 -*-
"""
Delhi Civic Navigator AI - Backend Server
Built with Python's built-in http.server (zero heavy dependencies!)
Works on Python 3.14+ without needing Rust/MSVC compilers.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import os
import sys
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env
load_dotenv()

# ── Elasticsearch Client ──────────────────────────────────────────────────────
def build_es_client():
    try:
        from elasticsearch import Elasticsearch
        url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
        api_key = os.getenv("ELASTICSEARCH_API_KEY")
        if api_key:
            client = Elasticsearch(url, api_key=api_key)
        else:
            client = Elasticsearch(url)
        # Test connection
        info = client.info()
        print(f"[ES] Connected to Elastic Cloud: {info['cluster_name']}")
        return client
    except Exception as e:
        print(f"[WARNING] Elasticsearch not available, using BM25 fallback. ({type(e).__name__}: {e})")
        return None


# ── BM25 Fallback (pure Python, no compilation needed) ───────────────────────
class BM25:
    """Pure-Python BM25 retrieval — no external packages needed."""
    def __init__(self, corpus):
        import math
        self.corpus = corpus
        self.avgdl = sum(len(d) for d in corpus) / max(len(corpus), 1)
        self.k1, self.b = 1.5, 0.75
        self.idf = {}
        N = len(corpus)
        from collections import Counter
        for doc in corpus:
            for term in set(doc):
                self.idf[term] = self.idf.get(term, 0) + 1
        self.idf = {t: math.log((N - f + 0.5) / (f + 0.5) + 1)
                    for t, f in self.idf.items()}

    def score(self, query_terms, doc):
        from collections import Counter
        tf = Counter(doc)
        score = 0
        for term in query_terms:
            if term not in tf:
                continue
            idf = self.idf.get(term, 0)
            f = tf[term]
            score += idf * (f * (self.k1 + 1)) / (
                f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
        return score

    def get_top_k(self, query_terms, k=1):
        scores = [(i, self.score(query_terms, doc)) for i, doc in enumerate(self.corpus)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [i for i, s in scores[:k] if s > 0]

def tokenize(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation)).split()

# ── Load Data ─────────────────────────────────────────────────────────────────
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'data', 'government_docs', 'services.json')
with open(data_path, 'r', encoding='utf-8') as f:
    DOCUMENTS = json.load(f)

# Build BM25 index
corpus_tokens = []
for doc in DOCUMENTS:
    text = f"{doc['service_name']} {doc['department']} {doc['eligibility']} {' '.join(doc['required_documents'])}"
    corpus_tokens.append(tokenize(text))
bm25 = BM25(corpus_tokens)

# Try Elasticsearch, fall back to BM25
es = build_es_client()
ES_INDEX = "delhi_services"

def index_to_elasticsearch():
    if not es:
        return
    try:
        if not es.indices.exists(index=ES_INDEX):
            es.indices.create(index=ES_INDEX, body={
                "mappings": {"properties": {
                    "service_name": {"type": "text"},
                    "department":   {"type": "text"},
                    "eligibility":  {"type": "text"},
                    "required_documents": {"type": "text"},
                    "fees":             {"type": "text"},
                    "processing_time":  {"type": "text"},
                    "how_to_apply":     {"type": "text"},
                    "official_source":  {"type": "keyword"}
                }}
            })
        from elasticsearch.helpers import bulk
        actions = [{"_index": ES_INDEX, "_id": i, "_source": doc}
                   for i, doc in enumerate(DOCUMENTS)]
        bulk(es, actions)
        es.indices.refresh(index=ES_INDEX)
        print(f"[ES] Indexed {len(DOCUMENTS)} documents into '{ES_INDEX}' index successfully.")
    except Exception as e:
        print(f"[WARNING] Elasticsearch not available, using BM25 fallback. ({type(e).__name__})")

def search(query, top_k=1):
    """Search Elasticsearch first, fall back to BM25."""
    if es:
        try:
            resp = es.search(index=ES_INDEX, body={
                "query": {"multi_match": {
                    "query": query,
                    "fields": ["service_name^3", "department^2", "eligibility",
                               "required_documents", "how_to_apply"],
                    "fuzziness": "AUTO"
                }},
                "size": top_k
            })
            hits = [h["_source"] for h in resp["hits"]["hits"]]
            if hits:
                return hits
        except Exception:
            pass
    # BM25 fallback
    q_tokens = tokenize(query)
    idxs = bm25.get_top_k(q_tokens, k=top_k)
    return [DOCUMENTS[i] for i in idxs]

# ── Gemini LLM ────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AI assistant for the Delhi Civic Navigator.
Respond ONLY in this exact structure:

Service:
[name]

Department:
[dept]

Eligibility:
[who can apply]

Required Documents:
• [doc1]
• [doc2]

Fees:
[fees]

Processing Time:
[time]

How to Apply:
Step 1: ...
Step 2: ...

Official Source:
[URL]
"""

def ask_gemini(query, context):
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash",
                                       system_instruction=SYSTEM_PROMPT)
        prompt = f"User query: {query}\n\nContext:\n{json.dumps(context, indent=2)}"
        return model.generate_content(prompt).text
    except Exception as e:
        print(f"Gemini fallback: {e}")
        return None

def format_response(ctx):
    """Direct formatter — used when Gemini API key is missing."""
    if not ctx:
        return "I'm sorry, I could not find information for that service."
    nl = "\n"
    return f"""Service:
{ctx.get('service_name', 'N/A')}

Department:
{ctx.get('department', 'N/A')}

Eligibility:
{ctx.get('eligibility', 'N/A')}

Required Documents:
{nl.join('• ' + d for d in ctx.get('required_documents', []))}

Fees:
{ctx.get('fees', 'N/A')}

Processing Time:
{ctx.get('processing_time', 'N/A')}

How to Apply:
{nl.join(ctx.get('how_to_apply', []))}

Official Source:
{ctx.get('official_source', 'N/A')}"""

# ── HTTP Handler ──────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json(200, {"status": "healthy", "documents_indexed": len(DOCUMENTS)})
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/search":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            query = body.get("query", "").strip()
            if not query:
                self.send_json(400, {"error": "Query cannot be empty"})
                return
            results = search(query)
            context = results[0] if results else {}
            response_text = ask_gemini(query, context) or format_response(context)
            self.send_json(200, {"response": response_text})
        else:
            self.send_json(404, {"error": "Not found"})

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    index_to_elasticsearch()
    port = int(os.getenv("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"\nDelhi Civic Navigator backend running on http://localhost:{port}")
    print(f"   Health check: http://localhost:{port}/api/health")
    print(f"   Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
