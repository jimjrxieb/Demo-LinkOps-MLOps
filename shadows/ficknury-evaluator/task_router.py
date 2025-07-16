import logging
from typing import Optional

from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Task(BaseModel):
    task_id: str
    title: str
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    tags: Optional[list] = []


class AutonomyEvaluation(BaseModel):
    task_id: str
    autonomous: bool
    confidence: float
    reasoning: str
    required_capabilities: list[str]
    automation_feasibility: str
    recommendations: list[str]


class AutonomyEvaluator:
    """
    Evaluates whether tasks can be 100% completed autonomously using AI/ML, orbs, and runes.
    Does NOT route tasks - only assesses automation feasibility.
    """

    def __init__(self):
        self.autonomous_patterns = {
            # Infrastructure tasks that can be fully automated
            "kubernetes": [
                "deploy",
                "scale",
                "rollback",
                "create",
                "delete",
                "update",
                "patch",
            ],
            "docker": ["build", "push", "pull", "run", "stop", "remove"],
            "helm": ["install", "upgrade", "rollback", "uninstall", "package"],
            "terraform": ["plan", "apply", "destroy", "init", "validate"],
            "security": ["scan", "audit", "compliance", "vulnerability", "cve"],
            "monitoring": ["metrics", "logs", "alerts", "dashboards"],
            "ci_cd": ["pipeline", "workflow", "build", "test", "deploy"],
            "database": ["backup", "restore", "migration", "optimization"],
            "networking": ["firewall", "load-balancer", "dns", "proxy"],
            "configuration": ["config", "environment", "secrets", "variables"],
        }

        self.non_autonomous_patterns = {
            # Tasks that require human intervention or external dependencies
            "business": ["strategy", "planning", "budget", "vendor", "contract"],
            "human": [
                "interview",
                "meeting",
                "presentation",
                "training",
                "communication",
            ],
            "physical": ["hardware", "datacenter", "cable", "physical"],
            "creative": ["design", "branding", "marketing", "content creation"],
            "legal": ["compliance", "legal", "licensing", "gdpr", "privacy"],
            "manual": ["manual", "human", "approval", "sign-off", "verification"],
            "external": ["third-party", "vendor", "external", "procurement"],
        }

        self.ai_capabilities = [
            "code_generation",
            "configuration_management",
            "infrastructure_as_code",
            "security_scanning",
            "log_analysis",
            "metric_monitoring",
            "automated_testing",
            "deployment_automation",
            "troubleshooting",
            "documentation_generation",
        ]

    def evaluate_autonomy(self, task: Task) -> AutonomyEvaluation:
        """
        Evaluate if a task can be 100% completed autonomously.

        Args:
            task: Task to evaluate

        Returns:
            AutonomyEvaluation with feasibility assessment
        """
        logger.info(f"Evaluating autonomy for task: {task.task_id}")

        description_lower = task.description.lower()
        title_lower = task.title.lower()
        combined_text = f"{title_lower} {description_lower}"

        # Check for autonomous patterns
        autonomous_score = self._calculate_autonomous_score(combined_text)

        # Check for non-autonomous patterns
        non_autonomous_score = self._calculate_non_autonomous_score(combined_text)

        # Determine required capabilities
        required_capabilities = self._identify_required_capabilities(combined_text)

        # Calculate final autonomy assessment
        net_score = autonomous_score - non_autonomous_score

        # Determine if task is autonomous
        is_autonomous = net_score >= 0.3 and non_autonomous_score < 0.5

        # Generate reasoning
        reasoning = self._generate_reasoning(
            autonomous_score, non_autonomous_score, required_capabilities, is_autonomous
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            is_autonomous, required_capabilities, task
        )

        # Determine automation feasibility
        if is_autonomous and autonomous_score >= 0.7:
            feasibility = "high"
        elif is_autonomous and autonomous_score >= 0.4:
            feasibility = "medium"
        elif non_autonomous_score >= 0.5:
            feasibility = "low"
        else:
            feasibility = "uncertain"

        evaluation = AutonomyEvaluation(
            task_id=task.task_id,
            autonomous=is_autonomous,
            confidence=max(autonomous_score, non_autonomous_score),
            reasoning=reasoning,
            required_capabilities=required_capabilities,
            automation_feasibility=feasibility,
            recommendations=recommendations,
        )

        logger.info(
            f"Autonomy evaluation complete. Autonomous: {is_autonomous}, Feasibility: {feasibility}"
        )
        return evaluation

    def _calculate_autonomous_score(self, text: str) -> float:
        """Calculate how well the task matches autonomous patterns"""
        total_matches = 0
        total_patterns = 0

        for category, patterns in self.autonomous_patterns.items():
            total_patterns += len(patterns)
            category_matches = sum(1 for pattern in patterns if pattern in text)
            total_matches += category_matches

            # Boost score if category is mentioned
            if category.replace("_", "-") in text or category.replace("_", " ") in text:
                total_matches += 0.5

        return min(total_matches / total_patterns, 1.0) if total_patterns > 0 else 0.0

    def _calculate_non_autonomous_score(self, text: str) -> float:
        """Calculate how well the task matches non-autonomous patterns"""
        total_matches = 0
        total_patterns = 0

        for category, patterns in self.non_autonomous_patterns.items():
            total_patterns += len(patterns)
            category_matches = sum(1 for pattern in patterns if pattern in text)
            total_matches += category_matches

            # Heavy penalty if category is mentioned
            if category.replace("_", "-") in text or category.replace("_", " ") in text:
                total_matches += 1.0

        return min(total_matches / total_patterns, 1.0) if total_patterns > 0 else 0.0

    def _identify_required_capabilities(self, text: str) -> list[str]:
        """Identify which AI capabilities are required for the task"""
        required = []

        capability_keywords = {
            "code_generation": ["code", "script", "program", "develop", "implement"],
            "configuration_management": ["config", "configure", "setup", "environment"],
            "infrastructure_as_code": [
                "terraform",
                "cloudformation",
                "infrastructure",
                "iac",
            ],
            "security_scanning": [
                "security",
                "scan",
                "vulnerability",
                "cve",
                "compliance",
            ],
            "log_analysis": ["logs", "logging", "analysis", "troubleshoot", "debug"],
            "metric_monitoring": [
                "metrics",
                "monitor",
                "alert",
                "dashboard",
                "observability",
            ],
            "automated_testing": ["test", "testing", "validation", "verify", "check"],
            "deployment_automation": ["deploy", "deployment", "release", "rollout"],
            "troubleshooting": ["troubleshoot", "debug", "fix", "resolve", "issue"],
            "documentation_generation": [
                "document",
                "documentation",
                "readme",
                "guide",
            ],
        }

        for capability, keywords in capability_keywords.items():
            if any(keyword in text for keyword in keywords):
                required.append(capability)

        return required

    def _generate_reasoning(
        self,
        autonomous_score: float,
        non_autonomous_score: float,
        capabilities: list[str],
        is_autonomous: bool,
    ) -> str:
        """Generate human-readable reasoning for the autonomy decision"""
        if is_autonomous:
            if autonomous_score >= 0.7:
                reason = f"High automation potential (score: {autonomous_score:.2f}). "
            else:
                reason = (
                    f"Moderate automation potential (score: {autonomous_score:.2f}). "
                )

            reason += f"Task involves {len(capabilities)} automatable capabilities: {', '.join(capabilities[:3])}."

            if non_autonomous_score > 0.2:
                reason += f" Some manual aspects detected (score: {non_autonomous_score:.2f}) but still automatable."
        else:
            if non_autonomous_score >= 0.5:
                reason = f"Requires human intervention (manual score: {non_autonomous_score:.2f}). "
            else:
                reason = f"Low automation confidence (autonomous score: {autonomous_score:.2f}). "

            reason += "Task may involve business decisions, human interaction, or external dependencies."

        return reason

    def _generate_recommendations(
        self, is_autonomous: bool, capabilities: list[str], task: Task
    ) -> list[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if is_autonomous:
            recommendations.append("✅ Proceed with Whis training pipeline")
            recommendations.append(
                "🤖 Can be fully automated using AI/ML + orbs + runes"
            )

            if "code_generation" in capabilities:
                recommendations.append("📝 Generate code templates and scripts")
            if "configuration_management" in capabilities:
                recommendations.append("⚙️ Create configuration manifests")
            if "security_scanning" in capabilities:
                recommendations.append("🔒 Include automated security checks")
        else:
            recommendations.append(
                "❌ Requires human intervention - not fully autonomous"
            )
            recommendations.append(
                "👥 Consider breaking down into smaller, automatable tasks"
            )
            recommendations.append("🔄 Flag for deploy agent or manual execution")

            if task.priority == "high":
                recommendations.append("⚡ High priority - prioritize for deploy agent")

        return recommendations


# Global evaluator instance
autonomy_evaluator = AutonomyEvaluator()


async def evaluate_task(task: Task) -> AutonomyEvaluation:
    """
    Evaluate if a task can be completed 100% autonomously.
    This is complementary to the 70% orb confidence system.
    """
    return autonomy_evaluator.evaluate_autonomy(task)
