"""
Helm logic for the Kubernetes Specialist AI Agent.
Handles Helm chart operations including install, upgrade, and uninstall.
"""

import asyncio
import json
import logging
import tempfile
import os
from typing import Dict, Any, List, Optional
import aiofiles

logger = logging.getLogger(__name__)


class HelmManager:
    """Manages Helm chart operations and release management."""

    def __init__(self, kubeconfig: Optional[str] = None):
        self.kubeconfig = kubeconfig
        self.helm_binary = "helm"

    async def install_chart(
        self,
        release_name: str,
        chart_name: str,
        namespace: str = "default",
        values: Dict[str, Any] = {},
        version: Optional[str] = None,
        wait: bool = True,
        timeout: Optional[int] = 300,
    ) -> Dict[str, Any]:
        """
        Install a Helm chart.

        Args:
            release_name: Name of the release
            chart_name: Chart name or path
            namespace: Target namespace
            values: Values to override
            version: Chart version
            wait: Wait for deployment to complete
            timeout: Timeout in seconds

        Returns:
            Installation result
        """
        try:
            # Create values file if values provided
            values_file = None
            if values:
                values_file = await self._create_values_file(values)

            # Build command
            cmd = [
                self.helm_binary,
                "install",
                release_name,
                chart_name,
                "--namespace",
                namespace,
                "--create-namespace",
            ]

            if values_file:
                cmd.extend(["-f", values_file])

            if version:
                cmd.extend(["--version", version])

            if wait:
                cmd.append("--wait")
                if timeout:
                    cmd.extend(["--timeout", f"{timeout}s"])

            # Execute command
            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                # Get release status
                status = await self._get_release_status(release_name, namespace)

                return {
                    "status": "installed",
                    "release_name": release_name,
                    "namespace": namespace,
                    "chart_version": status.get("chart_version"),
                    "app_version": status.get("app_version"),
                    "last_deployed": status.get("last_deployed"),
                    "description": status.get("description"),
                    "output": result["output"],
                }
            else:
                raise Exception(f"Helm install failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm install failed: {str(e)}")
            raise

    async def upgrade_chart(
        self,
        release_name: str,
        chart_name: str,
        namespace: str = "default",
        values: Dict[str, Any] = {},
        version: Optional[str] = None,
        wait: bool = True,
        timeout: Optional[int] = 300,
    ) -> Dict[str, Any]:
        """
        Upgrade an existing Helm chart.

        Args:
            release_name: Name of the release
            chart_name: Chart name or path
            namespace: Target namespace
            values: Values to override
            version: Chart version
            wait: Wait for deployment to complete
            timeout: Timeout in seconds

        Returns:
            Upgrade result
        """
        try:
            # Create values file if values provided
            values_file = None
            if values:
                values_file = await self._create_values_file(values)

            # Build command
            cmd = [
                self.helm_binary,
                "upgrade",
                release_name,
                chart_name,
                "--namespace",
                namespace,
            ]

            if values_file:
                cmd.extend(["-f", values_file])

            if version:
                cmd.extend(["--version", version])

            if wait:
                cmd.append("--wait")
                if timeout:
                    cmd.extend(["--timeout", f"{timeout}s"])

            # Execute command
            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                # Get release status
                status = await self._get_release_status(release_name, namespace)

                return {
                    "status": "upgraded",
                    "release_name": release_name,
                    "namespace": namespace,
                    "chart_version": status.get("chart_version"),
                    "app_version": status.get("app_version"),
                    "last_deployed": status.get("last_deployed"),
                    "description": status.get("description"),
                    "output": result["output"],
                }
            else:
                raise Exception(f"Helm upgrade failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm upgrade failed: {str(e)}")
            raise

    async def uninstall_chart(
        self, release_name: str, namespace: str = "default"
    ) -> Dict[str, Any]:
        """
        Uninstall a Helm chart.

        Args:
            release_name: Name of the release
            namespace: Target namespace

        Returns:
            Uninstall result
        """
        try:
            cmd = [
                self.helm_binary,
                "uninstall",
                release_name,
                "--namespace",
                namespace,
            ]

            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                return {
                    "status": "uninstalled",
                    "release_name": release_name,
                    "namespace": namespace,
                    "message": "Release uninstalled successfully",
                    "output": result["output"],
                }
            else:
                raise Exception(f"Helm uninstall failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm uninstall failed: {str(e)}")
            raise

    async def list_releases(
        self, namespace: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List Helm releases.

        Args:
            namespace: Filter by namespace

        Returns:
            List of releases
        """
        try:
            cmd = [self.helm_binary, "list", "--output", "json"]

            if namespace:
                cmd.extend(["--namespace", namespace])
            else:
                cmd.append("--all-namespaces")

            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                releases_data = json.loads(result["output"])
                return releases_data.get("Releases", [])
            else:
                raise Exception(f"Helm list failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm list failed: {str(e)}")
            raise

    async def get_release_status(
        self, release_name: str, namespace: str = "default"
    ) -> Dict[str, Any]:
        """
        Get detailed status of a Helm release.

        Args:
            release_name: Name of the release
            namespace: Target namespace

        Returns:
            Release status
        """
        try:
            cmd = [
                self.helm_binary,
                "status",
                release_name,
                "--namespace",
                namespace,
                "--output",
                "json",
            ]

            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                return json.loads(result["output"])
            else:
                raise Exception(f"Helm status failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm status failed: {str(e)}")
            raise

    async def rollback_release(
        self, release_name: str, revision: int, namespace: str = "default"
    ) -> Dict[str, Any]:
        """
        Rollback a Helm release to a previous revision.

        Args:
            release_name: Name of the release
            revision: Revision number to rollback to
            namespace: Target namespace

        Returns:
            Rollback result
        """
        try:
            cmd = [
                self.helm_binary,
                "rollback",
                release_name,
                str(revision),
                "--namespace",
                namespace,
            ]

            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                return {
                    "status": "rolled_back",
                    "release_name": release_name,
                    "revision": revision,
                    "namespace": namespace,
                    "output": result["output"],
                }
            else:
                raise Exception(f"Helm rollback failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm rollback failed: {str(e)}")
            raise

    async def get_release_history(
        self, release_name: str, namespace: str = "default"
    ) -> List[Dict[str, Any]]:
        """
        Get release history.

        Args:
            release_name: Name of the release
            namespace: Target namespace

        Returns:
            Release history
        """
        try:
            cmd = [
                self.helm_binary,
                "history",
                release_name,
                "--namespace",
                namespace,
                "--output",
                "json",
            ]

            result = await self._run_command(cmd)

            if result["return_code"] == 0:
                history_data = json.loads(result["output"])
                return history_data.get("Releases", [])
            else:
                raise Exception(f"Helm history failed: {result['error']}")

        except Exception as e:
            logger.error(f"Helm history failed: {str(e)}")
            raise

    async def _create_values_file(self, values: Dict[str, Any]) -> str:
        """Create a temporary values file."""
        try:
            # Create temporary file
            fd, path = tempfile.mkstemp(suffix=".yaml")
            os.close(fd)

            # Write values to file
            content = self._dict_to_yaml(values)
            async with aiofiles.open(path, "w") as f:
                await f.write(content)

            return path

        except Exception as e:
            logger.error(f"Failed to create values file: {str(e)}")
            raise

    def _dict_to_yaml(self, data: Dict[str, Any], indent: int = 0) -> str:
        """Convert dictionary to YAML format."""
        yaml_content = ""
        for key, value in data.items():
            if isinstance(value, dict):
                yaml_content += " " * indent + f"{key}:\n"
                yaml_content += self._dict_to_yaml(value, indent + 2)
            elif isinstance(value, list):
                yaml_content += " " * indent + f"{key}:\n"
                for item in value:
                    if isinstance(item, dict):
                        yaml_content += " " * (indent + 2) + "-\n"
                        yaml_content += self._dict_to_yaml(item, indent + 4)
                    else:
                        yaml_content += " " * (indent + 2) + f"- {item}\n"
            else:
                yaml_content += " " * indent + f"{key}: {value}\n"

        return yaml_content

    async def _run_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run a Helm command."""
        try:
            env = os.environ.copy()
            if self.kubeconfig:
                env["KUBECONFIG"] = self.kubeconfig

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )

            stdout, stderr = await process.communicate()

            output = stdout.decode() if stdout else ""
            error = stderr.decode() if stderr else ""

            return {
                "output": output,
                "error": error if error else None,
                "return_code": process.returncode,
            }

        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            raise

    async def _get_release_status(
        self, release_name: str, namespace: str
    ) -> Dict[str, Any]:
        """Get release status information."""
        try:
            status = await self.get_release_status(release_name, namespace)
            return {
                "chart_version": status.get("Chart", {})
                .get("Metadata", {})
                .get("Version"),
                "app_version": status.get("Chart", {})
                .get("Metadata", {})
                .get("AppVersion"),
                "last_deployed": status.get("Info", {}).get("LastDeployed"),
                "description": status.get("Info", {}).get("Description"),
            }
        except Exception:
            return {}


