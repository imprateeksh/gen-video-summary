import streamlit as st
from dotenv import load_dotenv
from constants import prompt, EG1, prompt_notes, IMG_URL
from youtube_transcript_api import YouTubeTranscriptApi
import ollama


load_dotenv()

def get_video_transcript(yt_video_url):
    try:
        video_id = yt_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # output of transcript is like this - 
        # v\[{'text': "today I'm sharing with you five python", 'start': 0.12, 'duration': 4.96}, {'text': 'AI projects and exactly how to build', 'start': 2.6, 'duration': 4.279}, {...}]
        # We will get list, so will try to make as paragraph
        txt = ""
        for t in transcript:
            txt += " " + t["text"]
        return txt
    except Exception as ex:
        raise ex


def use_ollama_to_get_summary(transcript: str, prompt: str = prompt):
    # return ollama.get_results(prompt_notes.format(TRANSCRIPT=transcript))
    return ollama.get_results(prompt.format(TRANSCRIPT=transcript, EG1= EG1))

st.title("Get Youtube Video summary")
yt_link = st.sidebar.text_input("Youtube video url:")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.sidebar.image(
        IMG_URL.format(video_id=video_id), 
        use_column_width=True
    )

if st.button("Get detailed notes"):
    transcript_info = get_video_transcript(yt_link)
    if transcript_info:
        summary = use_ollama_to_get_summary(transcript_info)
        st.markdown("### Video Summary:")
        st.write(summary)