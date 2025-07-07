"""
Terraform logic for the Platform Engineer AI Agent.
Handles Terraform operations including plan, apply, and destroy.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional
import aiofiles

logger = logging.getLogger(__name__)


class TerraformExecutor:
    """Handles Terraform command execution and state management."""

    def __init__(self, workspace: str, working_dir: str = None):
        self.workspace = workspace
        self.working_dir = working_dir or f"/tmp/terraform/{workspace}"
        self.state_file = f"{self.working_dir}/terraform.tfstate"
        self.backend_config = {}

    async def init(self) -> Dict[str, Any]:
        """Initialize Terraform workspace."""
        try:
            # Create working directory if it doesn't exist
            os.makedirs(self.working_dir, exist_ok=True)

            # Run terraform init
            cmd = [
                "terraform",
                "init",
                "-input=false",
                "-backend-config=key={workspace}.tfstate".format(
                    workspace=self.workspace
                ),
            ]

            result = await self._run_command(cmd)

            return {
                "status": "initialized",
                "workspace": self.workspace,
                "working_dir": self.working_dir,
                "output": result["output"],
                "error": result.get("error"),
            }

        except Exception as e:
            logger.error(f"Terraform init failed: {str(e)}")
            raise

    async def plan(
        self, variables: Dict[str, str] = {}, targets: List[str] = []
    ) -> Dict[str, Any]:
        """Create a Terraform plan."""
        try:
            # Prepare variables file
            var_file = await self._create_variables_file(variables)

            # Build command
            cmd = ["terraform", "plan", "-input=false", "-out=plan.tfplan"]

            if var_file:
                cmd.extend(["-var-file", var_file])

            if targets:
                for target in targets:
                    cmd.extend(["-target", target])

            # Run plan
            result = await self._run_command(cmd)

            # Parse plan output
            plan_summary = await self._parse_plan_output(result["output"])

            return {
                "status": "planned",
                "workspace": self.workspace,
                "plan_file": f"{self.working_dir}/plan.tfplan",
                "summary": plan_summary,
                "output": result["output"],
                "error": result.get("error"),
            }

        except Exception as e:
            logger.error(f"Terraform plan failed: {str(e)}")
            raise

    async def apply(
        self, variables: Dict[str, str] = {}, targets: List[str] = []
    ) -> Dict[str, Any]:
        """Apply Terraform configuration."""
        try:
            # Create plan first
            plan_result = await self.plan(variables, targets)

            if plan_result.get("error"):
                raise Exception(f"Plan failed: {plan_result['error']}")

            # Apply the plan
            cmd = ["terraform", "apply", "-auto-approve", "plan.tfplan"]
            result = await self._run_command(cmd)

            # Parse apply output
            apply_summary = await self._parse_apply_output(result["output"])

            return {
                "status": "applied",
                "workspace": self.workspace,
                "summary": apply_summary,
                "output": result["output"],
                "error": result.get("error"),
            }

        except Exception as e:
            logger.error(f"Terraform apply failed: {str(e)}")
            raise

    async def destroy(self, targets: List[str] = []) -> Dict[str, Any]:
        """Destroy Terraform resources."""
        try:
            # Build command
            cmd = ["terraform", "destroy", "-auto-approve"]

            if targets:
                for target in targets:
                    cmd.extend(["-target", target])

            # Run destroy
            result = await self._run_command(cmd)

            # Parse destroy output
            destroy_summary = await self._parse_destroy_output(result["output"])

            return {
                "status": "destroyed",
                "workspace": self.workspace,
                "summary": destroy_summary,
                "output": result["output"],
                "error": result.get("error"),
            }

        except Exception as e:
            logger.error(f"Terraform destroy failed: {str(e)}")
            raise

    async def show(self) -> Dict[str, Any]:
        """Show current Terraform state."""
        try:
            cmd = ["terraform", "show", "-json"]
            result = await self._run_command(cmd)

            if result.get("error"):
                raise Exception(f"Show failed: {result['error']}")

            # Parse JSON output
            state_data = json.loads(result["output"])

            return {
                "status": "shown",
                "workspace": self.workspace,
                "state": state_data,
                "resources": state_data.get("values", {})
                .get("root_module", {})
                .get("resources", []),
            }

        except Exception as e:
            logger.error(f"Terraform show failed: {str(e)}")
            raise

    async def output(self) -> Dict[str, Any]:
        """Get Terraform outputs."""
        try:
            cmd = ["terraform", "output", "-json"]
            result = await self._run_command(cmd)

            if result.get("error"):
                raise Exception(f"Output failed: {result['error']}")

            # Parse JSON output
            outputs = json.loads(result["output"])

            return {
                "status": "outputs_retrieved",
                "workspace": self.workspace,
                "outputs": outputs,
            }

        except Exception as e:
            logger.error(f"Terraform output failed: {str(e)}")
            raise

    async def validate(self) -> Dict[str, Any]:
        """Validate Terraform configuration."""
        try:
            cmd = ["terraform", "validate"]
            result = await self._run_command(cmd)

            return {
                "status": "validated",
                "workspace": self.workspace,
                "valid": not result.get("error"),
                "output": result["output"],
                "error": result.get("error"),
            }

        except Exception as e:
            logger.error(f"Terraform validate failed: {str(e)}")
            raise

    async def _run_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run a Terraform command."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.working_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
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

    async def _create_variables_file(self, variables: Dict[str, str]) -> Optional[str]:
        """Create a Terraform variables file."""
        if not variables:
            return None

        try:
            var_file = f"{self.working_dir}/variables.tfvars"

            content = ""
            for key, value in variables.items():
                if isinstance(value, str):
                    content += f'{key} = "{value}"\n'
                else:
                    content += f"{key} = {value}\n"

            async with aiofiles.open(var_file, "w") as f:
                await f.write(content)

            return var_file

        except Exception as e:
            logger.error(f"Failed to create variables file: {str(e)}")
            raise

    async def _parse_plan_output(self, output: str) -> Dict[str, Any]:
        """Parse Terraform plan output."""
        try:
            summary = {
                "resources_to_add": 0,
                "resources_to_change": 0,
                "resources_to_destroy": 0,
                "changes": [],
            }

            lines = output.split("\n")
            for line in lines:
                if "Plan:" in line:
                    # Parse plan summary
                    if "to add" in line:
                        summary["resources_to_add"] = int(line.split()[0])
                    if "to change" in line:
                        summary["resources_to_change"] = int(line.split()[0])
                    if "to destroy" in line:
                        summary["resources_to_destroy"] = int(line.split()[0])

                # Parse resource changes
                if (
                    line.strip().startswith("+")
                    or line.strip().startswith("-")
                    or line.strip().startswith("~")
                ):
                    summary["changes"].append(line.strip())

            return summary

        except Exception as e:
            logger.error(f"Failed to parse plan output: {str(e)}")
            return {"error": str(e)}

    async def _parse_apply_output(self, output: str) -> Dict[str, Any]:
        """Parse Terraform apply output."""
        try:
            summary = {
                "resources_created": 0,
                "resources_updated": 0,
                "resources_destroyed": 0,
                "outputs": {},
            }

            lines = output.split("\n")
            for line in lines:
                if "Apply complete!" in line:
                    # Parse apply summary
                    if "created" in line:
                        summary["resources_created"] = int(line.split()[0])
                    if "updated" in line:
                        summary["resources_updated"] = int(line.split()[0])
                    if "destroyed" in line:
                        summary["resources_destroyed"] = int(line.split()[0])

                # Parse outputs
                if "Outputs:" in line:
                    # This is a simplified parser - in reality, you'd need more
                    # sophisticated parsing
                    pass

            return summary

        except Exception as e:
            logger.error(f"Failed to parse apply output: {str(e)}")
            return {"error": str(e)}

    async def _parse_destroy_output(self, output: str) -> Dict[str, Any]:
        """Parse Terraform destroy output."""
        try:
            summary = {"resources_destroyed": 0, "destroy_complete": False}

            lines = output.split("\n")
            for line in lines:
                if "Destroy complete!" in line:
                    summary["destroy_complete"] = True
                    if "destroyed" in line:
                        summary["resources_destroyed"] = int(line.split()[0])

            return summary

        except Exception as e:
            logger.error(f"Failed to parse destroy output: {str(e)}")
            return {"error": str(e)}


# Main functions for the API
async def plan_terraform(
    workspace: str, variables: Dict[str, str] = {}, targets: List[str] = []
) -> str:
    """
    Create a Terraform plan for the specified workspace.

    Args:
        workspace: Terraform workspace name
        variables: Variables to pass to Terraform
        targets: Specific resources to target

    Returns:
        Plan output as string
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Create plan
        result = await executor.plan(variables, targets)

        if result.get("error"):
            raise Exception(f"Plan failed: {result['error']}")

        return result["output"]

    except Exception as e:
        logger.error(f"Terraform plan failed: {str(e)}")
        raise


