import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import ollama


load_dotenv()

prompt = """
You are a technical content summarizer and visualizer. Your task is to create a detailed summary of the provided transcript. The summary should be divided into the following sections:

Key Points: List the most important points from the tutorial as clear, concise bullet points.
Detailed Summary: Provide a well-organized, paragraph-based summary of the content.
Examples: Highlight key examples or use cases mentioned in the tutorial.
Comparisons: Compare the concepts or tools discussed with others, using tables or bullet points.
Visual Representation: Identify opportunities to include diagrams or flowcharts that represent key concepts or processes.
Additional Insights: Include any other relevant details, such as tips, best practices, or future trends.
Ensure that the summary is comprehensive and captures the essence of the tutorial without limiting the word count. Use bullet points, paragraphs, tables, and diagrams where appropriate to present the information clearly and effectively.
Example: {EG1}
Input: {TRANSCRIPT}
"""
EG1 = """
**Key Points:**

 - Kubernetes is an open-source platform for automating deployment, scaling, and management of containers.
 - Kubernetes manages clusters of machines running containers.
 - Comparison with Docker Swarm: Kubernetes offers more advanced features for orchestration.

**Detailed Summary:**
Kubernetes is a powerful tool for managing containerized applications. 
It automates the process of deployment, scaling, and management, making it easier to 
handle clusters of machines. Unlike Docker Swarm, Kubernetes provides more advanced 
orchestration features, which makes it a preferred choice for larger and more complex 
applications.

**Examples:**
 - Kubernetes: Used by large-scale applications like Airbnb and Google.
 - Docker Swarm: Preferred for simpler, smaller-scale deployments.

**Comparisons:**
| Feature | Kubernetes | Docker Swarm |
| --- | --- | --- |
|Complexity | Higher (more features) | Lower (simpler to set up) |
|Scalability | Excellent for large clusters | Better for smaller setups|
|Ecosystem Support | Extensive | Limited|

**Visual Representation:**
Diagram: A flowchart showing the lifecycle of a Kubernetes deployment from Pod creation to scaling.

**Additional Insights:**
Kubernetes’ robustness comes with a steeper learning curve, but the payoff in scalability and flexibility is significant, especially for enterprises.
"""



# """
# You are a youtube video summarizer who takes input as transcript text
# and summarizes entire point. You will provide the important summary in points
# within 250 words. Generate the summary of the text provided here : {TRANSCRIPT}
# """

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
    return ollama.get_results(prompt.format(TRANSCRIPT=transcript, EG1= EG1))

st.title("YT: Get Video summary")
yt_link = st.sidebar.text_input("Enter video url (preferably Youtube):")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.sidebar.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    # st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed notes"):
    transcript_info = get_video_transcript(yt_link)
    if transcript_info:
        summary = use_ollama_to_get_summary(transcript_info)
        st.markdown("### Video Summary:")
        st.write(summary)