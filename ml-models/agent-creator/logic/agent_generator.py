#!/usr/bin/env python3
"""
Agent Generator
==============

Core logic for generating AI agents and tools from natural language tasks.
Uses LangChain with local LLM to create scripts, YAML, and commands.
"""

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackManager
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class AgentGenerator:
    """
    AI Agent Generator for creating tools and scripts from natural language.
    """

    def __init__(
        self,
        tools_dir: str = "output/tools",
        llm_model_path: str = "llm_weights/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    ):
        """
        Initialize the agent generator.

        Args:
            tools_dir: Directory to save generated tools
            llm_model_path: Path to the local LLM model
        """
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)

        # LLM configuration
        self.llm_model_path = llm_model_path
        self.llm = None

        # Tool categories
        self.tool_categories = {
            "kubernetes": [
                "pod",
                "deployment",
                "service",
                "configmap",
                "secret",
                "namespace",
            ],
            "docker": ["container", "image", "dockerfile", "compose"],
            "bash": ["script", "command", "shell", "bash"],
            "python": ["script", "api", "automation", "data"],
            "yaml": ["config", "manifest", "deployment", "kubernetes"],
            "terraform": ["infrastructure", "aws", "azure", "gcp", "cloud"],
        }

        logger.info(
            f"🤖 Agent Generator initialized with tools directory: {self.tools_dir}"
        )

    def _initialize_llm(self):
        """Initialize the local LLM if not already done."""
        if self.llm is None:
            try:
                # Check if model exists
                if not os.path.exists(self.llm_model_path):
                    logger.warning(f"LLM model not found at {self.llm_model_path}")
                    return False

                # Initialize LLM with streaming callback
                callback_manager = CallbackManager([StreamingStdOutCallbackManager()])

                self.llm = LlamaCpp(
                    model_path=self.llm_model_path,
                    temperature=0.1,
                    max_tokens=2048,
                    n_ctx=4096,
                    callback_manager=callback_manager,
                    verbose=False,
                )

                logger.info("✅ Local LLM initialized successfully")
                return True

            except Exception as e:
                logger.error(f"Failed to initialize LLM: {e}")
                return False
        return True

    def _categorize_task(self, task: str) -> str:
        """
        Categorize the task based on keywords.

        Args:
            task: The task description

        Returns:
            Category name
        """
        task_lower = task.lower()

        for category, keywords in self.tool_categories.items():
            for keyword in keywords:
                if keyword in task_lower:
                    return category

        return "general"

    def _get_prompt_template(self, category: str) -> str:
        """
        Get the appropriate prompt template for the task category.

        Args:
            category: Task category

        Returns:
            Prompt template
        """
        base_template = """You are an expert DevOps and automation assistant. Given a task, generate the appropriate code, script, or configuration.

Task: {task}

Requirements:
- Generate only the code/script, no explanations
- Use best practices and security standards
- Include proper error handling where appropriate
- Add comments for clarity
- Ensure the code is production-ready

Output the code:"""

        category_templates = {
            "kubernetes": """You are a Kubernetes expert. Generate a valid YAML manifest for the given task.

Task: {task}

Requirements:
- Generate valid Kubernetes YAML
- Use current API versions
- Include proper labels and annotations
- Add resource limits and requests
- Follow security best practices
- Include comments for clarity

Output the YAML:""",
            "docker": """You are a Docker expert. Generate Docker configuration for the given task.

Task: {task}

Requirements:
- Generate valid Dockerfile or docker-compose.yml
- Use multi-stage builds when appropriate
- Include proper security practices
- Optimize for size and performance
- Add health checks where relevant
- Include comments for clarity

Output the Docker configuration:""",
            "bash": """You are a bash scripting expert. Generate a bash script for the given task.

Task: {task}

Requirements:
- Generate executable bash script
- Include proper error handling
- Add input validation
- Use proper exit codes
- Include logging and debugging
- Add comments for clarity
- Make it safe and secure

Output the bash script:""",
            "python": """You are a Python automation expert. Generate a Python script for the given task.

Task: {task}

Requirements:
- Generate executable Python code
- Include proper error handling
- Add input validation
- Use type hints where appropriate
- Include logging
- Add comments for clarity
- Follow PEP 8 standards
- Make it production-ready

Output the Python script:""",
            "terraform": """You are a Terraform infrastructure expert. Generate Terraform configuration for the given task.

Task: {task}

Requirements:
- Generate valid Terraform HCL
- Use current provider versions
- Include proper variable definitions
- Add outputs where useful
- Include proper tagging
- Follow security best practices
- Add comments for clarity

Output the Terraform configuration:""",
        }

        return category_templates.get(category, base_template)

    def generate_tool(
        self, task: str, category: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Generate a tool/script from a natural language task.

        Args:
            task: Natural language description of the task
            category: Optional category override

        Returns:
            Dictionary with generated tool information
        """
        try:
            logger.info(f"🚀 Generating tool for task: {task}")

            # Initialize LLM if needed
            if not self._initialize_llm():
                return {
                    "error": "LLM not available - please ensure model is downloaded"
                }

            # Categorize task if not provided
            if not category:
                category = self._categorize_task(task)

            # Get appropriate prompt template
            prompt_template = self._get_prompt_template(category)

            # Create prompt
            prompt = PromptTemplate(input_variables=["task"], template=prompt_template)

            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt)

            # Generate tool
            result = chain.run(task=task)

            # Clean up the result
            tool_code = result.strip()

            # Generate unique tool ID
            tool_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().isoformat()

            # Save tool to file
            filename = f"{category}_{tool_id}.{self._get_file_extension(category)}"
            file_path = self.tools_dir / filename

            with open(file_path, "w") as f:
                f.write(tool_code)

            # Prepare response
            response = {
                "success": True,
                "tool_id": tool_id,
                "category": category,
                "task": task,
                "tool_code": tool_code,
                "filename": filename,
                "file_path": str(file_path),
                "generated_at": timestamp,
                "estimated_complexity": self._estimate_complexity(tool_code),
                "suggested_usage": self._get_usage_suggestions(category, task),
            }

            logger.info(f"✅ Tool generated successfully: {tool_id}")
            return response

        except Exception as e:
            logger.error(f"Tool generation failed: {e}")
            return {"error": f"Generation failed: {str(e)}"}

    def _get_file_extension(self, category: str) -> str:
        """Get the appropriate file extension for the category."""
        extensions = {
            "kubernetes": "yaml",
            "docker": "yaml",
            "bash": "sh",
            "python": "py",
            "terraform": "tf",
            "yaml": "yaml",
            "general": "txt",
        }
        return extensions.get(category, "txt")

    def _estimate_complexity(self, code: str) -> str:
        """Estimate the complexity of the generated tool."""
        lines = len(code.split("\n"))
        if lines < 20:
            return "simple"
        elif lines < 50:
            return "moderate"
        else:
            return "complex"

    def _get_usage_suggestions(self, category: str, task: str) -> list[str]:
        """Get usage suggestions for the generated tool."""
        suggestions = {
            "kubernetes": [
                "Apply with: kubectl apply -f <filename>",
                "Validate with: kubectl apply --dry-run=client -f <filename>",
                "Check status with: kubectl get pods -l app=<app-name>",
            ],
            "docker": [
                "Build with: docker build -t <image-name> .",
                "Run with: docker run <image-name>",
                "Use docker-compose: docker-compose up -d",
            ],
            "bash": [
                "Make executable: chmod +x <filename>",
                "Run with: ./<filename>",
                "Test with: bash -n <filename> (syntax check)",
            ],
            "python": [
                "Install dependencies: pip install -r requirements.txt",
                "Run with: python <filename>",
                "Test with: python -m py_compile <filename>",
            ],
            "terraform": [
                "Initialize: terraform init",
                "Plan: terraform plan",
                "Apply: terraform apply",
            ],
        }
        return suggestions.get(
            category,
            ["Review the code before execution", "Test in a safe environment first"],
        )

    def list_tools(self) -> list[dict[str, Any]]:
        """
        List all generated tools.

        Returns:
            List of tool information
        """
        tools = []

        for tool_file in self.tools_dir.glob("*.*"):
            try:
                # Extract info from filename
                filename = tool_file.name
                parts = filename.split("_")
                category = parts[0] if len(parts) > 1 else "unknown"
                tool_id = parts[1].split(".")[0] if len(parts) > 1 else "unknown"

                # Read file content
                with open(tool_file) as f:
                    content = f.read()

                tools.append(
                    {
                        "tool_id": tool_id,
                        "category": category,
                        "filename": filename,
                        "file_path": str(tool_file),
                        "file_size": tool_file.stat().st_size,
                        "lines_of_code": len(content.split("\n")),
                        "created_at": datetime.fromtimestamp(
                            tool_file.stat().st_ctime
                        ).isoformat(),
                        "complexity": self._estimate_complexity(content),
                    }
                )

            except Exception as e:
                logger.warning(f"Failed to read tool info for {tool_file}: {e}")

        return sorted(tools, key=lambda x: x["created_at"], reverse=True)

    def get_tool(self, tool_id: str) -> dict[str, Any]:
        """
        Get a specific tool by ID.

        Args:
            tool_id: Tool ID to retrieve

        Returns:
            Tool information and content
        """
        try:
            # Find tool file
            tool_files = list(self.tools_dir.glob(f"*{tool_id}*"))
            if not tool_files:
                return {"error": f"Tool with ID {tool_id} not found"}

            tool_file = tool_files[0]

            # Read content
            with open(tool_file) as f:
                content = f.read()

            # Extract info
            filename = tool_file.name
            parts = filename.split("_")
            category = parts[0] if len(parts) > 1 else "unknown"

            return {
                "tool_id": tool_id,
                "category": category,
                "filename": filename,
                "content": content,
                "file_path": str(tool_file),
                "created_at": datetime.fromtimestamp(
                    tool_file.stat().st_ctime
                ).isoformat(),
                "complexity": self._estimate_complexity(content),
            }

        except Exception as e:
            logger.error(f"Failed to get tool: {e}")
            return {"error": f"Failed to get tool: {str(e)}"}

    def delete_tool(self, tool_id: str) -> dict[str, Any]:
        """
        Delete a tool by ID.

        Args:
            tool_id: Tool ID to delete

        Returns:
            Deletion confirmation
        """
        try:
            # Find tool file
            tool_files = list(self.tools_dir.glob(f"*{tool_id}*"))
            if not tool_files:
                return {"error": f"Tool with ID {tool_id} not found"}

            # Delete file
            tool_file = tool_files[0]
            tool_file.unlink()

            logger.info(f"🗑️ Deleted tool: {tool_id}")

            return {"message": f"Tool {tool_id} deleted successfully"}

        except Exception as e:
            logger.error(f"Failed to delete tool: {e}")
            return {"error": f"Failed to delete tool: {str(e)}"}

    def get_categories(self) -> dict[str, Any]:
        """
        Get available tool categories and their descriptions.

        Returns:
            Category information
        """
        return {
            "categories": {
                "kubernetes": {
                    "description": "Kubernetes manifests and configurations",
                    "keywords": self.tool_categories["kubernetes"],
                    "file_extension": "yaml",
                },
                "docker": {
                    "description": "Docker configurations and scripts",
                    "keywords": self.tool_categories["docker"],
                    "file_extension": "yaml",
                },
                "bash": {
                    "description": "Bash scripts and shell commands",
                    "keywords": self.tool_categories["bash"],
                    "file_extension": "sh",
                },
                "python": {
                    "description": "Python scripts and automation",
                    "keywords": self.tool_categories["python"],
                    "file_extension": "py",
                },
                "terraform": {
                    "description": "Terraform infrastructure code",
                    "keywords": self.tool_categories["terraform"],
                    "file_extension": "tf",
                },
                "general": {
                    "description": "General purpose tools and scripts",
                    "keywords": ["script", "tool", "automation"],
                    "file_extension": "txt",
                },
            }
        }


# Convenience function for backward compatibility
def generate_tool(task: str, category: Optional[str] = None) -> dict[str, Any]:
    """
    Convenience function for generating a tool.

    Args:
        task: Natural language description of the task
        category: Optional category override

    Returns:
        Generated tool information
    """
    generator = AgentGenerator()
    return generator.generate_tool(task, category)
