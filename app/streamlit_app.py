import streamlit as st
import requests
import json
import re
from typing import Any, Dict, Optional

# =====================================================
# Streamlit Page Config
# =====================================================
st.set_page_config(
    page_title="GenAI Compliance Agent",
    layout="wide"
)

st.title("🛡️ GenAI Compliance Agent")
st.caption("Semantic Kernel + Ollama | ISO 27001 & CISA Mapping")

# =====================================================
# Helper Functions
# =====================================================

def extract_text_from_sk(result: Any) -> Optional[str]:
    """
    Extract assistant text from Semantic Kernel / Ollama response
    """
    try:
        return result[0]["items"][0]["text"]
    except (IndexError, KeyError, TypeError):
        return None


def extract_json_from_text(text: str) -> Optional[Dict]:
    """
    Extract JSON embedded inside LLM text output
    """
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def normalize_compliance_data(parsed: Dict) -> Dict:
    """
    Normalize LLM output into a UI-stable schema
    """

    def normalize_items(items, kind):
        normalized = []
        for item in items or []:
            if not isinstance(item, dict):
                continue

            normalized.append({
                "title": (
                    item.get(kind)
                    or item.get("action")
                    or item.get("control")
                    or "Unnamed Item"
                ),
                "description": item.get("description"),
                "iso_27001": item.get("iso_27001_controls", []),
                "cisa": item.get("cisa_mapping", [])
            })
        return normalized

    return {
        "risks": normalize_items(parsed.get("risks"), "risk"),
        "controls": normalize_items(parsed.get("controls"), "control"),
        "verdict": parsed.get("verdict"),
        "recommended_actions": normalize_items(parsed.get("recommended_actions"), "action"),
    }


def render_section(title: str, content: Any):
    """
    Production-safe renderer
    """

    st.subheader(title)

    # Missing
    if content is None:
        st.info("No data provided.")
        return

    # Verdict
    if isinstance(content, str):
        if not content.strip():
            st.info("No data provided.")
        elif "non" in content.lower():
            st.error(content)
        elif "partial" in content.lower():
            st.warning(content)
        else:
            st.success(content)
        return

    # Empty list
    if isinstance(content, list) and len(content) == 0:
        st.info("No data provided.")
        return

    # Simple list[str]
    if isinstance(content, list) and all(isinstance(i, str) for i in content):
        for i in content:
            st.markdown(f"- {i}")
        return

    # Structured list[dict]
    if isinstance(content, list) and all(isinstance(i, dict) for i in content):
        for idx, item in enumerate(content, start=1):
            with st.expander(f"{idx}. {item.get('title', f'Item {idx}')}"):

                if item.get("description"):
                    st.markdown(f"**Description:** {item['description']}")

                if item.get("iso_27001"):
                    st.markdown("**ISO 27001 Controls:**")
                    st.markdown(", ".join(f"`{c}`" for c in item["iso_27001"]))

                if item.get("cisa"):
                    st.markdown("**CISA Mapping:**")
                    st.markdown(", ".join(f"`{c}`" for c in item["cisa"]))
        return

    # Fallback
    st.code(content)


# =====================================================
# UI Input
# =====================================================

system_description = st.text_area(
    "📄 Enter System Description / Scenario",
    height=220,
    placeholder="Describe your AI system, data flows, risks, controls, approvals..."
)

# =====================================================
# Button Action
# =====================================================

if st.button("🚀 Run Compliance Review"):
    if not system_description.strip():
        st.warning("Please enter a system description.")
    else:
        with st.spinner("Analyzing compliance risks..."):
            response = requests.post(
                "http://localhost:8000/review",
                json={"system_description": system_description},
                timeout=120
            )

        if response.status_code != 200:
            st.error("Backend error")
            st.code(response.text)
        else:
            payload = response.json()
            raw_result = payload.get("result")

            text_block = extract_text_from_sk(raw_result)
            parsed_raw = extract_json_from_text(text_block) if text_block else None

            if isinstance(parsed_raw, dict):
                parsed = normalize_compliance_data(parsed_raw)

                st.success("✅ Compliance Review Completed")

                render_section("🚨 Risks", parsed.get("risks"))
                render_section("🛡 Controls", parsed.get("controls"))
                render_section("⚖ Verdict", parsed.get("verdict"))
                render_section("📌 Recommended Actions", parsed.get("recommended_actions"))

                # Optional debug (comment out in prod)
                with st.expander("🔍 Debug: Normalized JSON"):
                    st.json(parsed)

            else:
                st.warning("⚠ Structured output not detected")
                st.subheader("📄 Raw LLM Output")
                st.write(text_block)