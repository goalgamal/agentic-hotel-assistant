"""
🏨 Grand Azure Hotel — AI Assistant (Streamlit GUI)
Run with:  streamlit run app.py
"""

import os
import sqlite3
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# ── Page config (MUST be first Streamlit call) ──────────────────
st.set_page_config(
    page_title="Grand Azure Hotel — AI Concierge",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ── Custom CSS — Luxury dark gold aesthetic ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=Jost:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
    background-color: #0d0d0d;
    color: #e8dcc8;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem; max-width: 100%; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111111 0%, #0a0a0a 100%);
    border-right: 1px solid #2a2218;
}
[data-testid="stSidebar"] * { color: #c9b98a !important; }

/* ── Hotel Header ── */
.hotel-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid #2a2218;
    margin-bottom: 1.5rem;
}
.hotel-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: #c9a84c;
    letter-spacing: 0.15em;
    line-height: 1;
    margin: 0;
}
.hotel-sub {
    font-family: 'Jost', sans-serif;
    font-size: 0.7rem;
    font-weight: 300;
    letter-spacing: 0.4em;
    color: #7a6e58;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.gold-line {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 1rem auto;
}

/* ── Chat messages ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    padding: 1rem 0;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
}
.msg-assistant {
    display: flex;
    justify-content: flex-start;
}

.bubble-user {
    background: linear-gradient(135deg, #2a1f0a 0%, #1e1708 100%);
    border: 1px solid #4a3820;
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.2rem;
    max-width: 70%;
    color: #e8dcc8;
    font-size: 0.92rem;
    line-height: 1.6;
}

.bubble-assistant {
    background: linear-gradient(135deg, #141414 0%, #111111 100%);
    border: 1px solid #2a2218;
    border-left: 3px solid #c9a84c;
    border-radius: 4px 16px 16px 16px;
    padding: 0.85rem 1.2rem;
    max-width: 75%;
    color: #d4c9ae;
    font-size: 0.92rem;
    line-height: 1.7;
}

.avatar-user {
    font-size: 1.1rem;
    margin-left: 0.5rem;
    align-self: flex-end;
}
.avatar-bot {
    font-size: 1.1rem;
    margin-right: 0.5rem;
    align-self: flex-end;
}

/* ── Tool badge ── */
.tool-badge {
    display: inline-block;
    background: #1a1408;
    border: 1px solid #3d2e10;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    font-size: 0.68rem;
    color: #c9a84c;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
    font-family: 'Jost', monospace;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #141414 !important;
    border: 1px solid #2a2218 !important;
    border-radius: 8px !important;
    color: #e8dcc8 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 1px #c9a84c22 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a84c, #a8872e) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #dbb85e, #c9a84c) !important;
    transform: translateY(-1px) !important;
}

/* ── Sidebar quick actions ── */
.quick-btn {
    background: #1a1408;
    border: 1px solid #3d2e10;
    border-radius: 6px;
    padding: 0.6rem 0.8rem;
    margin: 0.3rem 0;
    cursor: pointer;
    font-size: 0.8rem;
    color: #c9b98a;
    width: 100%;
    text-align: left;
    transition: border-color 0.2s;
}

