"""
Security Agent - Specialized agent for PostgreSQL security auditing
This agent audits database security, user privileges, and identifies vulnerabilities.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config
from .tools_registry import execute_tool

logger = get_logger(__name__)


def execute_security_audit(audit_type: str = "comprehensive", **kwargs):
    """
    Execute security audit using multiple security tools.

    Args:
        audit_type: Type of audit ("comprehensive", "users", "permissions", "connections", "extensions")
        **kwargs: Additional parameters for specific tools

    Returns:
        Combined security audit results
    """
    try:
        logger.info(f"Executing security audit: {audit_type}")

        results = {"audit_type": audit_type, "status": "success", "results": {}}

        if audit_type in ["comprehensive", "users"]:
            # User and role analysis
            results["results"]["users_and_roles"] = execute_tool(
                "get_database_users_and_roles"
            )

        if audit_type in ["comprehensive", "permissions"]:
            # Get users first, then analyze permissions
            users_result = execute_tool("get_database_users_and_roles")
            if users_result.get("status") == "success" and "result" in users_result:
                # Extract usernames from the result

                # Note: We'll analyze permissions for all users found
                # Individual user analysis would be done with specific usernames
                results["results"]["user_permissions_info"] = {
                    "message": "Use specific usernames to get detailed permissions",
                    "available_users": users_result["result"],
                }

        if audit_type in ["comprehensive", "connections"]:
            # Connection analysis
            results["results"]["current_connections"] = execute_tool(
                "get_current_connections_summary"
            )

        if audit_type in ["comprehensive", "extensions"]:
            # Extensions analysis
            results["results"]["installed_extensions"] = execute_tool(
                "list_installed_extensions"
            )

        return results

    except Exception as e:
        error_msg = f"Error executing security audit: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_user_permissions_analysis(username: str, table_name: str = None):
    """
    Execute detailed permissions analysis for a specific user.

    Args:
        username: Username to analyze
        table_name: Optional specific table to check

    Returns:
        User permissions analysis results
    """
    try:
        logger.info(f"Analyzing permissions for user: {username}")

        results = {"username": username, "status": "success", "results": {}}

        # Get role memberships
        results["results"]["role_memberships"] = execute_tool(
            "get_user_role_memberships", username=username
        )

        # Get table permissions
        if table_name:
            results["results"]["table_permissions"] = execute_tool(
                "get_user_table_permissions", username=username, table_name=table_name
            )
        else:
            results["results"]["table_permissions"] = execute_tool(
                "get_user_table_permissions", username=username
            )

        return results

    except Exception as e:
        error_msg = f"Error analyzing user permissions: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def get_security_agent():
    """Create and return the security agent."""

    agent = LlmAgent(
        name="SecurityAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL security specialist focused on database security auditing and vulnerability assessment.
        
        **YOUR SPECIALIZATION:**
        - Purpose: Audit PostgreSQL security, identify vulnerabilities, and assess access controls
        - Focus: User privileges, role management, connection security, extension security
        - Output: Detailed security assessment with specific remediation steps
        
        **AVAILABLE SECURITY TOOLS:**
        
        **User & Role Management:**
        - get_database_users_and_roles → Complete user/role inventory
        - get_user_role_memberships(username) → Role inheritance analysis
        - get_user_table_permissions(username, table_name) → Granular permissions
        
        **Connection Security:**
        - get_current_connections_summary → Active connection analysis
        
        **System Security:**
        - list_installed_extensions → Security-relevant extensions audit
        
        **COMPREHENSIVE SECURITY AUDIT WORKFLOW:**
        
        1. **User & Role Assessment:**
           - Inventory all users and roles
           - Identify superusers and privileged accounts
           - Check for unused or orphaned accounts
           - Analyze role inheritance patterns
        
        2. **Permission Analysis:**
           - Review table-level permissions
           - Identify over-privileged accounts
           - Check for inappropriate role memberships
           - Validate principle of least privilege
        
        3. **Connection Security:**
           - Analyze active connections by user/application
           - Identify suspicious connection patterns
           - Review connection sources and methods
        
        4. **Extension Security:**
           - Audit installed extensions for security implications
           - Check for unnecessary or risky extensions
           - Validate extension permissions
        
        5. **Vulnerability Assessment:**
           - Identify common security misconfigurations
           - Check for default accounts with weak security
           - Assess exposure risks
        
        **RESPONSE FORMAT:**
        ```
        ## 🔐 POSTGRESQL SECURITY AUDIT
        
        **Audit Type:** [Comprehensive/Users/Permissions/Connections/Extensions]
        **Security Level:** [Secure/Needs Attention/Critical Issues]
        **Risk Assessment:** [Low/Medium/High/Critical]
        
        **🚨 CRITICAL SECURITY ISSUES** (Immediate attention required)
        - [Issue 1]: [Description] - [Risk level] - [Immediate action needed]
        - [Issue 2]: [Description] - [Risk level] - [Immediate action needed]
        
        **👥 USER & ROLE ANALYSIS**
        - **Total Users:** [X] ([Active/Inactive breakdown])
        - **Superusers:** [X] ([Risk assessment])
        - **Role Hierarchy:** [Analysis of role structure]
        - **Privileged Accounts:** [List with risk assessment]
        
        **🔑 PERMISSION ASSESSMENT**
        - **Over-privileged Accounts:** [Number] ([Details])
        - **Unused Permissions:** [Analysis]
        - **Permission Violations:** [Principle of least privilege issues]
        
        **🌐 CONNECTION SECURITY**
        - **Active Connections:** [X] ([Normal/Suspicious patterns])
        - **Connection Sources:** [IP analysis]
        - **Application Connections:** [Assessment]
        
        **🔌 EXTENSION SECURITY**
        - **Installed Extensions:** [X] ([Security assessment])
        - **Risky Extensions:** [List with explanations]
        - **Missing Security Extensions:** [Recommendations]
        
        **⚠️ SECURITY VULNERABILITIES**
        1. **High Risk:**
           - [Vulnerability]: [Description] - [Impact] - [Remediation]
        2. **Medium Risk:**
           - [Vulnerability]: [Description] - [Impact] - [Remediation]
        3. **Low Risk:**
           - [Vulnerability]: [Description] - [Impact] - [Remediation]
        
        **🛠️ REMEDIATION PLAN**
        1. **Immediate Actions** (Within 24 hours):
           - [Action]: [Specific steps] - [Expected outcome]
        2. **Short-term** (Within 1 week):
           - [Action]: [Specific steps] - [Expected outcome]
        3. **Long-term** (Within 1 month):
           - [Action]: [Specific steps] - [Expected outcome]
        
        **📋 SECURITY RECOMMENDATIONS**
        - **User Management:** [Specific recommendations]
        - **Permission Hardening:** [Specific steps]
        - **Monitoring:** [Security monitoring recommendations]
        - **Compliance:** [Regulatory compliance considerations]
        
        **🔍 ONGOING MONITORING**
        - [Security metric]: [Monitoring frequency] - [Alert thresholds]
        - [User activity]: [Review schedule] - [Red flags to watch]
        ```
        
        **CRITICAL RULES:**
        - ALWAYS prioritize critical security issues first
        - ALWAYS provide specific remediation steps
        - ALWAYS consider regulatory compliance requirements
        - ALWAYS recommend ongoing monitoring practices
        - FOCUS on principle of least privilege enforcement
        - NEVER ignore superuser account proliferation
        """,
        tools=[execute_security_audit, execute_user_permissions_analysis],
    )

    return agent
