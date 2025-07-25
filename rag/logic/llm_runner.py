#!/usr/bin/env python3
"""
LLM Runner for Local Inference
==============================

Standalone LLM runner for generating answers from retrieved context.
Supports multiple local LLM backends.
"""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Try to import different LLM backends
try:
    from llama_cpp import Llama

    LLAMACPP_AVAILABLE = True
except ImportError:
    LLAMACPP_AVAILABLE = False
    logger.warning("llama-cpp-python not available")

try:
    import ollama

    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("ollama not available")

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("transformers not available")


class LLMRunner:
    """
    Local LLM runner for generating answers from context.
    """

    def __init__(
        self,
        model_type: str = "llama-cpp",
        model_path: str = "llm_weights/mistral-7b-instruct.Q4_K_M.gguf",
        model_name: str = "mistral",
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ):
        """
        Initialize the LLM runner.

        Args:
            model_type: Type of LLM backend ("llama-cpp", "ollama", "transformers")
            model_path: Path to the model file
            model_name: Name of the model for Ollama
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
        """
        self.model_type = model_type
        self.model_path = model_path
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

        self.model = None
        self.tokenizer = None

        # Initialize the model
        self._initialize_model()

        logger.info(f"🤖 LLM Runner initialized with {model_type}")
        logger.info(f"   Model: {model_path}")
        logger.info(f"   Max tokens: {max_tokens}")
        logger.info(f"   Temperature: {temperature}")

    def _initialize_model(self):
        """Initialize the LLM model based on the specified backend."""
        try:
            if self.model_type == "llama-cpp" and LLAMACPP_AVAILABLE:
                self._initialize_llama_cpp()
            elif self.model_type == "ollama" and OLLAMA_AVAILABLE:
                self._initialize_ollama()
            elif self.model_type == "transformers" and TRANSFORMERS_AVAILABLE:
                self._initialize_transformers()
            else:
                logger.warning(
                    f"Backend {self.model_type} not available, using fallback"
                )
                self.model_type = "fallback"

        except Exception as e:
            logger.error(f"Failed to initialize {self.model_type} model: {e}")
            self.model_type = "fallback"

    def _initialize_llama_cpp(self):
        """Initialize llama-cpp-python model."""
        if not os.path.exists(self.model_path):
            logger.warning(f"Model file not found: {self.model_path}")
            self.model_type = "fallback"
            return

        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=0,  # CPU only for now
            )
            logger.info("✅ llama-cpp model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load llama-cpp model: {e}")
            self.model_type = "fallback"

    def _initialize_ollama(self):
        """Initialize Ollama model."""
        try:
            # Check if model is available
            models = ollama.list()
            model_names = [model["name"] for model in models["models"]]

            if self.model_name not in model_names:
                logger.warning(
                    f"Ollama model {self.model_name} not found. Available: {model_names}"
                )
                self.model_type = "fallback"
                return

            logger.info("✅ Ollama model available")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            self.model_type = "fallback"

    def _initialize_transformers(self):
        """Initialize transformers model."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto" if torch.cuda.is_available() else "cpu",
            )
            logger.info("✅ Transformers model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load transformers model: {e}")
            self.model_type = "fallback"

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate an answer based on the question and context.

        Args:
            question: The user's question
            context: Retrieved context from documents

        Returns:
            Generated answer
        """
        if self.model_type == "fallback":
            return self._fallback_answer(question, context)

        try:
            if self.model_type == "llama-cpp":
                return self._generate_llama_cpp(question, context)
            elif self.model_type == "ollama":
                return self._generate_ollama(question, context)
            elif self.model_type == "transformers":
                return self._generate_transformers(question, context)
            else:
                return self._fallback_answer(question, context)

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._fallback_answer(question, context)

    def _generate_llama_cpp(self, question: str, context: str) -> str:
        """Generate answer using llama-cpp-python."""
        prompt = self._create_prompt(question, context)

        response = self.model(
            prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            stop=["</s>", "Human:", "Assistant:"],
        )

        return response["choices"][0]["text"].strip()

    def _generate_ollama(self, question: str, context: str) -> str:
        """Generate answer using Ollama."""
        prompt = self._create_prompt(question, context)

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "num_predict": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        )

        return response["response"].strip()

    def _generate_transformers(self, question: str, context: str) -> str:
        """Generate answer using transformers."""
        prompt = self._create_prompt(question, context)

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the prompt from the response
        return response[len(prompt) :].strip()

    def _create_prompt(self, question: str, context: str) -> str:
        """Create a prompt for the LLM."""
        return f"""<s>[INST] You are a helpful AI assistant. Answer the question based on the provided context. If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Question: {question}

Answer: [/INST]"""

    def _fallback_answer(self, question: str, context: str) -> str:
        """Fallback answer when LLM is not available."""
        # Simple template-based answer
        if not context.strip():
            return "I don't have enough information to answer your question. Please upload some documents first."

        # Return the most relevant context chunk
        context_chunks = context.split("\n\n")
        if context_chunks:
            return f"Based on the available information:\n\n{context_chunks[0]}"

        return "I found some relevant information, but I'm unable to generate a comprehensive answer at the moment."

    def get_status(self) -> dict[str, Any]:
        """Get the status of the LLM runner."""
        return {
            "model_type": self.model_type,
            "model_path": self.model_path,
            "model_name": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "available_backends": {
                "llama-cpp": LLAMACPP_AVAILABLE,
                "ollama": OLLAMA_AVAILABLE,
                "transformers": TRANSFORMERS_AVAILABLE,
            },
        }


# Global LLM runner instance
_llm_runner = None


def get_llm_runner() -> LLMRunner:
    """Get the global LLM runner instance."""
    global _llm_runner
    if _llm_runner is None:
        _llm_runner = LLMRunner()
    return _llm_runner


def generate_answer(question: str, context: str) -> str:
    """Generate an answer using the global LLM runner."""
    runner = get_llm_runner()
    return runner.generate_answer(question, context)
