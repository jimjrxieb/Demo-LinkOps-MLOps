#!/usr/bin/env python3
"""
Security Verification Report for LinkOps-MLOps
Verifies that all high-priority security fixes have been applied
"""

import json
import os
import re
from typing import Dict, Tuple

# Security requirements to verify
REQUIRED_VERSIONS = {
    "protobuf": "4.25.8",
    "zipp": "3.19.1",
    "requests": "2.32.4",
    "urllib3": "2.5.0",
    "fastapi": "0.109.1",
    "uvicorn": "0.29.0",
    "httpx": "0.27.0",
    "pydantic": "2.7.1",
    "anyio": "4.4.0",
    "python-multipart": "0.0.19",
}

JS_REQUIRED_VERSIONS = {"axios": "1.7.4", "vue": "3.5.10", "vite": "5.4.8"}


def parse_version(version_str: str) -> Tuple[int, ...]:
    """Parse version string into tuple for comparison"""
    return tuple(map(int, re.findall(r"\d+", version_str)))


def check_requirements_file(file_path: str) -> Dict[str, str]:
    """Check a requirements.txt file for security compliance"""
    results = {}

    if not os.path.exists(file_path):
        return {"ERROR": "File not found"}

    try:
        with open(file_path, "r") as f:
            content = f.read()

        for package, min_version in REQUIRED_VERSIONS.items():
            # Look for package in file
            pattern = rf"{package}([>=<!=]+)([\d\.]+)"
            match = re.search(pattern, content)

            if match:
                operator, version = match.groups()
                if operator.startswith(">="):
                    if parse_version(version) >= parse_version(min_version):
                        results[package] = f"✅ {version} (>= {min_version})"
                    else:
                        results[package] = f"❌ {version} (< {min_version})"
                elif operator == "==":
                    if parse_version(version) >= parse_version(min_version):
                        results[package] = f"✅ {version} (fixed version)"
                    else:
                        results[package] = f"❌ {version} (< {min_version})"
            else:
                results[package] = "⚠️ Not found"

    except Exception as e:
        results["ERROR"] = str(e)

    return results


def check_package_json(file_path: str) -> Dict[str, str]:
    """Check package.json for security compliance"""
    results = {}

    if not os.path.exists(file_path):
        return {"ERROR": "File not found"}

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        all_deps = {}
        if "dependencies" in data:
            all_deps.update(data["dependencies"])
        if "devDependencies" in data:
            all_deps.update(data["devDependencies"])

        for package, min_version in JS_REQUIRED_VERSIONS.items():
            if package in all_deps:
                current_version = all_deps[package].replace("^", "").replace("~", "")
                if parse_version(current_version) >= parse_version(min_version):
                    results[package] = f"✅ {current_version}"
                else:
                    results[package] = f"❌ {current_version} (< {min_version})"
            else:
                results[package] = "⚠️ Not found"

    except Exception as e:
        results["ERROR"] = str(e)

    return results


def main():
    """Generate security verification report"""
    print("🔒 LinkOps-MLOps Security Verification Report")
    print("=" * 60)

    # All services to check
    services = [
        "./mlops/whis_smithing/requirements.txt",
        "./mlops/mlops_utils/requirements.txt",
        "./mlops/whis_sanitize/requirements.txt",
        "./mlops/whis_logic/requirements.txt",
        "./mlops/whis_webscraper/requirements.txt",
        "./mlops/audit_assess/requirements.txt",
        "./mlops/whis_enhance/requirements.txt",
        "./mlops/whis_data_input/requirements.txt",
        "./mlops/mlops_platform/requirements.txt",
        "./mlops/audit_migrate/requirements.txt",
        "./shadows/jimmie_logic/requirements.txt",
        "./shadows/devops_engineer/requirements.txt",
        "./shadows/platform_engineer/requirements.txt",
        "./shadows/audit_logic/requirements.txt",
        "./shadows/ficknury_evaluator/requirements.txt",
        "./shadows/ml_data_scientist/requirements.txt",
        "./shadows/kubernetes_specialist/requirements.txt",
    ]

    compliant_services = 0
    total_services = 0

    print("\n📋 Python Services Security Status:")
    print("-" * 40)

    for service_file in services:
        if os.path.exists(service_file):
            total_services += 1
            service_name = (
                service_file.replace("./mlops/", "")
                .replace("./shadows/", "")
                .replace("/requirements.txt", "")
            )
            print(f"\n🔍 {service_name}")

            results = check_requirements_file(service_file)

            service_compliant = True
            for package, status in results.items():
                if package != "ERROR":
                    print(f"  {status}")
                    if "❌" in status:
                        service_compliant = False
                else:
                    print(f"  ❌ Error: {status}")
                    service_compliant = False

            if service_compliant:
                compliant_services += 1
                print("  🎉 Service is security compliant")
            else:
                print("  ⚠️ Service needs attention")

    print("\n📊 JavaScript Frontend Security Status:")
    print("-" * 40)

    frontend_results = check_package_json("./frontend/package.json")
    print("\n🔍 Frontend")

    frontend_compliant = True
    for package, status in frontend_results.items():
        if package != "ERROR":
            print(f"  {status}")
            if "❌" in status:
                frontend_compliant = False
        else:
            print(f"  ❌ Error: {status}")
            frontend_compliant = False

    if frontend_compliant:
        print("  🎉 Frontend is security compliant")
    else:
        print("  ⚠️ Frontend needs attention")

    print("\n📈 Overall Security Summary:")
    print("=" * 60)
    print(f"✅ Python Services Compliant: {compliant_services}/{total_services}")
    print(f"✅ Frontend Compliant: {'Yes' if frontend_compliant else 'No'}")

    overall_compliance = (compliant_services == total_services) and frontend_compliant

    if overall_compliance:
        print("🎉 ALL SERVICES ARE SECURITY COMPLIANT!")
        print("🛡️ Platform is protected against known vulnerabilities")
    else:
        print("⚠️ Some services still need security updates")

    return 0 if overall_compliance else 1


if __name__ == "__main__":
    exit(main())
