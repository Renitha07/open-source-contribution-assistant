import logging
import time
from config.llm import get_llm, MODEL_NAME
from openai import RateLimitError, APITimeoutError, APIConnectionError

logger = logging.getLogger(__name__)

client = get_llm()

MAX_RETRIES = 3
BASE_DELAY = 2.0
RETRYABLE_ERRORS = (RateLimitError, APITimeoutError, APIConnectionError)


def invoke_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Invoke LLM with retry logic and structured logging.
    
    Args:
        system_prompt: System message for the LLM
        user_prompt: User message for the LLM
        
    Returns:
        LLM response content as string
        
    Raises:
        Exception: If all retries exhausted
    """
    last_exception = None
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"LLM call attempt {attempt + 1}/{MAX_RETRIES}")
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                timeout=120.0,
            )
            
            content = response.choices[0].message.content
            
            if not content or not content.strip():
                raise ValueError("Empty response from LLM")
                
            logger.debug(f"LLM call successful, response length: {len(content)}")
            return content.strip()
            
        except RETRYABLE_ERRORS as e:
            last_exception = e
            delay = BASE_DELAY * (2 ** attempt)
            logger.warning(f"LLM call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {delay}s...")
            time.sleep(delay)
            
        except Exception as e:
            logger.error(f"LLM call failed with non-retryable error: {e}")
            raise
    
    logger.error(f"All {MAX_RETRIES} LLM call attempts failed")
    raise last_exception or Exception("LLM call failed after retries")