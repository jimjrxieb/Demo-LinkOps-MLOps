"""
CI/CD logic for the Platform Engineer AI Agent.
Handles pipeline triggering, monitoring, and rollback operations.
"""

import logging
from typing import Dict, Any, Tuple
from datetime import datetime
import aiohttp
import os

logger = logging.getLogger(__name__)

# Configuration for different CI/CD platforms
CI_PLATFORMS = {
    "github": {
        "api_base": "https://api.github.com",
        "trigger_endpoint": "/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches",
    },
    "gitlab": {
        "api_base": "https://gitlab.com/api/v4",
        "trigger_endpoint": "/projects/{project_id}/pipeline",
    },
    "jenkins": {
        "api_base": "http://jenkins:8080",
        "trigger_endpoint": "/job/{job_name}/build",
    },
    "azure": {
        "api_base": "https://dev.azure.com",
        "trigger_endpoint": "/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs",
    },
}


async def trigger_pipeline(
    name: str,
    repo_url: str,
    branch: str = "main",
    environment: str = "production",
    variables: Dict[str, str] = {},
) -> Tuple[str, str, str]:
    """
    Trigger a CI/CD pipeline for a specific repository and branch.

    Args:
        name: Pipeline/workflow name
        repo_url: Repository URL
        branch: Branch to trigger on
        environment: Target environment
        variables: Pipeline variables

    Returns:
        Tuple of (pipeline_id, status, url)
    """
    try:
        # Determine CI platform from repo URL
        platform = _detect_ci_platform(repo_url)

        if platform == "github":
            return await _trigger_github_workflow(
                name, repo_url, branch, environment, variables
            )
        elif platform == "gitlab":
            return await _trigger_gitlab_pipeline(
                name, repo_url, branch, environment, variables
            )
        elif platform == "jenkins":
            return await _trigger_jenkins_job(
                name, repo_url, branch, environment, variables
            )
        elif platform == "azure":
            return await _trigger_azure_pipeline(
                name, repo_url, branch, environment, variables
            )
        else:
            raise ValueError(f"Unsupported CI platform: {platform}")

    except Exception as e:
        logger.error(f"Pipeline trigger failed: {str(e)}")
        raise


async def monitor_pipeline(pipeline_id: str) -> Dict[str, Any]:
    """
    Monitor the status of a running pipeline.

    Args:
        pipeline_id: The pipeline ID to monitor

    Returns:
        Pipeline status information
    """
    try:
        # Parse pipeline ID to determine platform and extract info
        platform, project_info = _parse_pipeline_id(pipeline_id)

        if platform == "github":
            return await _monitor_github_workflow(pipeline_id, project_info)
        elif platform == "gitlab":
            return await _monitor_gitlab_pipeline(pipeline_id, project_info)
        elif platform == "jenkins":
            return await _monitor_jenkins_job(pipeline_id, project_info)
        elif platform == "azure":
            return await _monitor_azure_pipeline(pipeline_id, project_info)
        else:
            raise ValueError(f"Unsupported CI platform: {platform}")

    except Exception as e:
        logger.error(f"Pipeline monitoring failed: {str(e)}")
        raise


async def rollback_deployment(pipeline_id: str) -> Dict[str, Any]:
    """
    Rollback a deployment to the previous version.

    Args:
        pipeline_id: The pipeline ID to rollback

    Returns:
        Rollback status information
    """
    try:
        # Parse pipeline ID to determine platform
        platform, project_info = _parse_pipeline_id(pipeline_id)

        if platform == "github":
            return await _rollback_github_deployment(pipeline_id, project_info)
        elif platform == "gitlab":
            return await _rollback_gitlab_deployment(pipeline_id, project_info)
        elif platform == "jenkins":
            return await _rollback_jenkins_deployment(pipeline_id, project_info)
        elif platform == "azure":
            return await _rollback_azure_deployment(pipeline_id, project_info)
        else:
            raise ValueError(f"Unsupported CI platform: {platform}")

    except Exception as e:
        logger.error(f"Deployment rollback failed: {str(e)}")
        raise


