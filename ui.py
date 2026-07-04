import streamlit as st
from app.langgraph_agent import run_graph

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🧠",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("AI Research Agent")
st.caption("Multi-source AI research with memory, reasoning, and structured retrieval")

st.markdown("### Ask a research question")

col1, col2 = st.columns([5, 1], vertical_alignment="bottom")

with col1:
    query = st.text_input(
        label="",
        placeholder="e.g. What is the difference between LLM and AI agent?",
        label_visibility="collapsed"
    )

with col2:
    run_btn = st.button("🔍 Run", use_container_width=True)


# =========================
# EXECUTION
# =========================
if run_btn and query:

    with st.status("🔄 Researching...", expanded=True) as status:
        st.write("🧭 Initializing agent...")
        st.write("🌐 Searching sources...")
        st.write("🤖 Generating response...")

        result = run_graph(query)

        st.write("✅ Completed")
        status.update(label="Done", state="complete")


    st.markdown("---")


    # =========================
    # ANSWER SECTION
    # =========================
    st.subheader("🧠 Answer")
    st.markdown(result["answer"])


    # =========================
    # SOURCES SECTION
    # =========================
    st.subheader("📚 Sources")

    if result.get("sources"):
        for s in result["sources"]:
            if isinstance(s, dict):
                title = s.get("title", "Source")
                url = s.get("url", "")

                st.markdown(
                    f"""
                    **🔹 {title}**  
                    [Open Source]({url})
                    """
                )
                st.divider()
    else:
        st.info("No sources found.")


    # =========================
    # TRACE SECTION
    # =========================
    st.subheader("🧭 Execution Trace")

    with st.expander("View reasoning steps", expanded=False):
        for t in result.get("trace", []):
            st.markdown(f"- {t}")


    # =========================
    # METADATA
    # =========================
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Mode", result.get("mode", "unknown"))

    with col2:
        st.metric("Sources Used", len(result.get("sources", [])))


# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Built with LangGraph • LLM Agents • Multi-source Retrieval by Vibhor Chauhan")