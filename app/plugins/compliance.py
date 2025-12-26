from semantic_kernel.functions import kernel_function
from logging_conf import audit_logger

class CompliancePlugin:

    @kernel_function(
        name="check_audit_logging",
        description="Check if audit logging is enabled"
    )
    def check_audit_logging(self, enabled: bool) -> str:
        result = "Compliant" if enabled else "Non-Compliant"
        audit_logger.info(f"audit_logging_check={result}")
        return result

    @kernel_function(
        name="check_human_approval",
        description="Check if human approval exists"
    )
    def check_human_approval(self, enabled: bool) -> str:
        result = "Compliant" if enabled else "Non-Compliant"
        audit_logger.info(f"human_approval_check={result}")
        return result