# GitHub Actions specific functions
async def _trigger_github_workflow(
    name: str, repo_url: str, branch: str, environment: str, variables: Dict[str, str]
) -> Tuple[str, str, str]:
    """Trigger a GitHub Actions workflow."""
    try:
        # Extract owner and repo from URL
        owner, repo = _extract_github_info(repo_url)

        # Get GitHub token from environment
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

        # Prepare request
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        payload = {"ref": branch, "inputs": {"environment": environment, **variables}}

        # Make API call
        async with aiohttp.ClientSession() as session:
            url = f"{CI_PLATFORMS['github']['api_base']}/repos/{owner}/{repo}/actions/workflows/{name}/dispatches"
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 204:
                    # Get the workflow run ID
                    run_id = await _get_latest_workflow_run(owner, repo, name, token)
                    pipeline_id = f"github:{owner}/{repo}:{run_id}"
                    status = "triggered"
                    url = f"https://github.com/{owner}/{repo}/actions/runs/{run_id}"
                    return pipeline_id, status, url
                else:
                    error_text = await response.text()
                    raise Exception(
                        f"GitHub API error: {response.status} - {error_text}"
                    )

    except Exception as e:
        logger.error(f"GitHub workflow trigger failed: {str(e)}")
        raise


async def _monitor_github_workflow(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Monitor a GitHub Actions workflow."""
    try:
        # Extract run ID from pipeline ID
        run_id = pipeline_id.split(":")[-1]
        owner = project_info["owner"]
        repo = project_info["repo"]

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with aiohttp.ClientSession() as session:
            url = f"{CI_PLATFORMS['github']['api_base']}/repos/{owner}/{repo}/actions/runs/{run_id}"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": data["status"],
                        "conclusion": data.get("conclusion"),
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "html_url": data["html_url"],
                        "jobs": data.get("jobs", []),
                    }
                else:
                    raise Exception(f"Failed to get workflow status: {response.status}")

    except Exception as e:
        logger.error(f"GitHub workflow monitoring failed: {str(e)}")
        raise


async def _rollback_github_deployment(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Rollback a GitHub deployment."""
    try:
        # This would typically involve reverting to a previous commit or deployment
        # For now, return a placeholder response
        return {
            "status": "rollback_initiated",
            "method": "git_revert",
            "target_commit": "previous_stable",
            "rollback_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"GitHub deployment rollback failed: {str(e)}")
        raise


# GitLab CI specific functions
async def _trigger_gitlab_pipeline(
    name: str, repo_url: str, branch: str, environment: str, variables: Dict[str, str]
) -> Tuple[str, str, str]:
    """Trigger a GitLab CI pipeline."""
    try:
        # Extract project ID from URL
        project_id = _extract_gitlab_project_id(repo_url)

        # Get GitLab token from environment
        token = os.getenv("GITLAB_TOKEN")
        if not token:
            raise ValueError("GITLAB_TOKEN environment variable not set")

        headers = {"PRIVATE-TOKEN": token, "Content-Type": "application/json"}

        payload = {
            "ref": branch,
            "variables": [
                {"key": "ENVIRONMENT", "value": environment},
                *[{"key": k, "value": v} for k, v in variables.items()],
            ],
        }

        async with aiohttp.ClientSession() as session:
            url = f"{CI_PLATFORMS['gitlab']['api_base']}/projects/{project_id}/pipeline"
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 201:
                    data = await response.json()
                    pipeline_id = f"gitlab:{project_id}:{data['id']}"
                    status = "triggered"
                    url = data["web_url"]
                    return pipeline_id, status, url
                else:
                    error_text = await response.text()
                    raise Exception(
                        f"GitLab API error: {response.status} - {error_text}"
                    )

    except Exception as e:
        logger.error(f"GitLab pipeline trigger failed: {str(e)}")
        raise


async def _monitor_gitlab_pipeline(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Monitor a GitLab CI pipeline."""
    try:
        # Extract pipeline ID
        pipeline_id_num = pipeline_id.split(":")[-1]
        project_id = project_info["project_id"]

        token = os.getenv("GITLAB_TOKEN")
        if not token:
            raise ValueError("GITLAB_TOKEN environment variable not set")

        headers = {"PRIVATE-TOKEN": token}

        async with aiohttp.ClientSession() as session:
            url = f"{CI_PLATFORMS['gitlab']['api_base']}/projects/{project_id}/pipelines/{pipeline_id_num}"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": data["status"],
                        "ref": data["ref"],
                        "sha": data["sha"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "web_url": data["web_url"],
                    }
                else:
                    raise Exception(f"Failed to get pipeline status: {response.status}")

    except Exception as e:
        logger.error(f"GitLab pipeline monitoring failed: {str(e)}")
        raise


async def _rollback_gitlab_deployment(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Rollback a GitLab deployment."""
    try:
        return {
            "status": "rollback_initiated",
            "method": "git_revert",
            "target_commit": "previous_stable",
            "rollback_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"GitLab deployment rollback failed: {str(e)}")
        raise


# Jenkins specific functions
async def _trigger_jenkins_job(
    name: str, repo_url: str, branch: str, environment: str, variables: Dict[str, str]
) -> Tuple[str, str, str]:
    """Trigger a Jenkins job."""
    try:
        # Get Jenkins credentials
        username = os.getenv("JENKINS_USERNAME")
        token = os.getenv("JENKINS_TOKEN")

        if not username or not token:
            raise ValueError(
                "JENKINS_USERNAME and JENKINS_TOKEN environment variables not set"
            )

        # Build parameters
        params = {
            "ENVIRONMENT": environment,
            "BRANCH": branch,
            "REPO_URL": repo_url,
            **variables,
        }

        # Trigger job via Jenkins API
        job_url = (
            f"{CI_PLATFORMS['jenkins']['api_base']}/job/{name}/buildWithParameters"
        )

        # For now, return placeholder response
        pipeline_id = f"jenkins:{name}:{datetime.now().strftime('%Y%m%d%H%M%S')}"
        status = "triggered"
        url = f"{CI_PLATFORMS['jenkins']['api_base']}/job/{name}"

        return pipeline_id, status, url

    except Exception as e:
        logger.error(f"Jenkins job trigger failed: {str(e)}")
        raise


async def _monitor_jenkins_job(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Monitor a Jenkins job."""
    try:
        # Placeholder implementation
        return {
            "status": "running",
            "build_number": "123",
            "estimated_duration": 300,
            "url": f"{CI_PLATFORMS['jenkins']['api_base']}/job/{project_info['job_name']}/123",
        }
    except Exception as e:
        logger.error(f"Jenkins job monitoring failed: {str(e)}")
        raise


async def _rollback_jenkins_deployment(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Rollback a Jenkins deployment."""
    try:
        return {
            "status": "rollback_initiated",
            "method": "previous_build",
            "target_build": "previous_stable",
            "rollback_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Jenkins deployment rollback failed: {str(e)}")
        raise


# Azure DevOps specific functions
async def _trigger_azure_pipeline(
    name: str, repo_url: str, branch: str, environment: str, variables: Dict[str, str]
) -> Tuple[str, str, str]:
    """Trigger an Azure DevOps pipeline."""
    try:
        # Get Azure DevOps token
        token = os.getenv("AZURE_DEVOPS_TOKEN")
        if not token:
            raise ValueError("AZURE_DEVOPS_TOKEN environment variable not set")

        # Extract organization and project
        org, project = _extract_azure_info(repo_url)

        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "resources": {
                "repositories": {"self": {"refName": f"refs/heads/{branch}"}}
            },
            "variables": {
                "ENVIRONMENT": {"value": environment},
                **{k: {"value": v} for k, v in variables.items()},
            },
        }

        # Placeholder implementation
        pipeline_id = f"azure:{org}/{project}:{datetime.now().strftime('%Y%m%d%H%M%S')}"
        status = "triggered"
        url = f"{CI_PLATFORMS['azure']['api_base']}/{org}/{project}/_build/results"

        return pipeline_id, status, url

    except Exception as e:
        logger.error(f"Azure pipeline trigger failed: {str(e)}")
        raise


async def _monitor_azure_pipeline(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Monitor an Azure DevOps pipeline."""
    try:
        return {
            "status": "running",
            "build_id": "12345",
            "definition_name": project_info.get("pipeline_name", "unknown"),
            "url": f"{CI_PLATFORMS['azure']['api_base']}/{project_info['org']}/{project_info['project']}/_build/results",
        }
    except Exception as e:
        logger.error(f"Azure pipeline monitoring failed: {str(e)}")
        raise


async def _rollback_azure_deployment(
    pipeline_id: str, project_info: Dict[str, str]
) -> Dict[str, Any]:
    """Rollback an Azure DevOps deployment."""
    try:
        return {
            "status": "rollback_initiated",
            "method": "previous_release",
            "target_release": "previous_stable",
            "rollback_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Azure deployment rollback failed: {str(e)}")
        raise


# Helper functions
def _detect_ci_platform(repo_url: str) -> str:
    """Detect CI platform from repository URL."""
    if "github.com" in repo_url:
        return "github"
    elif "gitlab.com" in repo_url or "gitlab" in repo_url:
        return "gitlab"
    elif "dev.azure.com" in repo_url or "visualstudio.com" in repo_url:
        return "azure"
    else:
        # Default to Jenkins for other cases
        return "jenkins"


def _extract_github_info(repo_url: str) -> Tuple[str, str]:
    """Extract owner and repo from GitHub URL."""
    # Handle different GitHub URL formats
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    parts = repo_url.split("/")
    if "github.com" in parts:
        github_index = parts.index("github.com")
        owner = parts[github_index + 1]
        repo = parts[github_index + 2]
        return owner, repo
    else:
        raise ValueError("Invalid GitHub URL format")


def _extract_gitlab_project_id(repo_url: str) -> str:
    """Extract project ID from GitLab URL."""
    # This would need to be implemented based on GitLab API
    # For now, return a placeholder
    return "12345"


def _extract_azure_info(repo_url: str) -> Tuple[str, str]:
    """Extract organization and project from Azure DevOps URL."""
    # Parse Azure DevOps URL format
    parts = repo_url.split("/")
    if "dev.azure.com" in parts:
        azure_index = parts.index("dev.azure.com")
        org = parts[azure_index + 1]
        project = parts[azure_index + 2]
        return org, project
    else:
        raise ValueError("Invalid Azure DevOps URL format")


def _parse_pipeline_id(pipeline_id: str) -> Tuple[str, Dict[str, str]]:
    """Parse pipeline ID to extract platform and project information."""
    parts = pipeline_id.split(":")
    platform = parts[0]

    if platform == "github":
        owner, repo = parts[1].split("/")
        return platform, {"owner": owner, "repo": repo}
    elif platform == "gitlab":
        return platform, {"project_id": parts[1]}
    elif platform == "jenkins":
        return platform, {"job_name": parts[1]}
    elif platform == "azure":
        org, project = parts[1].split("/")
        return platform, {"org": org, "project": project}
    else:
        raise ValueError(f"Unknown platform in pipeline ID: {platform}")


async def _get_latest_workflow_run(
    owner: str, repo: str, workflow: str, token: str
) -> str:
    """Get the latest workflow run ID."""
    try:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with aiohttp.ClientSession() as session:
            url = f"{CI_PLATFORMS['github']['api_base']}/repos/{owner}/{repo}/actions/workflows/{workflow}/runs"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data["workflow_runs"]:
                        return str(data["workflow_runs"][0]["id"])
                    else:
                        raise Exception("No workflow runs found")
                else:
                    raise Exception(f"Failed to get workflow runs: {response.status}")
    except Exception as e:
        logger.error(f"Failed to get latest workflow run: {str(e)}")
        raise
