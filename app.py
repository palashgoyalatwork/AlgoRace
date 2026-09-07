import time
import random

import streamlit as st
import plotly.graph_objects as go

from algorithms import run_algorithm, get_algorithm_steps


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AlgoRace",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(59,130,246,0.10), transparent 30%),
                radial-gradient(circle at 90% 10%, rgba(168,85,247,0.08), transparent 30%),
                #080b12;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            text-align: center;
            padding: 15px 0 28px 0;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -2px;
            margin-bottom: 5px;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
        }

        .race-card {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid rgba(148,163,184,0.15);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 15px;
        }

        .winner {
            text-align: center;
            padding: 16px;
            border-radius: 14px;
            background: rgba(34,197,94,0.10);
            border: 1px solid rgba(34,197,94,0.25);
            margin-top: 20px;
            font-size: 1.15rem;
            font-weight: 700;
        }

        .footer {
            text-align: center;
            color: #64748b;
            margin-top: 40px;
            font-size: 0.85rem;
        }

        div[data-testid="stMetric"] {
            background: rgba(15,23,42,0.6);
            padding: 12px;
            border-radius: 12px;
            border: 1px solid rgba(148,163,184,0.10);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = [
        random.randint(10, 100) for _ in range(50)
    ]

if "results" not in st.session_state:
    st.session_state.results = None


# =========================================================
# HELPERS
# =========================================================

def make_chart(values, highlights=(), title=""):
    """Create a Plotly bar chart for an algorithm state."""

    x = list(range(len(values)))

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=values,
            showlegend=False,
        )
    )

    fig.update_layout(
        title=title,
        height=310,
        margin=dict(l=15, r=15, t=45, b=25),
        template="plotly_dark",
        xaxis_title="Index",
        yaxis_title="Value",
        transition_duration=0,
    )

    return fig


def sample_steps(generator, max_frames=100):
    """
    Convert a potentially huge generator into a manageable
    number of animation frames.
    """

    steps = list(generator)

    if len(steps) <= max_frames:
        return steps

    interval = max(1, len(steps) // max_frames)

    sampled = steps[::interval]

    if sampled[-1] != steps[-1]:
        sampled.append(steps[-1])

    return sampled


def run_race(name_a, name_b, dataset, race_placeholder):
    """Run both algorithms visually."""

    steps_a = sample_steps(
        get_algorithm_steps(name_a, dataset),
        max_frames=90,
    )

    steps_b = sample_steps(
        get_algorithm_steps(name_b, dataset),
        max_frames=90,
    )

    total_frames = max(len(steps_a), len(steps_b))

    for frame in range(total_frames):

        state_a = steps_a[
            min(frame, len(steps_a) - 1)
        ]

        state_b = steps_b[
            min(frame, len(steps_b) - 1)
        ]

        array_a, comparisons_a, swaps_a, highlights_a = state_a
        array_b, comparisons_b, swaps_b, highlights_b = state_b

        col_a, col_b = race_placeholder.columns(2)

        with col_a:
            st.markdown(
                f"### 🔵 {name_a}"
            )

            st.plotly_chart(
                make_chart(
                    array_a,
                    highlights_a,
                    "Sorting...",
                ),
                use_container_width=True,
                key=f"race_a_{frame}",
            )

            m1, m2 = st.columns(2)

            with m1:
                st.metric(
                    "Comparisons",
                    f"{comparisons_a:,}",
                )

            with m2:
                st.metric(
                    "Swaps / Moves",
                    f"{swaps_a:,}",
                )

        with col_b:
            st.markdown(
                f"### 🟣 {name_b}"
            )

            st.plotly_chart(
                make_chart(
                    array_b,
                    highlights_b,
                    "Sorting...",
                ),
                use_container_width=True,
                key=f"race_b_{frame}",
            )

            m1, m2 = st.columns(2)

            with m1:
                st.metric(
                    "Comparisons",
                    f"{comparisons_b:,}",
                )

            with m2:
                st.metric(
                    "Swaps / Moves",
                    f"{swaps_b:,}",
                )

        progress = (frame + 1) / total_frames

        st.progress(
            progress,
            text=f"Race Progress — {int(progress * 100)}%",
        )

        time.sleep(0.035)

    # Final benchmark
    start_a = time.perf_counter()
    sorted_a, comparisons_a, swaps_a = run_algorithm(
        name_a,
        dataset,
    )
    end_a = time.perf_counter()

    start_b = time.perf_counter()
    sorted_b, comparisons_b, swaps_b = run_algorithm(
        name_b,
        dataset,
    )
    end_b = time.perf_counter()

    time_a = (end_a - start_a) * 1000
    time_b = (end_b - start_b) * 1000

    return {
        "algorithm_a": {
            "name": name_a,
            "sorted": sorted_a,
            "time": time_a,
            "comparisons": comparisons_a,
            "swaps": swaps_a,
        },
        "algorithm_b": {
            "name": name_b,
            "sorted": sorted_b,
            "time": time_b,
            "comparisons": comparisons_b,
            "swaps": swaps_b,
        },
    }


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🏁 AlgoRace</div>
        <div class="hero-subtitle">
            Put sorting algorithms head-to-head on the exact same dataset.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Race Settings")

    algorithm_names = [
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort",
    ]

    algorithm_a = st.selectbox(
        "Algorithm A",
        algorithm_names,
        index=0,
    )

    algorithm_b = st.selectbox(
        "Algorithm B",
        algorithm_names,
        index=4,
    )

    st.divider()

    array_size = st.slider(
        "Dataset Size",
        min_value=10,
        max_value=100,
        value=40,
        step=10,
    )

    st.caption(
        "Smaller datasets create a clearer live animation."
    )

    st.divider()

    if st.button(
        "🔄 Generate New Dataset",
        use_container_width=True,
    ):
        st.session_state.dataset = [
            random.randint(10, 100)
            for _ in range(array_size)
        ]

        st.session_state.results = None

        st.rerun()

    start_race = st.button(
        "🏁 START RACE",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# DATASET
# =========================================================

st.markdown("### 📊 Current Dataset")

dataset = st.session_state.dataset

preview = dataset[:30]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=list(range(len(preview))),
        y=preview,
        name="Dataset",
        showlegend=False,
    )
)

