from fastapi import FastAPI
from routers import cursor_patch_router, migrate_router, remote_link_router


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


app = FastAPI(
    title="Audit Migrate Service",
    description=(
        "Generate real folder structures and microservices from scaffold plans. "
        "Linked to audit_assess, audit_logic, whis_logic, igris_logic."
    ),
    version="1.0.0",
)

app.include_router(migrate_router.router)
app.include_router(remote_link_router.router)
app.include_router(cursor_patch_router.router)
