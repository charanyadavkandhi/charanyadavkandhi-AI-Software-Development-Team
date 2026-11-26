import os
import json
import re
import requests
from backend.config import Config

class BaseAgent:
    """Base Agent class providing LLM calling, JSON extraction, and fallback logic."""

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.api_key = Config.GEMINI_API_KEY or Config.OPENAI_API_KEY

    def call_llm(self, user_prompt: str, json_schema_hint: str = "") -> str:
        """Call either Gemini API, OpenAI API, or fallback to smart synthesis engine."""
        combined_prompt = f"{self.system_prompt}\n\nTask:\n{user_prompt}"
        if json_schema_hint:
            combined_prompt += f"\n\nRespond ONLY with valid JSON matching this schema:\n{json_schema_hint}"

        # 1. Try Gemini API if key is present
        if Config.GEMINI_API_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=Config.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=combined_prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                # Fallback to direct REST API if SDK has any quirks
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.GEMINI_MODEL}:generateContent?key={Config.GEMINI_API_KEY}"
                    payload = {"contents": [{"parts": [{"text": combined_prompt}]}]}
                    resp = requests.post(url, json=payload, timeout=30)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as inner_e:
                    print(f"[{self.name}] Gemini API error: {inner_e}")

        # 2. Try OpenAI API if key is present
        if Config.OPENAI_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": Config.OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.3
                }
                resp = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"[{self.name}] OpenAI API error: {e}")

        # 3. Fallback Smart Synthesis Engine
        return self.smart_fallback(user_prompt)

    def extract_json(self, raw_text: str) -> dict:
        """Extract and parse JSON from markdown code fences or raw text."""
        try:
            # Clean markdown code blocks ```json ... ```
            cleaned = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
            cleaned = re.sub(r"^```\s*$", "", cleaned, flags=re.MULTILINE).strip()
            
            # Find the outer JSON object
            match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(cleaned)
        except Exception as e:
            # If parsing fails, create a structured wrapper
            return {
                "error": "Failed to parse strict JSON",
                "raw_content": raw_text
            }

    def smart_fallback(self, user_prompt: str) -> str:
        """Override in child classes to supply intelligent generative defaults."""
        return json.dumps({"status": "completed", "agent": self.name})