fig.update_layout(
    height=280,
    margin=dict(l=20, r=20, t=20, b=20),
    template="plotly_dark",
    xaxis_title="Index",
    yaxis_title="Value",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


if len(dataset) > 30:
    st.caption(
        f"Showing first 30 elements of "
        f"{len(dataset)} total elements."
    )


# =========================================================
# LIVE RACE
# =========================================================

if start_race:

    race_data = [
        random.randint(10, 100)
        for _ in range(array_size)
    ]

    st.session_state.dataset = race_data

    st.markdown("## 🏁 LIVE RACE")

    race_placeholder = st.empty()

    results = run_race(
        algorithm_a,
        algorithm_b,
        race_data,
        race_placeholder,
    )

    st.session_state.results = results

    st.rerun()


# =========================================================
# RESULTS
# =========================================================

results = st.session_state.results

if results is not None:

    result_a = results["algorithm_a"]
    result_b = results["algorithm_b"]

    st.markdown("## 🏆 Race Results")

    col_a, col_b = st.columns(2)

    with col_a:

        st.markdown(
            f"""
            <div class="race-card">
                <h3>🔵 {result_a["name"]}</h3>
                <p>Algorithm A</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2 = st.columns(2)

        with m1:
            st.metric(
                "Execution Time",
                f"{result_a['time']:.4f} ms",
            )

        with m2:
            st.metric(
                "Comparisons",
                f"{result_a['comparisons']:,}",
            )

        st.metric(
            "Swaps / Moves",
            f"{result_a['swaps']:,}",
        )

        st.markdown("**Sorted Output**")

        st.plotly_chart(
            make_chart(
                result_a["sorted"],
                title="Final Sorted Array",
            ),
            use_container_width=True,
            key="final_a",
        )

    with col_b:

        st.markdown(
            f"""
            <div class="race-card">
                <h3>🟣 {result_b["name"]}</h3>
                <p>Algorithm B</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2 = st.columns(2)

        with m1:
            st.metric(
                "Execution Time",
                f"{result_b['time']:.4f} ms",
            )

        with m2:
            st.metric(
                "Comparisons",
                f"{result_b['comparisons']:,}",
            )

        st.metric(
            "Swaps / Moves",
            f"{result_b['swaps']:,}",
        )

        st.markdown("**Sorted Output**")

        st.plotly_chart(
            make_chart(
                result_b["sorted"],
                title="Final Sorted Array",
            ),
            use_container_width=True,
            key="final_b",
        )

    # -----------------------------------------------------
    # WINNER
    # -----------------------------------------------------

    if result_a["time"] < result_b["time"]:
        winner = result_a["name"]
    elif result_b["time"] < result_a["time"]:
        winner = result_b["name"]
    else:
        winner = "It's a tie!"

    st.markdown(
        f"""
        <div class="winner">
            🏆 Winner: {winner}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # COMPARISON
    # -----------------------------------------------------

    st.markdown("### 📈 Performance Comparison")

    st.table(
        {
            "Metric": [
                "Execution Time",
                "Comparisons",
                "Swaps / Moves",
            ],
            result_a["name"]: [
                f"{result_a['time']:.4f} ms",
                f"{result_a['comparisons']:,}",
                f"{result_a['swaps']:,}",
            ],
            result_b["name"]: [
                f"{result_b['time']:.4f} ms",
                f"{result_b['comparisons']:,}",
                f"{result_b['swaps']:,}",
            ],
        }
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AlgoRace V1 • Built with Python, Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)