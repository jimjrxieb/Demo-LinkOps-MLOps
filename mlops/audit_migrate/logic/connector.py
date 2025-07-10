from typing import Any, Dict


def sanitize_cmd(cmd):
    import shlex

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


import httpx


class ServiceConnector:
    def __init__(self):
        self.assess_base = "http://audit_assess:8005/scan"
        # In production, use service discovery or config

    async def call_audit_assess_scan(
        self, repo_url: str, branch: str = "main"
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.assess_base}/repo/",
                json={"repo_url": repo_url, "branch": branch},
            )
            resp.raise_for_status()
            return resp.json()

    async def call_audit_assess_suggestions(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.assess_base}/suggestions/")
            resp.raise_for_status()
            return resp.json()

    async def call_audit_assess_scaffold_plan(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.assess_base}/scaffold-plan/")
            resp.raise_for_status()
            return resp.json()
