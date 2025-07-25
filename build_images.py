#!/usr/bin/env python3
"""
Docker image builder and pusher for DEMO-LinkOps.

This script builds all Docker images for the microservices and optionally
pushes them to a Docker registry using credentials from environment variables.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DockerImageBuilder:
    """Docker image builder for DEMO-LinkOps microservices."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.registry_user = os.getenv("DOCKER_USER")
        self.registry_password = os.getenv("DOCKER_CRED")

        # Define services and their build contexts
        self.services = {
            "demo-linkops-rag": "./rag",
            "demo-linkops-ml-models": "./ml-models",
            "demo-linkops-pipeline": "./pipeline",
            "demo-linkops-sync-engine": "./sync_engine",
            "demo-linkops-unified-api": "./unified-api",
            "demo-linkops-frontend": "./frontend",
        }

    def run_command(
        self, cmd: List[str], description: str, timeout: int = 300
    ) -> Tuple[bool, str, str]:
        """Run a command and return success status, stdout, stderr."""
        try:
            logger.info(f"🔧 {description}...")
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            success = result.returncode == 0
            if success:
                logger.info(f"✅ {description} completed successfully")
            else:
                logger.error(f"❌ {description} failed")
                logger.error(f"Error output: {result.stderr}")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            logger.error(f"❌ {description} timed out")
            return False, "", "Command timed out"
        except Exception as e:
            logger.error(f"❌ {description} failed: {e}")
            return False, "", str(e)

    def docker_login(self) -> bool:
        """Login to Docker registry if credentials are available."""
        if not self.registry_user or not self.registry_password:
            logger.warning("⚠️  Docker registry credentials not found in environment")
            logger.info(
                "Set DOCKER_USER and DOCKER_CRED environment variables to enable pushing"
            )
            return False

        success, _, stderr = self.run_command(
            ["docker", "login", "-u", self.registry_user, "--password-stdin"],
            "Logging into Docker registry",
        )

        if success:
            logger.info("✅ Docker registry login successful")
        else:
            logger.error(f"❌ Docker registry login failed: {stderr}")

        return success

    def build_image(self, service_name: str, build_context: str) -> bool:
        """Build a Docker image for a service."""
        dockerfile_path = Path(self.project_root) / build_context / "Dockerfile"

        if not dockerfile_path.exists():
            logger.error(
                f"❌ Dockerfile not found for {service_name}: {dockerfile_path}"
            )
            return False

        # Build image with latest tag
        tag = f"{service_name}:latest"
        if self.registry_user:
            tag = f"{self.registry_user}/{tag}"

        success, stdout, stderr = self.run_command(
            ["docker", "build", "-t", tag, build_context],
            f"Building {service_name}",
            timeout=600,  # 10 minutes for build
        )

        if success:
            logger.info(f"✅ Successfully built {tag}")
        else:
            logger.error(f"❌ Failed to build {service_name}")
            logger.error(f"Build output: {stderr}")

        return success

    def push_image(self, service_name: str) -> bool:
        """Push a Docker image to registry."""
        if not self.registry_user:
            logger.warning(f"⚠️  Skipping push for {service_name} - no registry user")
            return True

        tag = f"{self.registry_user}/{service_name}:latest"

        success, stdout, stderr = self.run_command(
            ["docker", "push", tag],
            f"Pushing {service_name}",
            timeout=600,  # 10 minutes for push
        )

        if success:
            logger.info(f"✅ Successfully pushed {tag}")
        else:
            logger.error(f"❌ Failed to push {service_name}")
            logger.error(f"Push output: {stderr}")

        return success

    def build_all_images(self, push: bool = False) -> Dict[str, bool]:
        """Build all Docker images."""
        logger.info("🚀 Starting Docker image build process...")

        results = {}

        # Login if pushing
        login_success = True
        if push:
            login_success = self.docker_login()
            if not login_success:
                logger.error("❌ Docker login failed, skipping push operations")
                push = False

        # Build each service
        for service_name, build_context in self.services.items():
            logger.info(f"📦 Building {service_name}...")

            build_success = self.build_image(service_name, build_context)
            results[service_name] = build_success

            if build_success and push and login_success:
                push_success = self.push_image(service_name)
                results[f"{service_name}_push"] = push_success
            elif not build_success:
                logger.error(
                    f"❌ Skipping push for {service_name} due to build failure"
                )

        return results

    def print_summary(self, results: Dict[str, bool]) -> None:
        """Print build summary."""
        logger.info("📊 Build Summary:")
        logger.info("=" * 50)

        total_builds = len(self.services)
        successful_builds = sum(
            1 for k, v in results.items() if not k.endswith("_push") and v
        )
        failed_builds = total_builds - successful_builds

        logger.info(f"🏗️  Total builds: {total_builds}")
        logger.info(f"✅ Successful: {successful_builds}")
        logger.info(f"❌ Failed: {failed_builds}")

        if any(k.endswith("_push") for k in results.keys()):
            total_pushes = sum(1 for k in results.keys() if k.endswith("_push"))
            successful_pushes = sum(
                1 for k, v in results.items() if k.endswith("_push") and v
            )
            failed_pushes = total_pushes - successful_pushes

            logger.info(f"📤 Total pushes: {total_pushes}")
            logger.info(f"✅ Successful pushes: {successful_pushes}")
            logger.info(f"❌ Failed pushes: {failed_pushes}")

        logger.info("=" * 50)

        # List failed services
        failed_services = [
            k for k, v in results.items() if not k.endswith("_push") and not v
        ]
        if failed_services:
            logger.error("❌ Failed builds:")
            for service in failed_services:
                logger.error(f"   - {service}")

        failed_pushes = [
            k.replace("_push", "")
            for k, v in results.items()
            if k.endswith("_push") and not v
        ]
        if failed_pushes:
            logger.error("❌ Failed pushes:")
            for service in failed_pushes:
                logger.error(f"   - {service}")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent

    # Parse command line arguments
    push = "--push" in sys.argv

    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("❌ Docker is not installed or not available")
        return False

    # Build images
    builder = DockerImageBuilder(project_root)
    results = builder.build_all_images(push=push)

    # Print summary
    builder.print_summary(results)

    # Return success if all builds succeeded
    all_builds_successful = all(
        v for k, v in results.items() if not k.endswith("_push")
    )

    if all_builds_successful:
        logger.info("🎉 All Docker images built successfully!")
        return True
    else:
        logger.error("❌ Some Docker images failed to build")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("Usage: python3 build_images.py [--push]")
        print("")
        print("Options:")
        print("  --push    Push images to Docker registry after building")
        print("            Requires DOCKER_USER and DOCKER_CRED environment variables")
        print("")
        print("Environment Variables:")
        print("  DOCKER_USER    Docker registry username")
        print("  DOCKER_CRED    Docker registry password/token")
        sys.exit(0)

    success = main()
    sys.exit(0 if success else 1)
