# agent.py
from semantic_kernel.functions.kernel_function_from_prompt import (
    KernelFunctionFromPrompt,
)
from kernel_factory import create_kernel
from approval import require_approval

PROMPT = """
You are a Compliance Assessment Agent.

Analyze the following AI system description.

Your task:
1. Identify security, privacy, and governance risks
2. Map each risk to:
   - ISO/IEC 27001:2022 Annex A control IDs
   - CISA cybersecurity domains or Zero Trust pillars
3. Provide recommended remediation actions with the same mappings
4. Produce ONLY valid JSON
5. Do NOT include explanations, markdown, or extra text

Return JSON in exactly this format:

{
  "risks": [
    {
      "risk": "...",
      "iso_27001_controls": ["A.x.xx"],
      "cisa_mapping": ["..."]
    }
  ],
  "controls": [],
  "verdict": "Compliant | Partially Compliant | Non-Compliant",
  "recommended_actions": [
    {
      "action": "...",
      "iso_27001_controls": ["A.x.xx"],
      "cisa_mapping": ["..."]
    }
  ]
}

System Description:
{{$input}}

"""

async def run_compliance_agent(system_description: str):
    kernel = create_kernel()

    # ✅ Correct SK 1.39 way
    compliance_fn = KernelFunctionFromPrompt(
        function_name="ComplianceReview",
        prompt=PROMPT,
        description="Compliance risk analysis"
    )

    kernel.add_functions(plugin_name="compliance", functions=[compliance_fn])

    result = await kernel.invoke(
        plugin_name="compliance",
        function_name="ComplianceReview",
        input=system_description
    )

    require_approval(str(result))
    return result.value
