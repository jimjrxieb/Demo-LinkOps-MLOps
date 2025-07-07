"""
Pipeline management logic for the Platform Engineer AI Agent.
Handles pipeline creation, updates, and health analysis.
"""

import logging
import yaml
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PipelineManager:
    """Manages CI/CD pipeline configurations and operations."""

    def __init__(self, platform: str = "github"):
        self.platform = platform
        self.pipeline_templates = self._load_pipeline_templates()

    def _load_pipeline_templates(self) -> Dict[str, Any]:
        """Load pipeline templates for different platforms."""
        templates = {
            "github": {
                "basic": {
                    "name": "Basic CI/CD",
                    "on": {
                        "push": {"branches": ["main"]},
                        "pull_request": {"branches": ["main"]},
                    },
                    "jobs": {
                        "build": {
                            "runs-on": "ubuntu-latest",
                            "steps": [
                                {"name": "Checkout", "uses": "actions/checkout@v3"},
                                {
                                    "name": "Setup Node.js",
                                    "uses": "actions/setup-node@v3",
                                    "with": {"node-version": "16"},
                                },
                                {"name": "Install dependencies", "run": "npm ci"},
                                {"name": "Run tests", "run": "npm test"},
                                {"name": "Build", "run": "npm run build"},
                            ],
                        }
                    },
                },
                "docker": {
                    "name": "Docker CI/CD",
                    "on": {
                        "push": {"branches": ["main"]},
                        "pull_request": {"branches": ["main"]},
                    },
                    "jobs": {
                        "build": {
                            "runs-on": "ubuntu-latest",
                            "steps": [
                                {"name": "Checkout", "uses": "actions/checkout@v3"},
                                {
                                    "name": "Set up Docker Buildx",
                                    "uses": "docker/setup-buildx-action@v2",
                                },
                                {
                                    "name": "Build and push",
                                    "uses": "docker/build-push-action@v4",
                                    "with": {
                                        "context": ".",
                                        "push": "true",
                                        "tags": "${{ github.repository }}:${{ github.sha }}",
                                    },
                                },
                            ],
                        }
                    },
                },
            },
            "gitlab": {
                "basic": {
                    "stages": ["build", "test", "deploy"],
                    "build": {
                        "stage": "build",
                        "script": ["npm ci", "npm run build"],
                        "only": ["main"],
                    },
                    "test": {"stage": "test", "script": ["npm test"], "only": ["main"]},
                    "deploy": {
                        "stage": "deploy",
                        "script": ["echo 'Deploying...'"],
                        "only": ["main"],
                    },
                }
            },
            "jenkins": {
                "basic": {
                    "pipeline": {
                        "agent": "any",
                        "stages": [
                            {"stage": "Build", "steps": [{"sh": "npm ci"}]},
                            {"stage": "Test", "steps": [{"sh": "npm test"}]},
                            {
                                "stage": "Deploy",
                                "steps": [{"sh": "echo 'Deploying...'"}],
                            },
                        ],
                    }
                }
            },
        }
        return templates

    async def create_pipeline(
        self,
        name: str,
        repo_url: str,
        branch: str = "main",
        environment: str = "production",
        variables: Dict[str, str] = {},
        template: str = "basic",
    ) -> Dict[str, Any]:
        """
        Create a new pipeline configuration.

        Args:
            name: Pipeline name
            repo_url: Repository URL
            branch: Default branch
            environment: Target environment
            variables: Pipeline variables
            template: Template to use

        Returns:
            Pipeline configuration
        """
        try:
            # Get template
            if self.platform not in self.pipeline_templates:
                raise ValueError(f"Unsupported platform: {self.platform}")

            if template not in self.pipeline_templates[self.platform]:
                raise ValueError(
                    f"Template {template} not found for platform {self.platform}"
                )

            template_config = self.pipeline_templates[self.platform][template]

            # Customize template
            config = self._customize_template(
                template_config,
                name=name,
                repo_url=repo_url,
                branch=branch,
                environment=environment,
                variables=variables,
            )

            # Generate pipeline file
            pipeline_file = await self._generate_pipeline_file(config)

            return {
                "name": name,
                "platform": self.platform,
                "template": template,
                "config": config,
                "pipeline_file": pipeline_file,
                "created_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Pipeline creation failed: {str(e)}")
            raise

    async def update_pipeline(
        self,
        name: str,
        repo_url: str,
        branch: str = "main",
        environment: str = "production",
        variables: Dict[str, str] = {},
        template: str = "basic",
    ) -> Dict[str, Any]:
        """
        Update an existing pipeline configuration.

        Args:
            name: Pipeline name
            repo_url: Repository URL
            branch: Default branch
            environment: Target environment
            variables: Pipeline variables
            template: Template to use

        Returns:
            Updated pipeline configuration
        """
        try:
            # Create new configuration (same as create for now)
            config = await self.create_pipeline(
                name=name,
                repo_url=repo_url,
                branch=branch,
                environment=environment,
                variables=variables,
                template=template,
            )

            config["updated_at"] = datetime.now().isoformat()
            config["action"] = "updated"

            return config

        except Exception as e:
            logger.error(f"Pipeline update failed: {str(e)}")
            raise

    async def analyze_pipeline_health(
        self, pipeline_id: str, time_range: str = "7d"
    ) -> Dict[str, Any]:
        """
        Analyze pipeline health and provide recommendations.

        Args:
            pipeline_id: Pipeline identifier
            time_range: Time range for analysis ("1d", "7d", "30d")

        Returns:
            Health analysis results
        """
        try:
            # Parse time range
            days = self._parse_time_range(time_range)

            # Get pipeline runs for the time period
            runs = await self._get_pipeline_runs(pipeline_id, days)

            # Calculate metrics
            total_runs = len(runs)
            successful_runs = len([r for r in runs if r.get("status") == "success"])
            failed_runs = len([r for r in runs if r.get("status") == "failure"])

            success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0

            # Calculate average duration
            durations = [r.get("duration", 0) for r in runs if r.get("duration")]
            avg_duration = sum(durations) / len(durations) if durations else 0

            # Identify failure points
            failure_points = self._identify_failure_points(runs)

            # Generate recommendations
            recommendations = self._generate_recommendations(
                success_rate, avg_duration, failure_points, total_runs
            )

            return {
                "pipeline_id": pipeline_id,
                "time_range": time_range,
                "total_runs": total_runs,
                "successful_runs": successful_runs,
                "failed_runs": failed_runs,
                "success_rate": success_rate,
                "avg_duration": avg_duration,
                "failure_points": failure_points,
                "recommendations": recommendations,
                "analyzed_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Pipeline health analysis failed: {str(e)}")
            raise

    def _customize_template(
        self,
        template: Dict[str, Any],
        name: str,
        repo_url: str,
        branch: str,
        environment: str,
        variables: Dict[str, str],
    ) -> Dict[str, Any]:
        """Customize template with specific parameters."""
        config = template.copy()

        # Add variables to configuration
        if self.platform == "github":
            # Add environment variables to GitHub Actions
            if "jobs" in config:
                for job_name, job_config in config["jobs"].items():
                    if "steps" in job_config:
                        # Add environment variables to each step
                        for step in job_config["steps"]:
                            if "env" not in step:
                                step["env"] = {}
                            step["env"].update(variables)
                            step["env"]["ENVIRONMENT"] = environment
                            step["env"]["BRANCH"] = branch

        elif self.platform == "gitlab":
            # Add variables to GitLab CI
            config["variables"] = variables
            config["variables"]["ENVIRONMENT"] = environment
            config["variables"]["BRANCH"] = branch

        elif self.platform == "jenkins":
            # Add environment variables to Jenkins pipeline
            if "pipeline" in config and "environment" not in config["pipeline"]:
                config["pipeline"]["environment"] = {}
            config["pipeline"]["environment"].update(variables)
            config["pipeline"]["environment"]["ENVIRONMENT"] = environment
            config["pipeline"]["environment"]["BRANCH"] = branch

        return config

    async def _generate_pipeline_file(self, config: Dict[str, Any]) -> str:
        """Generate pipeline configuration file content."""
        try:
            if self.platform == "github":
                # Generate GitHub Actions workflow file
                content = yaml.dump(config, default_flow_style=False, sort_keys=False)
                return content

            elif self.platform == "gitlab":
                # Generate GitLab CI configuration
                content = yaml.dump(config, default_flow_style=False, sort_keys=False)
                return content

            elif self.platform == "jenkins":
                # Generate Jenkinsfile
                content = self._generate_jenkinsfile(config)
                return content

            else:
                raise ValueError(f"Unsupported platform: {self.platform}")

        except Exception as e:
            logger.error(f"Failed to generate pipeline file: {str(e)}")
            raise

    def _generate_jenkinsfile(self, config: Dict[str, Any]) -> str:
        """Generate Jenkinsfile content."""
        try:
            pipeline = config.get("pipeline", {})
            stages = pipeline.get("stages", [])

            jenkinsfile = "pipeline {\n"
            jenkinsfile += f"    agent {pipeline.get('agent', 'any')}\n\n"

            # Add environment variables
            if "environment" in pipeline:
                jenkinsfile += "    environment {\n"
                for key, value in pipeline["environment"].items():
                    jenkinsfile += f"        {key} = '{value}'\n"
                jenkinsfile += "    }\n\n"

            # Add stages
            jenkinsfile += "    stages {\n"
            for stage in stages:
                stage_name = stage.get("stage", "Unknown")
                steps = stage.get("steps", [])

                jenkinsfile += f"        stage('{stage_name}') {{\n"
                jenkinsfile += "            steps {\n"

                for step in steps:
                    if "sh" in step:
                        jenkinsfile += f"                sh '{step['sh']}'\n"
                    elif "echo" in step:
                        jenkinsfile += f"                echo '{step['echo']}'\n"

                jenkinsfile += "            }\n"
                jenkinsfile += "        }\n"

            jenkinsfile += "    }\n"
            jenkinsfile += "}\n"

            return jenkinsfile

        except Exception as e:
            logger.error(f"Failed to generate Jenkinsfile: {str(e)}")
            raise

    def _parse_time_range(self, time_range: str) -> int:
        """Parse time range string to number of days."""
        if time_range.endswith("d"):
            return int(time_range[:-1])
        elif time_range.endswith("h"):
            return int(time_range[:-1]) // 24
        elif time_range.endswith("w"):
            return int(time_range[:-1]) * 7
        else:
            return 7  # Default to 7 days

    async def _get_pipeline_runs(
        self, pipeline_id: str, days: int
    ) -> List[Dict[str, Any]]:
        """Get pipeline runs for the specified time period."""
        try:
            # This would integrate with actual CI platform APIs
            # For now, return mock data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            mock_runs = []
            for i in range(10):  # Mock 10 runs
                run_date = start_date + timedelta(days=i)
                mock_runs.append(
                    {
                        "id": f"run_{i}",
                        "status": "success" if i % 3 != 0 else "failure",
                        "duration": 300 + (i * 30),  # 5-8 minutes
                        "created_at": run_date.isoformat(),
                        "branch": "main",
                        "commit": f"abc123{i}",
                    }
                )

            return mock_runs

        except Exception as e:
            logger.error(f"Failed to get pipeline runs: {str(e)}")
            return []

    def _identify_failure_points(self, runs: List[Dict[str, Any]]) -> List[str]:
        """Identify common failure points in pipeline runs."""
        failure_points = []

        # Analyze failed runs
        failed_runs = [r for r in runs if r.get("status") == "failure"]

        if len(failed_runs) > len(runs) * 0.3:  # More than 30% failure rate
            failure_points.append("High failure rate - investigate root cause")

        # Check for timing issues
        long_runs = [
            r for r in runs if r.get("duration", 0) > 600
        ]  # Longer than 10 minutes
        if len(long_runs) > len(runs) * 0.2:  # More than 20% are slow
            failure_points.append("Slow pipeline execution - optimize build steps")

        # Check for specific failure patterns
        if any("test" in str(r).lower() for r in failed_runs):
            failure_points.append("Test failures - review test suite")

        if any("build" in str(r).lower() for r in failed_runs):
            failure_points.append(
                "Build failures - check dependencies and configuration"
            )

        return failure_points

    def _generate_recommendations(
        self,
        success_rate: float,
        avg_duration: float,
        failure_points: List[str],
        total_runs: int,
    ) -> List[str]:
        """Generate recommendations based on pipeline health metrics."""
        recommendations = []

        if success_rate < 80:
            recommendations.append(
                "Implement automated testing to improve success rate"
            )
            recommendations.append("Add pre-commit hooks to catch issues early")

        if avg_duration > 600:  # Longer than 10 minutes
            recommendations.append("Optimize build steps to reduce execution time")
            recommendations.append("Consider parallel job execution")
            recommendations.append("Cache dependencies to speed up builds")

        if total_runs < 5:
            recommendations.append("Increase pipeline usage to gather more metrics")

        if "High failure rate" in str(failure_points):
            recommendations.append(
                "Set up monitoring and alerting for pipeline failures"
            )
            recommendations.append(
                "Implement rollback strategies for failed deployments"
            )

        if "Test failures" in str(failure_points):
            recommendations.append("Review and update test suite")
            recommendations.append("Add flaky test detection and handling")

        if "Build failures" in str(failure_points):
            recommendations.append(
                "Pin dependency versions to prevent breaking changes"
            )
            recommendations.append("Implement dependency vulnerability scanning")

        return recommendations


