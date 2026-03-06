import streamlit as st
from generator import generate_post, generate_update

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AITA Generator",
    page_icon="🔥",
    layout="centered"
)

st.title("AITA Post Generator (with updates)")
st.caption("Describe a situation → get an AITA post → give your verdict → watch the update unfold")

# ── Session state init ────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "post_update" not in st.session_state:
    st.session_state.post_update = ""

# ── Stage 1: Input ────────────────────────────────────────────────────────────
if st.session_state.stage == "input":
    st.markdown("### What's the situation?")
    description = st.text_input(
        "Describe it in one sentence",
        placeholder="e.g. I told my sister her wedding dress was ugly"
    )

    if st.button("Generate Post 🚀", disabled=not description):
        with st.spinner("Writing your drama..."):
            post = generate_post(description)
            st.session_state.generated_post = post
            st.session_state.stage = "generated"
        st.rerun()

# ── Stage 2: Show post + get verdict ─────────────────────────────────────────
elif st.session_state.stage == "generated":
    st.markdown("### The Post")
    st.markdown(
        f"<div style='background:#1a1a2e;padding:20px;border-radius:10px;"
        f"border-left:4px solid #e94560;font-size:15px;line-height:1.7'>"
        f"{st.session_state.generated_post.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### Your Verdict")

    col1, col2, col3, col4 = st.columns(4)
    verdict_map = {
        "NTA": "NTA",
        "YTA": "YTA",
        "ESH": "ESH",
        "NAH": "NAH"
    }

    for col, (label, value) in zip([col1, col2, col3, col4], verdict_map.items()):
        if col.button(label, use_container_width=True):
            st.session_state.verdict = value
            st.rerun()

    if "verdict" in st.session_state:
        st.success(f"You voted: **{st.session_state.verdict}**")

        comment = st.text_area(
            "Leave a comment (the OP will see this...)",
            placeholder="e.g. Dude, just lie sometimes. Not everything needs brutal honesty.",
            max_chars=200
        )

        if st.button("Send & Get Update 📩", disabled=not comment):
            with st.spinner("OP is typing an update..."):
                update = generate_update(
                    original_post=st.session_state.generated_post,
                    user_verdict=st.session_state.verdict,
                    user_comment=comment,
                )
                st.session_state.post_update = update
                st.session_state.stage = "updated"
            st.rerun()

# ── Stage 3: Show update ──────────────────────────────────────────────────────
elif st.session_state.stage == "updated":
    st.markdown("### The Original Post")
    st.markdown(
        f"<div style='background:#1a1a2e;padding:20px;border-radius:10px;"
        f"border-left:4px solid #e94560;font-size:15px;line-height:1.7'>"
        f"{st.session_state.generated_post.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### The Update 🔥")
    st.markdown(
        f"<div style='background:#0f3460;padding:20px;border-radius:10px;"
        f"border-left:4px solid #f5a623;font-size:15px;line-height:1.7'>"
        f"{st.session_state.post_update.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.button("🔄 Try Another Situation"):
        for key in ["stage", "generated_post", "post_update", "verdict"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()