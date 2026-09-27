
import html
import requests
import streamlit as st
import textwrap


_streamlit_markdown = st.markdown


def _render_markdown(body, **kwargs):
    if kwargs.get("unsafe_allow_html"):
        return st.html(textwrap.dedent(body).strip())

    return _streamlit_markdown(body, **kwargs)


st.markdown = _render_markdown


# ============================================================
# CONFIG
# ============================================================

API_BASE = "http://127.0.0.1:8000"

TMDB_IMG = "https://image.tmdb.org/t/p/w500"


st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(229, 9, 20, 0.10),
            transparent 30%
        ),
        #080808;
    color: #ffffff;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* Remove default Streamlit header space */

[data-testid="stHeader"] {
    background: transparent;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #242424;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.sidebar-logo {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
}

.sidebar-logo span {
    color: #e50914;
}

.sidebar-subtitle {
    color: #888;
    font-size: 0.82rem;
    margin-bottom: 2rem;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    position: relative;
    min-height: 320px;
    border-radius: 24px;
    padding: 55px 55px;
    margin-bottom: 30px;

    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,0.95) 0%,
            rgba(0,0,0,0.82) 42%,
            rgba(0,0,0,0.25) 100%
        ),
        radial-gradient(
            circle at 80% 30%,
            rgba(229,9,20,0.25),
            transparent 45%
        ),
        #111;

    border: 1px solid #252525;
    overflow: hidden;
}

.hero-small {
    color: #e50914;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 3.4rem;
    line-height: 1.05;
    font-weight: 900;
    letter-spacing: -2px;
    margin: 12px 0;
}

.hero-description {
    color: #bdbdbd;
    font-size: 1rem;
    max-width: 620px;
    line-height: 1.7;
}


/* ==========================================================
   SECTION HEADERS
   ========================================================== */

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 30px;
    margin-bottom: 18px;
}

.section-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.section-line {
    height: 2px;
    background: linear-gradient(
        90deg,
        #e50914,
        transparent
    );
    margin-top: 8px;
}


/* ==========================================================
   MOVIE CARD
   ========================================================== */

.movie-wrapper {
    background: #111111;
    border: 1px solid #242424;
    border-radius: 14px;
    overflow: hidden;
    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
    margin-bottom: 8px;
}

.movie-wrapper:hover {
    transform: translateY(-5px);
    border-color: #444;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}

.movie-title {
    font-size: 0.9rem;
    font-weight: 650;
    line-height: 1.25rem;
    color: #f5f5f5;
    padding: 10px 11px 3px 11px;

    min-height: 42px;

    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.movie-meta {
    color: #888;
    font-size: 0.76rem;
    padding: 0 11px 11px 11px;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {
    width: 100%;
    border-radius: 9px;
    border: 1px solid #333;
    background: #181818;
    color: #ffffff;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #e50914;
    color: white;
    background: #e50914;
}


/* ==========================================================
   SEARCH
   ========================================================== */

.search-label {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 8px;
}

div[data-baseweb="input"] {
    background: #151515;
    border: 1px solid #333;
    border-radius: 12px;
}

div[data-baseweb="input"]:focus-within {
    border-color: #e50914;
    box-shadow: 0 0 0 1px #e50914;
}


/* ==========================================================
   DETAILS HERO
   ========================================================== */

.details-backdrop {
    border-radius: 22px;
    padding: 45px;
    margin-bottom: 25px;

    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,0.96),
            rgba(0,0,0,0.75),
            rgba(0,0,0,0.25)
        ),
        #111;

    border: 1px solid #292929;
}

.details-title {
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 12px;
}

.details-overview {
    color: #c4c4c4;
    line-height: 1.75;
    max-width: 750px;
}


/* ==========================================================
   BADGES
   ========================================================== */

.badge {
    display: inline-block;
    background: #1d1d1d;
    border: 1px solid #353535;
    color: #d7d7d7;
    padding: 6px 11px;
    border-radius: 20px;
    margin-right: 5px;
    margin-bottom: 5px;
    font-size: 0.78rem;
}

.badge-red {
    background: rgba(229,9,20,0.12);
    border-color: rgba(229,9,20,0.45);
    color: #ff5b63;
}


/* ==========================================================
   INFO BOX
   ========================================================== */

.info-box {
    background: #111;
    border: 1px solid #242424;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.info-label {
    color: #777;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.info-value {
    color: #fff;
    font-size: 1rem;
    font-weight: 650;
    margin-top: 4px;
}


/* ==========================================================
   EMPTY / ERROR
   ========================================================== */

.empty-box {
    background: #111;
    border: 1px dashed #333;
    border-radius: 16px;
    padding: 35px;
    text-align: center;
    color: #888;
}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {
    border-color: #242424 !important;
}


/* ==========================================================
   STREAMLIT SELECTBOX
   ========================================================== */

div[data-baseweb="select"] > div {
    background: #151515;
    border-color: #333;
    border-radius: 10px;
    color: white;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 800px) {

    .hero {
        padding: 30px;
        min-height: 250px;
    }

    .hero-title {
        font-size: 2.2rem;
    }

    .details-title {
        font-size: 2rem;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

if "force_home" not in st.session_state:
    st.session_state.force_home = False


# ============================================================
# URL ROUTING
# ============================================================

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")


if st.session_state.force_home:
    st.session_state.force_home = False
    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None
elif qp_view == "details" and qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except (ValueError, TypeError):
        st.session_state.view = "home"
        st.session_state.selected_tmdb_id = None
elif qp_view == "home" or qp_view == "details":
    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None


def goto_home():

    st.session_state.view = "home"
    st.session_state.selected_tmdb_id = None
    st.session_state.force_home = True
    st.query_params.clear()


def goto_details(tmdb_id: int):

    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)

    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))

    st.rerun()