# Main functions for the API
async def create_pipeline(
    name: str,
    repo_url: str,
    branch: str = "main",
    environment: str = "production",
    variables: Dict[str, str] = {},
    platform: str = "github",
) -> Dict[str, Any]:
    """
    Create a new pipeline configuration.

    Args:
        name: Pipeline name
        repo_url: Repository URL
        branch: Default branch
        environment: Target environment
        variables: Pipeline variables
        platform: CI platform to use

    Returns:
        Pipeline configuration
    """
    try:
        manager = PipelineManager(platform)
        return await manager.create_pipeline(
            name=name,
            repo_url=repo_url,
            branch=branch,
            environment=environment,
            variables=variables,
        )
    except Exception as e:
        logger.error(f"Pipeline creation failed: {str(e)}")
        raise


async def update_pipeline(
    name: str,
    repo_url: str,
    branch: str = "main",
    environment: str = "production",
    variables: Dict[str, str] = {},
    platform: str = "github",
) -> Dict[str, Any]:
    """
    Update an existing pipeline configuration.

    Args:
        name: Pipeline name
        repo_url: Repository URL
        branch: Default branch
        environment: Target environment
        variables: Pipeline variables
        platform: CI platform to use

    Returns:
        Updated pipeline configuration
    """
    try:
        manager = PipelineManager(platform)
        return await manager.update_pipeline(
            name=name,
            repo_url=repo_url,
            branch=branch,
            environment=environment,
            variables=variables,
        )
    except Exception as e:
        logger.error(f"Pipeline update failed: {str(e)}")
        raise


async def analyze_pipeline_health(
    pipeline_id: str, time_range: str = "7d"
) -> Dict[str, Any]:
    """
    Analyze pipeline health and provide recommendations.

    Args:
        pipeline_id: Pipeline identifier
        time_range: Time range for analysis

    Returns:
        Health analysis results
    """
    try:
        # Determine platform from pipeline ID
        platform = "github"  # Default, could be parsed from pipeline_id

        manager = PipelineManager(platform)
        return await manager.analyze_pipeline_health(pipeline_id, time_range)
    except Exception as e:
        logger.error(f"Pipeline health analysis failed: {str(e)}")
        raise
