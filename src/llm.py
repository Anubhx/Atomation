import time
import logging
from typing import Optional, Dict, Any
from src.config import DEFAULT_GENERATION_MODEL, MAX_RETRIES
from src.key_pool import KeyPool

logger = logging.getLogger("llm")

class GeminiClient:
    def __init__(
        self,
        key_pool: Optional[KeyPool] = None,
        model_name: str = DEFAULT_GENERATION_MODEL,
        local_only: bool = False
    ):
        self.key_pool = key_pool or KeyPool()
        self.model_name = model_name
        self.local_only = local_only

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sends generation request to Gemini API with KeyPool failover and retry logic.
        Returns dict with:
        - "text": generated response
        - "success": bool
        - "slot_name": masked key slot name used
        - "error": optional error message
        """
        if self.local_only:
            return {
                "text": "⚠️ **Local-Only Mode Enabled**: Gemini API calls are disabled. Showing retrieved local knowledge only.",
                "success": False,
                "slot_name": "None (Local Only)",
                "error": "Local-Only Mode"
            }

        if not self.key_pool.has_keys:
            return {
                "text": "⚠️ **No Gemini API Key Configured**: Please configure your API key in `.streamlit/secrets.toml` or environment variable `GEMINI_API_KEY`.",
                "success": False,
                "slot_name": "None",
                "error": "Missing API Key"
            }

        retries = 0
        last_error = ""

        while retries < MAX_RETRIES:
            slot = self.key_pool.get_available_key()
            if not slot:
                return {
                    "text": "⚠️ **All Gemini API Keys in Cooldown**: Rate limit reached across key pool. Please wait a few seconds and try again.",
                    "success": False,
                    "slot_name": "All in Cooldown",
                    "error": "Key Pool Cooldown"
                }

            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=slot.key_str)
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    system_instruction=system_instruction
                )

                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )

                if hasattr(response, "text") and response.text:
                    self.key_pool.mark_healthy(slot.slot_id)
                    return {
                        "text": response.text,
                        "success": True,
                        "slot_name": slot.get_masked_name(),
                        "error": None
                    }
                else:
                    last_error = "Empty response from Gemini API"
                    self.key_pool.mark_failed(slot.slot_id)

            except Exception as e:
                err_msg = str(e)
                last_error = err_msg
                logger.warning(f"Gemini API call failed on {slot.get_masked_name()}: {err_msg}")

                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                    self.key_pool.mark_rate_limited(slot.slot_id)
                elif "401" in err_msg or "403" in err_msg or "invalid" in err_msg.lower():
                    self.key_pool.disable_slot(slot.slot_id)
                else:
                    self.key_pool.mark_failed(slot.slot_id)

            retries += 1
            time.sleep(1.0 * retries)

        return {
            "text": f"❌ **Gemini API Error**: Request failed after {MAX_RETRIES} attempts. Last error: `{last_error}`",
            "success": False,
            "slot_name": "Failed",
            "error": last_error
        }
