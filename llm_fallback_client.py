
import json
import os
import re
from typing import Optional
from openai import OpenAI as OpenAIClient
import google.generativeai as genai

class LLMFallbackClient:
    def extract_text(self, llm_result: dict) -> str:
        """
        Extract plain string from LLM result dict for embedding/model.encode.
        """
        text = llm_result.get("result", "")
        if not isinstance(text, str):
            text = str(text)
        return text
    """
    A multi-provider merge agent. Tries OpenAI, then Gemini, then a deterministic fallback.

    It reads API keys from `api_keys.txt` by default. You can pass a custom path.
    """

    def ask(self, user_prompt: str, code: str, program: str = "COBOL") -> dict:
        """
        Try OpenAI first, fall back to Gemini if OpenAI fails or quota exceeded. Returns extracted business rules/requirements.
        """
        try:
            result = self._try_openai(user_prompt, code, program)
            # Check for OpenAI quota error
            error_msg = str(result.get("error", ""))
            if result.get("success"):
                return result
            elif "429" in error_msg or "insufficient_quota" in error_msg:
                print(f"[LLMFallbackClient] OpenAI quota exceeded, trying Gemini...")
                try:
                    result = self._try_gemini(user_prompt, code, program)
                    return result
                except Exception as e:
                    print(f"[LLMFallbackClient] Gemini exception: {e}")
                    return {"success": False, "error": f"Gemini failed after OpenAI quota error: {e}"}
            else:
                print(f"[LLMFallbackClient] OpenAI failed: {result.get('error')}")
        except Exception as e:
            print(f"[LLMFallbackClient] OpenAI exception: {e}")
        # Fallback to Gemini for any other error
        try:
            result = self._try_gemini(user_prompt, code, program)
            return result
        except Exception as e:
            print(f"[LLMFallbackClient] Gemini exception: {e}")
            return {"success": False, "error": f"Both providers failed: {e}"}

    @staticmethod
    def load_api_keys(path: str = "llm_config.json") -> dict:
        """Load API keys from a small config file (JSON or key=value lines).
        Handles both absolute and relative paths. Adds debug prints for diagnostics.
        """
        config_path = "llm_config.json"
        if not os.path.exists(config_path):
            print(f"[load_api_keys] No llm_config.json found at {config_path}")
            return {}
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                txt = fh.read().strip()
                if not txt:
                    print(f"[load_api_keys] File {config_path} is empty.")
                    return {}
                try:
                    keys = json.loads(txt)
                    print(f"[load_api_keys] Loaded keys from JSON in {config_path}: {list(keys.keys())}")
                    return keys
                except Exception as e:
                    print(f"[load_api_keys] Error parsing JSON in {config_path}: {e}")
                    return {}
        except Exception as e:
            print(f"[load_api_keys] Error reading {config_path}: {e}")
            return {}

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_keys_path: str = "api_keys.txt", provider_priority=None):
        self.model_name = model_name
        self.api_keys = self.load_api_keys(api_keys_path)
        # Always try OpenAI first, then Gemini
        self.provider_priority = ["openai", "gemini"]

    def _try_openai(self, user_prompt: str, code: str, program: str = "COBOL") -> dict:
        """
        Call OpenAI LLM with a user prompt, code, and program name. Returns extracted business rules/requirements.
        """
        if OpenAIClient is None:
            raise RuntimeError("openai python package not available")
        api_key = self.api_keys.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OpenAI API key not found in llm_config.json (use key 'OPENAI_API_KEY')")
        client = OpenAIClient(api_key=api_key)
        # Compose prompt for business rule extraction
        prompt = (
            f"{user_prompt}\n\nProgram Language: {program}\n\nCode:\n{code}\n"
        )
        try:
            resp = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            content = resp.choices[0].message.content
            return {"success": True, "provider": "openai", "result": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _try_gemini(self, user_prompt: str, code: str, program: str = "COBOL") -> dict:
        """
        Call Gemini LLM with a user prompt, code, and program name. Returns extracted business rules/requirements.
        """
        if genai is None:
            raise RuntimeError("google.generativeai package not available")
        api_key = self.api_keys.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Gemini API key not found in llm_config.json (use key 'GEMINI_API_KEY')")
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        # Compose prompt for business rule extraction
        prompt = (
            f"{user_prompt}\n\nProgram Language: {program}\n\nCode:\n{code}\n"
        )
        try:
            if hasattr(genai, "GenerativeModel"):
                model = genai.GenerativeModel(model_name="gemini-2.0-flash")
                resp = model.generate_content(prompt)
            else:
                print("[Gemini Diagnostic] google.generativeai attributes:", dir(genai))
                raise RuntimeError(
                    "Gemini provider usage error: The expected GenerativeModel API is not available in your installed google-generativeai package. "
                    "Please check the printed attributes above and consult https://github.com/google/generative-ai-python for correct usage. "
                    "You may need to update the package or adjust the provider code to match your installed version."
                )
        except Exception as e:
            raise RuntimeError(f"Gemini request failed: {e}")

        content = None
        try:
            content = resp.candidates[0].content
        except Exception:
            try:
                content = resp.text
            except Exception:
                content = str(resp)
        return {"success": True, "provider": "gemini", "result": content}
        
