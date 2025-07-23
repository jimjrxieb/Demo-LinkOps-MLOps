import logging
import os
import smtplib
from email.mime.text import MIMEText
from http.client import HTTPException

import requests
from demo_client_audits.api.confluence import push_to_confluence
from demo_db.db import save_ml_model
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO)


def generate_agent(agent_name: str, backlog_url: str, email_to: str):
    try:
        env = Environment(loader=FileSystemLoader("ml-creator/templates"))
        template = env.get_template("agent_backlog_scanner.py.jinja")

        agent_code = template.render(
            agent_name=agent_name, backlog_url=backlog_url, email_to=email_to
        )

        os.makedirs("demo-db/ml-models/agents", exist_ok=True)
        agent_path = f"demo-db/ml-models/agents/{agent_name}.py"
        with open(agent_path, "w") as f:
            f.write(agent_code)

        # Execute via demo-jamesos
        response = requests.post(
            "http://demo-jamesos:8003/rank_task",
            json={"task": agent_name, "category": "agent", "agent_path": agent_path},
        )
        report = response.json().get("report", "No report generated")

        # Send email
        send_email(email_to, report)

        # Push to Confluence
        report_path = f"demo-db/ml-models/agents/{agent_name}_report.md"
        with open(report_path, "w") as f:
            f.write(report)
        push_to_confluence(agent_name, report_path, f"Agent Report - {agent_name}")

        save_ml_model(
            agent_name,
            {
                "data": {"agent_type": "backlog_scanner", "backlog_url": backlog_url},
                "training_history": [],
            },
        )

        logging.info(f"Generated agent {agent_name} at {agent_path}")
        return {"agent_name": agent_name, "path": agent_path, "report": report}
    except Exception as e:
        logging.error(f"Agent generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent generation failed: {e}")


def send_email(email_to: str, report: str):
    try:
        msg = MIMEText(report)
        msg["Subject"] = "Backlog Report"
        msg["From"] = os.getenv("SMTP_FROM")
        msg["To"] = email_to

        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)
        logging.info(f"Email sent to {email_to}")
    except Exception as e:
        logging.error(f"Email sending failed: {e}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")
