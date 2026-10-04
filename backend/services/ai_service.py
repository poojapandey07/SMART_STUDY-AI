import json
import requests
from backend.config import Config

class AIService:
    """Intelligent educational AI assistant for college student learning."""

    @staticmethod
    def _call_gemini_api(prompt: str, system_instruction: str = "") -> str:
        """Call Google Gemini REST API using AI_API_KEY."""
        api_key = Config.AI_API_KEY
        if not api_key:
            return ""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.AI_MODEL}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"SYSTEM INSTRUCTIONS:\n{system_instruction}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will provide clear, concise, student-friendly explanations."}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        payload = {"contents": contents}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except Exception as e:
            print(f"[AIService] Gemini API error: {e}")
        return ""

    @staticmethod
    def _call_openai_api(prompt: str, system_instruction: str = "") -> str:
        """Call OpenAI REST API using AI_API_KEY."""
        api_key = Config.AI_API_KEY
        if not api_key:
            return ""

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"[AIService] OpenAI API error: {e}")
        return ""

    @classmethod
    def get_ai_response(cls, prompt: str, system_instruction: str = "") -> str:
        """Fetch AI response from configured provider or return empty string to trigger fallback."""
        if Config.AI_API_KEY:
            if Config.AI_PROVIDER == "openai":
                res = cls._call_openai_api(prompt, system_instruction)
                if res:
                    return res
            else:
                res = cls._call_gemini_api(prompt, system_instruction)
                if res:
                    return res
        return ""

    @classmethod
    def chat(cls, message: str, subject: str = "General", mode: str = "socratic") -> dict:
        """Generate conversational AI response for student queries."""
        sys_inst = (
            f"You are SmartStudy AI, a helpful, concise college study mentor. "
            f"Subject: {subject}. Keep responses natural, direct, and under 150 words. "
            "Use simple formatting, avoid long lectures, and highlight key concepts clearly."
        )
        
        raw_ai = cls.get_ai_response(message, sys_inst)
        if raw_ai:
            return {
                "message": raw_ai,
                "subject": subject,
                "source": Config.AI_PROVIDER
            }

        return cls._generate_fallback_chat(message, subject)

    @classmethod
    def explain(cls, topic: str, subject: str = "General") -> dict:
        """Provide simple explanation, examples, and key points for a topic."""
        prompt = (
            f"Explain the topic '{topic}' in '{subject}' simply. "
            "Respond in JSON with keys: 'simple_explanation', 'examples' (list of strings), 'key_points' (list of strings)."
        )
        
        raw_ai = cls.get_ai_response(prompt)
        if raw_ai:
            try:
                cleaned = raw_ai.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(cleaned)
                return {
                    "topic": topic,
                    "subject": subject,
                    "simple_explanation": parsed.get("simple_explanation", ""),
                    "examples": parsed.get("examples", []),
                    "key_points": parsed.get("key_points", []),
                    "source": Config.AI_PROVIDER
                }
            except Exception:
                pass

        return cls._generate_fallback_explanation(topic, subject)

    @classmethod
    def notes(cls, topic: str, subject: str = "General") -> dict:
        """Generate concise revision notes for a topic."""
        prompt = f"Create concise high-yield bulleted revision notes for '{topic}' in '{subject}'. Keep it clean and exam-focused."
        raw_ai = cls.get_ai_response(prompt)
        
        if raw_ai:
            return {
                "topic": topic,
                "subject": subject,
                "notes": raw_ai,
                "source": Config.AI_PROVIDER
            }

        return cls._generate_fallback_notes(topic, subject)

    # --------------------------------------------------------------------------
    # Human-like educational fallback responses
    # --------------------------------------------------------------------------
    @staticmethod
    def _generate_fallback_chat(message: str, subject: str) -> dict:
        msg_lower = message.lower()
        
        if "array" in msg_lower or "explain arrays" in msg_lower:
            return {
                "message": (
                    "**Arrays** are like a numbered row of lockers in your college hallway:\n\n"
                    "• **Contiguous Memory**: Every locker sits right next to the previous one.\n"
                    "• **Instant Access `O(1)`**: If you know the index (locker #3), you can jump straight to it without checking #1 or #2.\n"
                    "• **Insertion/Deletion `O(n)`**: Inserting an item in the middle requires shifting every locker to the right.\n\n"
                    "**Example**: `scores = [85, 92, 78]` -> `scores[0]` is `85` in constant time."
                ),
                "subject": subject,
                "source": "smartstudy_engine"
            }
        
        if "normalization" in msg_lower or "dbms" in msg_lower:
            return {
                "message": (
                    "**Database Normalization** is organizing tables to eliminate data redundancy and prevent update anomalies:\n\n"
                    "• **1NF**: Atomic values only (no lists inside cells), unique rows.\n"
                    "• **2NF**: In 1NF + no partial dependency on a composite key.\n"
                    "• **3NF**: In 2NF + no transitive dependency (non-key attribute determining another non-key attribute).\n\n"
                    "💡 **Student Tip**: Remember 'Every non-key attribute must depend on the key, the whole key, and nothing but the key'."
                ),
                "subject": subject,
                "source": "smartstudy_engine"
            }

        if "process scheduling" in msg_lower or "round robin" in msg_lower or "os" in msg_lower:
            return {
                "message": (
                    "**OS Process Scheduling** decides which program gets CPU time:\n\n"
                    "• **FCFS (First-Come, First-Served)**: Simple queue, but can suffer from convoy effect.\n"
                    "• **SJF (Shortest Job First)**: Optimal average waiting time, but requires knowing burst time in advance.\n"
                    "• **Round Robin (RR)**: Each process gets a fixed time slice (quantum), ensuring fair responsiveness in interactive operating systems."
                ),
                "subject": subject,
                "source": "smartstudy_engine"
            }

        if "example" in msg_lower:
            return {
                "message": (
                    f"Here is a quick practical example for **{subject}**:\n\n"
                    "```python\n"
                    "# Practical implementation example\n"
                    "def find_maximum(numbers):\n"
                    "    max_val = numbers[0]\n"
                    "    for num in numbers[1:]:\n"
                    "        if num > max_val:\n"
                    "            max_val = num\n"
                    "    return max_val\n"
                    "```\n"
                    "This scans the array in linear time `O(n)` with `O(1)` space."
                ),
                "subject": subject,
                "source": "smartstudy_engine"
            }

        return {
            "message": (
                f"Regarding **{message}** in {subject}:\n\n"
                "1. **Core Concept**: Break down the problem into input, state transition, and expected output.\n"
                "2. **Common Trap**: Watch out for off-by-one errors and edge cases (like empty collections or null references).\n\n"
                "Ask me if you'd like a short code example, revision notes, or a practice question!"
            ),
            "subject": subject,
            "source": "smartstudy_engine"
        }

    @staticmethod
    def _generate_fallback_explanation(topic: str, subject: str) -> dict:
        return {
            "topic": topic,
            "subject": subject,
            "simple_explanation": f"{topic} is an essential concept in {subject} used to structure logic and solve computational problems efficiently.",
            "examples": [
                f"Standard implementation of {topic} in everyday coding assignments",
                f"Tracing state transitions step-by-step with sample input values"
            ],
            "key_points": [
                "Understand the time and space complexity trade-offs.",
                "Review edge cases: empty inputs, single element, boundary values.",
                "Practice active recall by writing out the algorithm or proof from memory."
            ],
            "source": "smartstudy_engine"
        }

    @staticmethod
    def _generate_fallback_notes(topic: str, subject: str) -> dict:
        return {
            "topic": topic,
            "subject": subject,
            "notes": (
                f"# 📝 Quick Revision Notes: {topic}\n"
                f"**Subject:** {subject}\n\n"
                f"## 1. Key Definition\n"
                f"• {topic} provides the theoretical framework for organizing and processing data in {subject}.\n\n"
                f"## 2. Important Principles\n"
                f"• Time Complexity: Understand best, average, and worst-case behavior.\n"
                f"• Space Complexity: Check whether auxiliary memory is required.\n\n"
                f"## 3. Exam Checklist\n"
                f"• Can you explain {topic} in 2 sentences without notes?\n"
                f"• Can you draw a trace diagram or write the core function?\n"
            ),
            "source": "smartstudy_engine"
        }
