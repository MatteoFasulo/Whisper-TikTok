from pathlib import Path
import random
import streamlit as st

import praw

HOME = Path(__name__).parent.absolute()


@st.cache_data
def create_instance(*args, **kwargs):
    reddit = praw.Reddit(
        client_id=kwargs.get('client_id'),
        client_secret=kwargs.get('client_secret'),
        user_agent=kwargs.get('user_agent'),
    )

    subreddit = get_subreddit(reddit=reddit, subreddit=kwargs.get(
        'subreddit'), nsfw=kwargs.get('nsfw'))
    submission = get_random_submission(subreddit=subreddit)
    st.session_state['submission'] = submission
    return True


def get_subreddit(*args, **kwargs):
    reddit = kwargs.get('reddit')
    subreddit = reddit.subreddit(kwargs.get('subreddit'))
    nsfw = kwargs.get('nsfw')
    try:
        st.text(f"Subreddit: {subreddit.display_name}")
    except Exception as exception:
        st.exception(exception=exception)

    if subreddit.over18 and not nsfw:
        st.error(
            body='subreddit has NSFW contents but you did not select to scrape them')
    return subreddit


def get_random_submission(*args, **kwargs):
    subreddit = kwargs.get('subreddit')
    submissions = [submission for submission in subreddit.hot(limit=10)]
    return random.choice(submissions)


# Streamlit Config
st.set_page_config(
    page_title="Whisper-TikTok",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MatteoFasulo/Whisper-TikTok',
        'Report a bug': "https://github.com/MatteoFasulo/Whisper-TikTok/issues",
        'About':
            """
            # Whisper-TikTok
            Whisper-TikTok is an innovative AI-powered tool that leverages the prowess of Edge TTS, OpenAI-Whisper, and FFMPEG to craft captivating TikTok videos also with a web application interface!

            Mantainer: https://github.com/MatteoFasulo

            If you find a bug or if you just have questions about the project feel free to reach me at https://github.com/MatteoFasulo/Whisper-TikTok
            Any contribution to this project is welcome to improve the quality of work!
            """
    }
)

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("https://github.com/MatteoFasulo/Whisper-TikTok",
             label="GitHub", icon="🌎")

with st.sidebar:
    with st.expander("ℹ️ How to use"):
        st.write(
            """
            Before starting you will need to create a new [Reddit API App](https://www.reddit.com/prefs/apps) by selecting `script` (personal use).
            Then, after putting the App name, http://localhost as `reddit uri` and `about url`, you have just to insert those values in this dashboard to use the Reddit API for scraping any subreddit.
            """)
    client_id = st.text_input(label='Reddit Client ID')
    client_secret = st.text_input(
        label='Reddit Client Secret', type='password')
    user_agent = st.text_input(label='Reddit User Agent')


st.title("🏆 Whisper-TikTok 🚀")
st.subheader('Reddit section')
st.write("""
    This section allows you to generate videos from subreddits.""")

st.divider()

LEFT, RIGHT = st.columns(2)

with LEFT:
    num_videos = st.number_input(label='How many videos do you want to generate?',
                                 min_value=1, max_value=10, value=1, step=1)

    subreddit = st.text_input(
        label='What Subreddit do you want to use', placeholder='AskReddit')

    nsfw = st.checkbox(label='NSFW content?', value=False)

    max_chars = st.slider(label='Maximum number of characters per line',
                          min_value=10, max_value=50, value=38, step=1)

    max_words = st.number_input(label='Maximum number of words per line', min_value=1,
                                max_value=5, value=2, step=1)

    result = st.button('Get subreddit')

    with RIGHT:
        if result:
            create_instance(client_id=client_id, client_secret=client_secret,
                            user_agent=user_agent, subreddit=subreddit, nsfw=nsfw)
            submission = st.session_state['submission']
            title = submission.title
            submission.comment_sort = "new"
            top_level_comments = list(submission.comments)
            max_comments = 10
            st.subheader(title)
            for comment in top_level_comments[:max_comments]:
                st.text(comment.body)
                st.divider()