# Main functions for the API
async def install_chart(
    release_name: str,
    chart_name: str,
    namespace: str = "default",
    values: Dict[str, Any] = {},
    version: Optional[str] = None,
    wait: bool = True,
    timeout: Optional[int] = 300,
) -> Dict[str, Any]:
    """
    Install a Helm chart.

    Args:
        release_name: Name of the release
        chart_name: Chart name or path
        namespace: Target namespace
        values: Values to override
        version: Chart version
        wait: Wait for deployment to complete
        timeout: Timeout in seconds

    Returns:
        Installation result
    """
    try:
        manager = HelmManager()
        return await manager.install_chart(
            release_name=release_name,
            chart_name=chart_name,
            namespace=namespace,
            values=values,
            version=version,
            wait=wait,
            timeout=timeout,
        )
    except Exception as e:
        logger.error(f"Helm install failed: {str(e)}")
        raise


async def upgrade_chart(
    release_name: str,
    chart_name: str,
    namespace: str = "default",
    values: Dict[str, Any] = {},
    version: Optional[str] = None,
    wait: bool = True,
    timeout: Optional[int] = 300,
) -> Dict[str, Any]:
    """
    Upgrade an existing Helm chart.

    Args:
        release_name: Name of the release
        chart_name: Chart name or path
        namespace: Target namespace
        values: Values to override
        version: Chart version
        wait: Wait for deployment to complete
        timeout: Timeout in seconds

    Returns:
        Upgrade result
    """
    try:
        manager = HelmManager()
        return await manager.upgrade_chart(
            release_name=release_name,
            chart_name=chart_name,
            namespace=namespace,
            values=values,
            version=version,
            wait=wait,
            timeout=timeout,
        )
    except Exception as e:
        logger.error(f"Helm upgrade failed: {str(e)}")
        raise


async def uninstall_chart(
    release_name: str, namespace: str = "default"
) -> Dict[str, Any]:
    """
    Uninstall a Helm chart.

    Args:
        release_name: Name of the release
        namespace: Target namespace

    Returns:
        Uninstall result
    """
    try:
        manager = HelmManager()
        return await manager.uninstall_chart(release_name, namespace)
    except Exception as e:
        logger.error(f"Helm uninstall failed: {str(e)}")
        raise


async def list_releases(namespace: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List Helm releases.

    Args:
        namespace: Filter by namespace

    Returns:
        List of releases
    """
    try:
        manager = HelmManager()
        return await manager.list_releases(namespace)
    except Exception as e:
        logger.error(f"Helm list failed: {str(e)}")
        raise