# ============================================================
# API HELPER
# ============================================================

@st.cache_data(ttl=30)
def api_get_json(
    path: str,
    params: dict | None = None,
):

    try:

        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=25,
        )

        if response.status_code >= 400:

            return None, (
                f"HTTP {response.status_code}: "
                f"{response.text[:300]}"
            )

        return response.json(), None

    except requests.exceptions.ConnectionError:

        return None, (
            "Cannot connect to FastAPI. "
            "Make sure main.py is running on "
            "http://127.0.0.1:8000"
        )

    except requests.exceptions.Timeout:

        return None, (
            "FastAPI request timed out. "
            "Check your backend and TMDB connection."
        )

    except requests.exceptions.RequestException as e:

        return None, f"Request failed: {e}"

    except Exception as e:

        return None, f"Unexpected error: {e}"


# ============================================================
# MOVIE CARD GRID
# ============================================================

def poster_grid(
    cards,
    cols=6,
    key_prefix="grid",
):

    if not cards:

        st.markdown(
            """
            <div class="empty-box">
                🎬 No movies available.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return


    rows = (
        len(cards) + cols - 1
    ) // cols


    idx = 0


    for row in range(rows):

        column_set = st.columns(
            cols,
            gap="medium",
        )


        for col_index in range(cols):

            if idx >= len(cards):
                break


            movie = cards[idx]

            idx += 1


            tmdb_id = movie.get("tmdb_id")

            title = (
                movie.get("title")
                or "Untitled"
            )

            poster = movie.get(
                "poster_url"
            )

            release_date = (
                movie.get("release_date")
                or ""
            )

            year = (
                release_date[:4]
                if release_date
                else ""
            )


            with column_set[col_index]:

                # Poster
                if poster:

                    st.image(
                        poster,
                        width="stretch",
                    )

                else:

                    st.markdown(
                        """
                        <div style="
                            height:260px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#151515;
                            border-radius:12px;
                            color:#777;
                        ">
                            🎬 No Poster
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                # Title
                safe_title = html.escape(
                    str(title)
                )


                st.markdown(
                    f"""
                    <div class="movie-title">
                        {safe_title}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                # Year
                if year:

                    st.markdown(
                        f"""
                        <div class="movie-meta">
                            {year}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        """
                        <div class="movie-meta">
                            Movie
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


                # Open button
                if st.button(
                    "View Movie",
                    key=(
                        f"{key_prefix}_"
                        f"{row}_"
                        f"{col_index}_"
                        f"{idx}_"
                        f"{tmdb_id}"
                    ),
                ):

                    if tmdb_id:

                        goto_details(
                            int(tmdb_id)
                        )


# ============================================================
# TF-IDF CONVERTER
# ============================================================

def to_cards_from_tfidf_items(
    tfidf_items,
):

    cards = []


    for item in tfidf_items or []:

        tmdb = (
            item.get("tmdb")
            or {}
        )


        if tmdb.get("tmdb_id"):

            cards.append(
                {
                    "tmdb_id": tmdb[
                        "tmdb_id"
                    ],

                    "title": (
                        tmdb.get("title")
                        or item.get("title")
                        or "Untitled"
                    ),

                    "poster_url": tmdb.get(
                        "poster_url"
                    ),

                    "vote_average": tmdb.get(
                        "vote_average"
                    ),

                    "release_date": tmdb.get(
                        "release_date"
                    ),
                }
            )


    return cards


# ============================================================
# TMDB SEARCH PARSER
# ============================================================

def parse_tmdb_search_to_cards(
    data,
    keyword: str,
    limit: int = 24,
):

    keyword_lower = (
        keyword.strip().lower()
    )


    # --------------------------------------------------------
    # RAW TMDB RESPONSE
    # --------------------------------------------------------

    if (
        isinstance(data, dict)
        and "results" in data
    ):

        raw_items = []


        for movie in (
            data.get("results")
            or []
        ):

            title = (
                movie.get("title")
                or ""
            ).strip()


            tmdb_id = movie.get("id")


            poster_path = movie.get(
                "poster_path"
            )


            if not title or not tmdb_id:
                continue


            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),

                    "title": title,

                    "poster_url": (
                        f"{TMDB_IMG}{poster_path}"
                        if poster_path
                        else None
                    ),

                    "release_date": (
                        movie.get(
                            "release_date",
                            "",
                        )
                    ),

                    "vote_average": (
                        movie.get(
                            "vote_average"
                        )
                    ),
                }
            )


    # --------------------------------------------------------
    # ALREADY CONVERTED LIST
    # --------------------------------------------------------

    elif isinstance(data, list):

        raw_items = []


        for movie in data:

            tmdb_id = (
                movie.get("tmdb_id")
                or movie.get("id")
            )


            title = (
                movie.get("title")
                or ""
            ).strip()


            if not title or not tmdb_id:
                continue


            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),

                    "title": title,

                    "poster_url": movie.get(
                        "poster_url"
                    ),

                    "release_date": (
                        movie.get(
                            "release_date",
                            "",
                        )
                    ),

                    "vote_average": (
                        movie.get(
                            "vote_average"
                        )
                    ),
                }
            )


    else:

        return [], []


    # --------------------------------------------------------
    # KEYWORD FILTER
    # --------------------------------------------------------

    matched = [
        movie
        for movie in raw_items
        if keyword_lower
        in movie["title"].lower()
    ]


    final_list = (
        matched
        if matched
        else raw_items
    )


    # --------------------------------------------------------
    # SUGGESTIONS
    # --------------------------------------------------------

    suggestions = []


    for movie in final_list[:10]:

        year = (
            movie.get(
                "release_date"
            )
            or ""
        )[:4]


        label = (
            f"{movie['title']} ({year})"
            if year
            else movie["title"]
        )


        suggestions.append(
            (
                label,
                movie["tmdb_id"],
            )
        )


    # --------------------------------------------------------
    # CARDS
    # --------------------------------------------------------

    cards = [
        {
            "tmdb_id": movie[
                "tmdb_id"
            ],

            "title": movie[
                "title"
            ],

            "poster_url": movie[
                "poster_url"
            ],

            "release_date": movie.get(
                "release_date"
            ),

            "vote_average": movie.get(
                "vote_average"
            ),
        }

        for movie in final_list[:limit]
    ]


    return suggestions, cards


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">
            🎬 Cine<span>Match</span>
        </div>

        <div class="sidebar-subtitle">
            Smart Movie Recommendations
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.button(
        "🏠  Home",
        width="stretch",
        on_click=goto_home,
    )


    st.markdown("---")


    st.markdown(
        "### Browse"
    )


    home_category = st.selectbox(
        "Movie Category",

        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming",
        ],

        index=0,
    )


    grid_cols = st.slider(
        "Movies per row",
        min_value=4,
        max_value=8,
        value=6,
    )


    st.markdown("---")


    st.markdown(
        """
        <div style="
            color:#777;
            font-size:0.78rem;
            line-height:1.6;
        ">
            Powered by TMDB + TF-IDF<br>
            FastAPI + Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HOME VIEW
# ============================================================

if st.session_state.view == "home":


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero">

            <div class="hero-small">
                YOUR PERSONAL MOVIE DISCOVERY
            </div>

            <div class="hero-title">
                Find your next<br>
                favorite movie.
            </div>

            <div class="hero-description">
                Search thousands of movies and discover
                similar titles using our TF-IDF recommendation
                engine and TMDB movie data.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    st.markdown(
        '<div class="search-label">🔎 Search Movies</div>',
        unsafe_allow_html=True,
    )


    typed = st.text_input(
        "Movie search",
        placeholder=(
            "Search Batman, Avengers, Inception..."
        ),
        label_visibility="collapsed",
    )


    # ========================================================
    # SEARCH RESULTS
    # ========================================================

    if typed.strip():

        if len(typed.strip()) < 2:

            st.info(
                "Type at least 2 characters."
            )

        else:

            data, error = api_get_json(
                "/tmdb/search",
                params={
                    "query": typed.strip()
                },
            )


            if error or data is None:

                st.error(
                    f"Search failed: {error}"
                )

            else:

                suggestions, cards = (
                    parse_tmdb_search_to_cards(
                        data,
                        typed.strip(),
                        limit=24,
                    )
                )


                # ------------------------------------------------
                # SEARCH RESULTS
                # ------------------------------------------------

                st.markdown(
                    f"""
                    <div class="section-header">
                        <div>
                            <div class="section-title">
                                Search Results
                            </div>
                            <div class="section-line"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


                poster_grid(
                    cards,
                    cols=grid_cols,
                    key_prefix="search",
                )


        st.stop()


    # ========================================================
    # HOME FEED
    # ========================================================

    category_name = (
        home_category
        .replace("_", " ")
        .title()
    )


    st.markdown(
        f"""
        <div class="section-header">

            <div>
                <div class="section-title">
                    {category_name}
                </div>

                <div class="section-line"></div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    home_cards, error = api_get_json(
        "/home",
        params={
            "category": home_category,
            "limit": 24,
        },
    )


    if error or not home_cards:

        st.error(
            f"Home feed failed: "
            f"{error or 'Unknown error'}"
        )

        st.stop()


    poster_grid(
        home_cards,
        cols=grid_cols,
        key_prefix="home",
    )


# ============================================================
# DETAILS VIEW
# ============================================================

elif st.session_state.view == "details":


    tmdb_id = (
        st.session_state.selected_tmdb_id
    )


    if not tmdb_id:

        st.warning(
            "No movie selected."
        )

        st.button(
            "← Back to Home",
            key="back_home_without_movie",
            width="content",
            on_click=goto_home,
        )

        st.stop()


    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    st.button(
        "← Back to Home",
        key="back_home_from_details",
        width="content",
        on_click=goto_home,
    )


    # --------------------------------------------------------
    # GET DETAILS
    # --------------------------------------------------------

    data, error = api_get_json(
        f"/movie/id/{tmdb_id}"
    )


    if error or not data:

        st.error(
            f"Could not load movie details: "
            f"{error or 'Unknown error'}"
        )

        st.stop()


    title = (
        data.get("title")
        or "Untitled"
    )


    overview = (
        data.get("overview")
        or "No overview available."
    )


    release = (
        data.get("release_date")
        or "Unknown"
    )


    genres = data.get(
        "genres",
        [],
    )


    genre_names = [
        genre.get("name")
        for genre in genres
        if genre.get("name")
    ]


    # --------------------------------------------------------
    # BACKDROP
    # --------------------------------------------------------

    backdrop = data.get(
        "backdrop_url"
    )


    if backdrop:

        st.markdown(
            f"""
            <div
                class="details-backdrop"
                style="
                    background-image:
                    linear-gradient(
                        90deg,
                        rgba(0,0,0,0.96),
                        rgba(0,0,0,0.78),
                        rgba(0,0,0,0.35)
                    ),
                    url('{backdrop}');
                    background-size:cover;
                    background-position:center;
                "
            >

                <div class="details-title">
                    {html.escape(title)}
                </div>

                <div style="
                    color:#999;
                    margin-bottom:15px;
                ">
                    {release}
                </div>

                <div>
                    {
                        "".join(
                            [
                                f'<span class="badge">{html.escape(g)}</span>'
                                for g in genre_names
                            ]
                        )
                    }
                </div>

                <div class="details-overview">
                    {html.escape(overview)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="details-backdrop">

                <div class="details-title">
                    {html.escape(title)}
                </div>

                <div class="details-overview">
                    {html.escape(overview)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # MOVIE INFORMATION
    # --------------------------------------------------------

    poster = data.get(
        "poster_url"
    )


    left, right = st.columns(
        [1, 2.5],
        gap="large",
    )


    with left:

        if poster:

            st.image(
                poster,
                width="stretch",
            )

        else:

            st.markdown(
                """
                <div class="empty-box">
                    🎬<br>
                    Poster unavailable
                </div>
                """,
                unsafe_allow_html=True,
            )


    with right:

        st.markdown(
            "### Movie Information"
        )


        info1, info2, info3 = st.columns(3)


        with info1:

            st.markdown(
                f"""
                <div class="info-box">

                    <div class="info-label">
                        Release
                    </div>

                    <div class="info-value">
                        {html.escape(release)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


        with info2:

            rating = data.get(
                "vote_average"
            )


            rating_text = (
                f"⭐ {rating:.1f}"
                if isinstance(
                    rating,
                    (int, float),
                )
                else "N/A"
            )


            st.markdown(
                f"""
                <div class="info-box">

                    <div class="info-label">
                        Rating
                    </div>

                    <div class="info-value">
                        {rating_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


        with info3:

            st.markdown(
                f"""
                <div class="info-box">

                    <div class="info-label">
                        TMDB ID
                    </div>

                    <div class="info-value">
                        {tmdb_id}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


        st.markdown(
            "### Overview"
        )


        st.markdown(
            f"""
            <div class="details-overview">
                {html.escape(overview)}
            </div>
            """,
            unsafe_allow_html=True,
        )


        if genre_names:

            st.markdown(
                "### Genres"
            )


            genre_html = "".join(
                [
                    f"""
                    <span class="badge">
                        {html.escape(genre)}
                    </span>
                    """

                    for genre in genre_names
                ]
            )


            st.markdown(
                genre_html,
                unsafe_allow_html=True,
            )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()


    st.markdown(
        """
        <div class="section-title">
            🎯 Recommended For You
        </div>

        <div class="section-line"></div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # BUNDLE
    # --------------------------------------------------------

    bundle, bundle_error = api_get_json(
        "/movie/search",
        params={
            "query": title,
            "tfidf_top_n": 12,
            "genre_limit": 12,
        },
    )


    if not bundle_error and bundle:

        # ----------------------------------------------------
        # TF-IDF
        # ----------------------------------------------------

        tfidf_cards = (
            to_cards_from_tfidf_items(
                bundle.get(
                    "tfidf_recommendations"
                )
            )
        )


        if tfidf_cards:

            st.markdown(
                """
                <div class="section-header">

                    <div>
                        <div class="section-title">
                            🔎 Similar Movies
                        </div>

                        <div class="section-line"></div>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            st.caption(
                "Recommendations generated using TF-IDF similarity."
            )


            poster_grid(
                tfidf_cards,
                cols=grid_cols,
                key_prefix="tfidf",
            )


        # ----------------------------------------------------
        # GENRE
        # ----------------------------------------------------

        genre_cards = bundle.get(
            "genre_recommendations",
            [],
        )


        if genre_cards:

            st.markdown(
                """
                <div class="section-header">

                    <div>
                        <div class="section-title">
                            🎭 More Like This
                        </div>

                        <div class="section-line"></div>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            st.caption(
                "Popular movies from the same genre."
            )


            poster_grid(
                genre_cards,
                cols=grid_cols,
                key_prefix="genre",
            )


    # ========================================================
    # FALLBACK
    # ========================================================

    else:

        st.info(
            "The combined recommendation service "
            "is temporarily unavailable. Showing "
            "genre recommendations instead."
        )


        genre_only, genre_error = api_get_json(
            "/recommend/genre",
            params={
                "tmdb_id": tmdb_id,
                "limit": 18,
            },
        )


        if not genre_error and genre_only:

            poster_grid(
                genre_only,
                cols=grid_cols,
                key_prefix="genre_fallback",
            )

        else:

            st.warning(
                "No recommendations available right now."
            )