/* ── Status metrics ── */
.metric-card {
    background: #111111;
    border: 1px solid #2a2218;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
    margin: 0.3rem 0;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    color: #c9a84c;
    line-height: 1;
}
.metric-label {
    font-size: 0.68rem;
    color: #7a6e58;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* ── Divider ── */
hr { border-color: #2a2218 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #141414 !important;
    border-color: #2a2218 !important;
    color: #e8dcc8 !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# LAZY IMPORTS — only loaded after API key is set
# ════════════════════════════════════════════════════════════════
@st.cache_resource
def load_agent_components(api_key: str):
    """Load all LangChain / LangGraph components (cached)."""
    os.environ["OPENAI_API_KEY"] = api_key

    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.tools import tool
    from langchain_core.messages import SystemMessage
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolNode, tools_condition
    from langgraph.graph.message import add_messages
    from typing import TypedDict, Annotated
    from langchain_core.messages import BaseMessage

    # ── Load RAG ──────────────────────────────────────────────
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.load_local(
        "hotel_vectorstore", embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    DB_PATH = "hotel.db"

    # ── Tools ─────────────────────────────────────────────────
    @tool
    def search_hotel_info(query: str) -> str:
        """Search the hotel knowledge base for information about amenities,
        rooms, restaurants, policies, location, and hotel services."""
        docs = retriever.invoke(query)
        if not docs:
            return "No relevant information found."
        return "Hotel Knowledge Base:\n\n" + "\n\n---\n\n".join(d.page_content for d in docs)

    @tool
    def check_room_availability(room_type: str = "") -> str:
        """Check which hotel rooms are currently available.
        Optionally filter by room type: Standard, Deluxe, Suite, or Presidential."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if room_type.strip():
            cursor.execute(
                "SELECT room_number, room_type, floor, price_per_night FROM rooms "
                "WHERE is_available=1 AND LOWER(room_type)=LOWER(?)", (room_type,))
        else:
            cursor.execute(
                "SELECT room_number, room_type, floor, price_per_night FROM rooms WHERE is_available=1")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return f"No available rooms" + (f" of type '{room_type}'." if room_type else ".")
        header = "Room No | Type           | Floor | Price/Night\n" + "-"*50
        lines = [f"{r[0]:<8} | {r[1]:<14} | {r[2]:<5} | ${r[3]:.2f}" for r in rows]
        return f"Available Rooms:\n{header}\n" + "\n".join(lines)

    @tool
    def get_booking_details(guest_name: str) -> str:
        """Look up an existing booking by the guest's name."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.booking_id, b.guest_name, r.room_number, r.room_type,
                   b.check_in, b.check_out, b.total_price, b.status
            FROM bookings b JOIN rooms r ON b.room_id=r.room_id
            WHERE LOWER(b.guest_name) LIKE LOWER(?)
        """, (f"%{guest_name}%",))
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return f"No booking found for guest '{guest_name}'."
        out = []
        for r in rows:
            out.append(
                f"Booking ID: {r[0]} | Guest: {r[1]} | Room: {r[2]} ({r[3]})\n"
                f"Check-In: {r[4]} | Check-Out: {r[5]} | Total: ${r[6]:.2f} | Status: {r[7]}"
            )
        return "\n\n".join(out)

    @tool
    def book_room(guest_name: str, room_number: str, check_in: str, check_out: str) -> str:
        """Book a hotel room for a guest.
        Args:
            guest_name: Full name of the guest
            room_number: Room number (e.g. '201', '601', '801')
            check_in: Check-in date YYYY-MM-DD
            check_out: Check-out date YYYY-MM-DD"""
        try:
            ci = datetime.strptime(check_in, "%Y-%m-%d")
            co = datetime.strptime(check_out, "%Y-%m-%d")
            if co <= ci:
                return "Error: Check-out must be after check-in."
            nights = (co - ci).days
        except ValueError:
            return "Error: Use YYYY-MM-DD date format."

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_id, room_type, price_per_night, is_available FROM rooms WHERE room_number=?",
            (room_number,))
        room = cursor.fetchone()
        if not room:
            conn.close(); return f"Error: Room {room_number} does not exist."
        room_id, room_type, price, is_available = room
        if not is_available:
            conn.close(); return f"Error: Room {room_number} is not available."

        total = price * nights
        cursor.execute(
            "INSERT INTO bookings (guest_name,room_id,check_in,check_out,total_price,status) VALUES (?,?,?,?,?,'confirmed')",
            (guest_name, room_id, check_in, check_out, total))
        bid = cursor.lastrowid
        cursor.execute("UPDATE rooms SET is_available=0 WHERE room_id=?", (room_id,))
        conn.commit(); conn.close()

        return (
            f"✅ Booking Confirmed! ID: {bid}\n"
            f"Guest: {guest_name} | Room: {room_number} ({room_type})\n"
            f"Check-In: {check_in} | Check-Out: {check_out}\n"
            f"Nights: {nights} | Total: ${total:.2f}"
        )

    tools = [search_hotel_info, check_room_availability, get_booking_details, book_room]

    # ── LangGraph ─────────────────────────────────────────────
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    SYSTEM_PROMPT = """You are a helpful and professional AI concierge for Grand Azure Hotel,
a 5-star luxury hotel in Cairo, Egypt.

Your responsibilities:
1. Answer guest questions about the hotel (amenities, rooms, restaurants, policies, location)
2. Check room availability when guests want to book
3. Process room bookings for guests
4. Look up existing bookings

Guidelines:
- Always be warm, professional, and helpful
- For hotel information questions, use search_hotel_info tool
- For availability questions, use check_room_availability tool
- For booking lookups, use get_booking_details tool
- For new bookings, first check availability then use book_room tool
- Confirm guest name, room number, and dates before booking
- Remember context from earlier in the conversation"""

    class AgentState(TypedDict):
        messages: Annotated[list[BaseMessage], add_messages]

    def agent_node(state: AgentState) -> AgentState:
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)
    builder.set_entry_point("agent")
    builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")
    graph = builder.compile()

    return graph, tools


# ════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []           # conversation history (dicts for display)
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []        # LangChain message objects (for agent)
if "tool_calls_log" not in st.session_state:
    st.session_state.tool_calls_log = []     # track which tools were called
if "total_turns" not in st.session_state:
    st.session_state.total_turns = 0

def handle_submit():
    """Grabs the text input, saves it to trigger the agent, and clears the box."""
    if st.session_state.chat_input.strip():
        st.session_state.pending_prompt = st.session_state.chat_input
        st.session_state.chat_input = ""


# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:#c9a84c; letter-spacing:0.1em;">
            GRAND AZURE
        </div>
        <div style="font-size:0.6rem; color:#7a6e58; letter-spacing:0.3em; text-transform:uppercase; margin-top:0.3rem;">
            AI Concierge System
        </div>
    </div>
    <hr style="border-color:#2a2218; margin: 0.8rem 0;">
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("<div style='font-size:0.72rem; color:#7a6e58; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;'>OpenAI API Key</div>", unsafe_allow_html=True)
    api_key = st.text_input("", type="password", placeholder="sk-...", label_visibility="collapsed",
                             value=os.getenv("OPENAI_API_KEY", ""))

    st.markdown("<hr style='border-color:#2a2218; margin: 1rem 0;'>", unsafe_allow_html=True)

    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.total_turns}</div>
            <div class="metric-label">Turns</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.tool_calls_log)}</div>
            <div class="metric-label">Tool Calls</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2a2218; margin: 1rem 0;'>", unsafe_allow_html=True)

    # Quick prompts
    st.markdown("<div style='font-size:0.68rem; color:#7a6e58; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.6rem;'>Quick Prompts</div>", unsafe_allow_html=True)

    quick_prompts = [
        ("🍽️", "What restaurants are available?"),
        ("🛏️", "Show me all available rooms"),
        ("💎", "Tell me about the Suite rooms"),
        ("🏊", "What amenities does the hotel have?"),
        ("📋", "What is the cancellation policy?"),
        ("🚗", "How do I get from the airport?"),
    ]

    for icon, prompt in quick_prompts:
        if st.button(f"{icon}  {prompt}", key=f"quick_{prompt[:10]}", use_container_width=True):
            st.session_state["pending_prompt"] = prompt

    st.markdown("<hr style='border-color:#2a2218; margin: 1rem 0;'>", unsafe_allow_html=True)

    # Tool call log
    if st.session_state.tool_calls_log:
        st.markdown("<div style='font-size:0.68rem; color:#7a6e58; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.6rem;'>Recent Tool Calls</div>", unsafe_allow_html=True)
        for tc in st.session_state.tool_calls_log[-6:]:
            st.markdown(f"<div style='font-size:0.72rem; color:#c9a84c; padding:0.2rem 0;'>🔧 {tc}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2a2218; margin: 1rem 0;'>", unsafe_allow_html=True)

    if st.button("🔄  Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_messages = []
        st.session_state.tool_calls_log = []
        st.session_state.total_turns = 0
        st.rerun()


# ════════════════════════════════════════════════════════════════
# MAIN AREA
# ════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="hotel-header">
    <div class="hotel-name">GRAND AZURE HOTEL</div>
    <div class="gold-line"></div>
    <div class="hotel-sub">AI Concierge · Cairo, Egypt · Est. 1998</div>
</div>
""", unsafe_allow_html=True)

# Chat area
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0;">
        <div style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#3d3020; margin-bottom:0.5rem;">
            Welcome, Valued Guest
        </div>
        <div style="font-size:0.82rem; letter-spacing:0.1em; color:#3d3020;">
            Ask about rooms, restaurants, amenities, or make a reservation
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🏨"):
                tools_used = msg.get("tools_used", [])
                if tools_used:
                    badges_html = " ".join(
                        f'<span style="display:inline-block; background:#1a1408; border:1px solid #3d2e10; '
                        f'border-radius:4px; padding:2px 8px; font-size:0.68rem; color:#c9a84c; '
                        f'margin-right:4px; margin-bottom:6px;">🔧 {t}</span>'
                        for t in tools_used
                    )
                    st.markdown(badges_html, unsafe_allow_html=True)
                st.write(msg["content"])


# ── Input area ──────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

col_input, col_send = st.columns([6, 1])
with col_input:
    st.text_input(
        "",
        placeholder="Ask about rooms, dining, amenities, or make a reservation...",
        label_visibility="collapsed",
        key="chat_input",
        on_change=handle_submit
    )
with col_send:
    st.button("Send →", use_container_width=True, on_click=handle_submit)


# ── Process message ─────────────────────────────────────────────
if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt

    if not api_key or not api_key.startswith("sk-"):
        st.error("⚠️ Please enter a valid OpenAI API key in the sidebar.")
        st.session_state.pop("pending_prompt")
        st.stop()

    st.session_state.pop("pending_prompt")

    # Load agent (cached)
    try:
        graph, tools_list = load_agent_components(api_key)
    except Exception as e:
        st.error(f"Failed to load agent: {e}")
        st.stop()

    from langchain_core.messages import HumanMessage

    # Add user message to display
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.lc_messages.append(HumanMessage(content=user_input))

    # Run agent
    with st.spinner(""):
        try:
            result = graph.invoke({"messages": st.session_state.lc_messages})

            # Extract new messages
            new_msgs = result["messages"][len(st.session_state.lc_messages)-1:]
            st.session_state.lc_messages = result["messages"]

            # Find tool calls made
            tools_used_this_turn = []
            for m in new_msgs:
                if hasattr(m, "tool_calls") and m.tool_calls:
                    for tc in m.tool_calls:
                        tools_used_this_turn.append(tc["name"])
                        st.session_state.tool_calls_log.append(tc["name"])

            # Get final response
            final_response = result["messages"][-1].content
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_response,
                "tools_used": tools_used_this_turn
            })
            st.session_state.total_turns += 1

        except Exception as e:
            st.error(f"Agent error: {e}")

    st.rerun()