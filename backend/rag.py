import os
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, build_user_prompt
from elastic import es_client

class RAGPipeline:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                system_instruction=SYSTEM_PROMPT
            )
        else:
            print("WARNING: GEMINI_API_KEY not found. Using direct formatter (no LLM).")
            self.model = None

    def query(self, user_query: str) -> str:
        # Step 1: Retrieve context from Elasticsearch
        results = es_client.search(user_query, top_k=1)
        context = results[0] if results else {}

        # Step 2: Build prompt
        prompt = build_user_prompt(user_query, context)

        # Step 3: Call LLM or fall back to direct formatting
        if self.model:
            response = self.model.generate_content(prompt)
            return response.text
        else:
            if not context:
                return "I'm sorry, I could not find official information for this service in the currently indexed database."
            
            return f"""Service:
{context.get('service_name')}

Department:
{context.get('department')}

Eligibility:
{context.get('eligibility')}

Required Documents:
{chr(10).join(['• ' + doc for doc in context.get('required_documents', [])])}

Fees:
{context.get('fees')}

Processing Time:
{context.get('processing_time')}

How to Apply:
{chr(10).join(context.get('how_to_apply', []))}

Official Source:
{context.get('official_source')}"""

rag_pipeline = RAGPipeline()