async def apply_terraform(
    workspace: str, variables: Dict[str, str] = {}, targets: List[str] = []
) -> List[str]:
    """
    Apply Terraform configuration for the specified workspace.

    Args:
        workspace: Terraform workspace name
        variables: Variables to pass to Terraform
        targets: Specific resources to target

    Returns:
        List of applied resources
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Apply configuration
        result = await executor.apply(variables, targets)

        if result.get("error"):
            raise Exception(f"Apply failed: {result['error']}")

        # Get current state to see what was applied
        state_result = await executor.show()
        resources = state_result.get("resources", [])

        return [resource.get("address", "unknown") for resource in resources]

    except Exception as e:
        logger.error(f"Terraform apply failed: {str(e)}")
        raise


async def destroy_resources(workspace: str, targets: List[str] = []) -> List[str]:
    """
    Destroy Terraform resources in the specified workspace.

    Args:
        workspace: Terraform workspace name
        targets: Specific resources to destroy

    Returns:
        List of destroyed resources
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Get current state before destroy
        state_result = await executor.show()
        resources_before = state_result.get("resources", [])

        # Destroy resources
        result = await executor.destroy(targets)

        if result.get("error"):
            raise Exception(f"Destroy failed: {result['error']}")

        # Return list of destroyed resources
        return [resource.get("address", "unknown") for resource in resources_before]

    except Exception as e:
        logger.error(f"Terraform destroy failed: {str(e)}")
        raise


async def get_terraform_state(workspace: str) -> Dict[str, Any]:
    """
    Get current Terraform state for the specified workspace.

    Args:
        workspace: Terraform workspace name

    Returns:
        Current state information
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Get state
        result = await executor.show()

        return result

    except Exception as e:
        logger.error(f"Failed to get Terraform state: {str(e)}")
        raise


async def get_terraform_outputs(workspace: str) -> Dict[str, Any]:
    """
    Get Terraform outputs for the specified workspace.

    Args:
        workspace: Terraform workspace name

    Returns:
        Output values
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Get outputs
        result = await executor.output()

        return result.get("outputs", {})

    except Exception as e:
        logger.error(f"Failed to get Terraform outputs: {str(e)}")
        raise


async def validate_terraform_config(workspace: str) -> bool:
    """
    Validate Terraform configuration for the specified workspace.

    Args:
        workspace: Terraform workspace name

    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        executor = TerraformExecutor(workspace)

        # Initialize if needed
        await executor.init()

        # Validate configuration
        result = await executor.validate()

        return result.get("valid", False)

    except Exception as e:
        logger.error(f"Terraform validation failed: {str(e)}")
        return False
