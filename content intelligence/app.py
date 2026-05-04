"""Streamlit entry point for the AI Content Intelligence Capstone."""
from __future__ import annotations

import asyncio

import streamlit as st

from content_assistant.orchestrator import ContentAssistantOrchestrator
from content_assistant.schemas.content_schema import ContentRequest

st.set_page_config(page_title="AI Content Intelligence Capstone", page_icon="🧠", layout="wide")
st.title("AI Content Intelligence Capstone")
st.caption("Multi-agent, multimedia, RAG-enabled, memory-aware content generation system.")

task = st.selectbox("Content task", ["text", "blog", "social", "email", "audio", "video", "image", "campaign", "repurpose", "seo"])
prompt = st.text_area("Prompt", value="Create a campaign for an AI productivity assistant", height=140)
audience = st.text_input("Audience", value="founders and marketing teams")
tone = st.text_input("Tone", value="professional")

if st.button("Generate", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt before generating.")
    else:
        with st.spinner("Generating content..."):
            orchestrator = ContentAssistantOrchestrator()
            request = ContentRequest(task=task, prompt=prompt.strip(), audience=audience.strip(), tone=tone.strip())
            response = asyncio.run(orchestrator.run(request))
        st.subheader("Output")
        st.write(response.content)
        st.subheader("Metadata")
        st.json(response.metadata)
