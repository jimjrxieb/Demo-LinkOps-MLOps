#!/bin/bash

# LinkOps Repository Audit Script
# Audits any public repository for security, GitOps compliance, and migration readiness

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AUDIT_SERVICE_URL="http://localhost:8003"
MIGRATE_SERVICE_URL="http://localhost:8007"
OUTPUT_DIR="./audit-reports"

# Help function
show_help() {
    echo "LinkOps Repository Audit Script"
    echo ""
    echo "Usage: $0 [OPTIONS] <repository-url>"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -o, --output DIR    Output directory for reports (default: ./audit-reports)"
    echo "  -b, --branch BRANCH Branch to audit (default: main)"
    echo "  -m, --migrate       Generate migration plan after audit"
    echo "  -v, --verbose       Verbose output"
    echo ""
    echo "Examples:"
    echo "  $0 https://github.com/user/repo"
    echo "  $0 -o ./reports -b develop https://github.com/user/repo"
    echo "  $0 -m https://github.com/user/repo"
    echo ""
}

# Parse command line arguments
REPO_URL=""
BRANCH="main"
MIGRATE=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -b|--branch)
            BRANCH="$2"
            shift 2
            ;;
        -m|--migrate)
            MIGRATE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            if [[ -z "$REPO_URL" ]]; then
                REPO_URL="$1"
            else
                echo -e "${RED}Error: Multiple repository URLs provided${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate input
if [[ -z "$REPO_URL" ]]; then
    echo -e "${RED}Error: Repository URL is required${NC}"
    show_help
    exit 1
fi

# Validate URL format
if [[ ! "$REPO_URL" =~ ^https://github\.com/[^/]+/[^/]+ ]]; then
    echo -e "${RED}Error: Invalid GitHub repository URL${NC}"
    echo "Expected format: https://github.com/username/repository"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Extract repository name for file naming
REPO_NAME=$(echo "$REPO_URL" | sed 's|https://github.com/||' | sed 's|/|_|g')
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$OUTPUT_DIR/${REPO_NAME}_audit_${TIMESTAMP}.json"

echo -e "${BLUE}🔍 LinkOps Repository Audit${NC}"
echo "=================================="
echo -e "Repository: ${YELLOW}$REPO_URL${NC}"
echo -e "Branch: ${YELLOW}$BRANCH${NC}"
echo -e "Output: ${YELLOW}$REPORT_FILE${NC}"
echo ""

# Check if audit service is running
echo -e "${BLUE}📡 Checking audit service...${NC}"
if ! curl -s "$AUDIT_SERVICE_URL/health" > /dev/null; then
    echo -e "${RED}❌ Audit service is not running at $AUDIT_SERVICE_URL${NC}"
    echo "Please start the audit service:"
    echo "  docker-compose up audit_assess"
    exit 1
fi
echo -e "${GREEN}✅ Audit service is running${NC}"

# Perform audit
echo -e "${BLUE}🔍 Starting repository audit...${NC}"
AUDIT_DATA=$(cat <<EOF
{
    "repo_url": "$REPO_URL",
    "branch": "$BRANCH"
}
EOF
)

if [[ "$VERBOSE" == true ]]; then
    echo "Request data: $AUDIT_DATA"
fi

# Make audit request
AUDIT_RESPONSE=$(curl -s -X POST "$AUDIT_SERVICE_URL/scan/audit" \
    -H "Content-Type: application/json" \
    -d "$AUDIT_DATA")

# Check if audit was successful
if [[ $? -ne 0 ]]; then
    echo -e "${RED}❌ Audit request failed${NC}"
    exit 1
fi

# Save full report
echo "$AUDIT_RESPONSE" | jq '.' > "$REPORT_FILE"

# Extract summary
SUMMARY=$(echo "$AUDIT_RESPONSE" | jq -r '.summary')

if [[ "$SUMMARY" == "null" ]]; then
    echo -e "${RED}❌ Audit failed - no summary returned${NC}"
    echo "Response: $AUDIT_RESPONSE"
    exit 1
fi

# Display results
echo -e "${GREEN}✅ Audit completed successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Audit Summary:${NC}"
echo "=================="

SECURITY_SCORE=$(echo "$SUMMARY" | jq -r '.security_score')
GITOPS_SCORE=$(echo "$SUMMARY" | jq -r '.gitops_score')
TOTAL_ISSUES=$(echo "$SUMMARY" | jq -r '.total_issues')
GRADE=$(echo "$SUMMARY" | jq -r '.grade')

echo -e "Security Score: ${YELLOW}$SECURITY_SCORE${NC}"
echo -e "GitOps Score:   ${YELLOW}$GITOPS_SCORE${NC}"
echo -e "Total Issues:   ${YELLOW}$TOTAL_ISSUES${NC}"
echo -e "Grade:          ${YELLOW}$GRADE${NC}"

# Color-code the grade
if [[ "$GRADE" == "A" ]]; then
    echo -e "Grade:          ${GREEN}$GRADE${NC}"
elif [[ "$GRADE" == "B" ]]; then
    echo -e "Grade:          ${BLUE}$GRADE${NC}"
elif [[ "$GRADE" == "C" ]]; then
    echo -e "Grade:          ${YELLOW}$GRADE${NC}"
else
    echo -e "Grade:          ${RED}$GRADE${NC}"
fi

echo ""
echo -e "${BLUE}📁 Full report saved to: ${YELLOW}$REPORT_FILE${NC}"

# Generate summary report
SUMMARY_FILE="$OUTPUT_DIR/${REPO_NAME}_summary_${TIMESTAMP}.md"
cat > "$SUMMARY_FILE" <<EOF
# Repository Audit Summary

**Repository:** $REPO_URL  
**Branch:** $BRANCH  
**Audit Date:** $(date)  
**Report File:** $REPORT_FILE  

## Scores

- **Security Score:** $SECURITY_SCORE
- **GitOps Score:** $GITOPS_SCORE
- **Total Issues:** $TOTAL_ISSUES
- **Grade:** $GRADE

## Recommendations

$(echo "$AUDIT_RESPONSE" | jq -r '.report.gitops_compliance.recommendations[] | "- " + .title + " (" + .priority + " priority)"' 2>/dev/null || echo "- No specific recommendations available")

## Next Steps

1. Review the full report: \`$REPORT_FILE\`
2. Address high-priority security issues
3. Implement GitOps improvements
4. Consider migration to containerized deployment

EOF

echo -e "${BLUE}📝 Summary report saved to: ${YELLOW}$SUMMARY_FILE${NC}"

# Run migration if requested
if [[ "$MIGRATE" == true ]]; then
    echo ""
    echo -e "${BLUE}🛠️  Generating migration plan...${NC}"
    
    # Check if migrate service is running
    if ! curl -s "$MIGRATE_SERVICE_URL/health" > /dev/null; then
        echo -e "${YELLOW}⚠️  Migration service is not running at $MIGRATE_SERVICE_URL${NC}"
        echo "Skipping migration plan generation"
    else
        # Generate migration plan
        MIGRATION_RESPONSE=$(curl -s -X POST "$MIGRATE_SERVICE_URL/migrate" \
            -H "Content-Type: application/json" \
            -d "$AUDIT_RESPONSE")
        
        if [[ $? -eq 0 ]]; then
            MIGRATION_FILE="$OUTPUT_DIR/${REPO_NAME}_migration_${TIMESTAMP}.json"
            echo "$MIGRATION_RESPONSE" | jq '.' > "$MIGRATION_FILE"
            echo -e "${GREEN}✅ Migration plan saved to: ${YELLOW}$MIGRATION_FILE${NC}"
        else
            echo -e "${RED}❌ Migration plan generation failed${NC}"
        fi
    fi
fi

echo ""
echo -e "${GREEN}🎉 Audit process completed!${NC}"
echo ""
echo -e "${BLUE}📋 Files generated:${NC}"
echo "  - Full audit report: $REPORT_FILE"
echo "  - Summary report: $SUMMARY_FILE"
if [[ "$MIGRATE" == true ]]; then
    echo "  - Migration plan: $MIGRATION_FILE"
fi
echo ""
echo -e "${BLUE}💡 Next steps:${NC}"
echo "  1. Review the security issues in the full report"
echo "  2. Implement GitOps improvements based on recommendations"
echo "  3. Consider containerizing the application if not already done"
echo "  4. Set up CI/CD pipelines for automated deployment" 