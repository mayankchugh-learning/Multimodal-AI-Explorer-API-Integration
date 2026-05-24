"""LangChain example code snippets for teaching (per modality + provider)."""

from __future__ import annotations

from src.providers import default_model


def _model(provider: str, override: str | None) -> str:
    if override and override.strip():
        return override.strip()
    return default_model(provider)


def get_langchain_code(modality_id: str, provider: str, model_override: str | None) -> str:
    provider = provider.lower()
    model = _model(provider, model_override)
    builders = {
        "text_to_text": _text_to_text,
        "text_to_image": _text_to_image,
        "image_to_text": _image_to_text,
        "text_to_audio": _text_to_audio,
        "audio_to_text": _audio_to_text,
        "video_to_text": _video_to_text,
        "text_to_video": _text_to_video,
    }
    builder = builders.get(modality_id, _generic)
    return builder(provider, model)


def _text_to_text(provider: str, model: str) -> str:
    if provider == "openai":
        return f'''# pip install langchain langchain-openai langchain-core
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="{model}",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.environ["OPENAI_API_KEY"],
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{{question}}"),
])

# LCEL chain: prompt | model | parser
chain = prompt | llm | StrOutputParser()

answer = chain.invoke({{"question": "Explain RAG in two sentences."}})
print(answer)
'''
    if provider == "anthropic":
        return f'''# pip install langchain langchain-anthropic langchain-core
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(
    model="{model}",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

response = llm.invoke([HumanMessage(content="Explain RAG in two sentences.")])
print(response.content)
'''
    if provider == "google":
        return f'''# pip install langchain langchain-google-genai langchain-core
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model="{model}",
    temperature=0.7,
    max_output_tokens=1024,
    google_api_key=os.environ["GOOGLE_API_KEY"],
)

chain = (
    ChatPromptTemplate.from_messages([("human", "{{question}}")])
    | llm
    | StrOutputParser()
)
print(chain.invoke({{"question": "Explain RAG in two sentences."}}))
'''
    if provider == "groq":
        return f'''# pip install langchain langchain-groq langchain-core
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="{model}",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.environ["GROQ_API_KEY"],
)

chain = ChatPromptTemplate.from_template("{{q}}") | llm | StrOutputParser()
print(chain.invoke({{"q": "Explain RAG in two sentences."}}))
'''
    if provider == "openrouter":
        return f'''# pip install langchain langchain-openai langchain-core
import os
from langchain_openai import ChatOpenAI

# OpenRouter is OpenAI-compatible
llm = ChatOpenAI(
    model="{model}",
    temperature=0.7,
    max_tokens=1024,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={{
        "HTTP-Referer": "https://your-app.example",
        "X-Title": "Student Demo",
    }},
)

print(llm.invoke("Explain RAG in two sentences.").content)
'''
    if provider == "huggingface":
        return f'''# pip install langchain langchain-huggingface langchain-core
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="{model}",
        huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
        temperature=0.7,
        max_new_tokens=1024,
    )
)

print(llm.invoke("Explain RAG in two sentences.").content)
'''
    if provider == "ollama":
        return f'''# pip install langchain langchain-ollama langchain-core
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="{model}", temperature=0.7)
chain = ChatPromptTemplate.from_template("{{q}}") | llm | StrOutputParser()
print(chain.invoke({{"q": "Explain RAG in two sentences."}}))
'''
    return _generic(provider, model)


def _image_to_text(provider: str, model: str) -> str:
    if provider in ("openai", "openrouter"):
        base = "openrouter" if provider == "openrouter" else "openai"
        extra = (
            '\n    base_url="https://openrouter.ai/api/v1",\n'
            '    api_key=os.environ["OPENROUTER_API_KEY"],\n'
            if provider == "openrouter"
            else '\n    api_key=os.environ["OPENAI_API_KEY"],\n'
        )
        return f'''# pip install langchain langchain-openai langchain-core
import base64
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="{model}", max_tokens=1024,{extra})

with open("photo.jpg", "rb") as f:
    b64 = base64.standard_b64encode(f.read()).decode()

message = HumanMessage(
    content=[
        {{"type": "text", "text": "Describe this image."}},
        {{
            "type": "image_url",
            "image_url": {{"url": f"data:image/jpeg;base64,{{b64}}"}},
        }},
    ]
)
print(llm.invoke([message]).content)
'''
    if provider == "anthropic":
        return f'''# pip install langchain langchain-anthropic
import base64
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="{model}", api_key=os.environ["ANTHROPIC_API_KEY"])

with open("photo.jpg", "rb") as f:
    data = base64.standard_b64encode(f.read()).decode()

msg = HumanMessage(
    content=[
        {{
            "type": "image",
            "source": {{
                "type": "base64",
                "media_type": "image/jpeg",
                "data": data,
            }},
        }},
        {{"type": "text", "text": "Describe this image."}},
    ]
)
print(llm.invoke([msg]).content)
'''
    if provider == "google":
        return f'''# pip install langchain langchain-google-genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="{model}", google_api_key=os.environ["GOOGLE_API_KEY"])

# Pass image path or PIL Image in HumanMessage content list
msg = HumanMessage(
    content=[
        "Describe this image.",
        {{"type": "image_url", "image_url": "photo.jpg"}},
    ]
)
print(llm.invoke([msg]).content)
'''
    if provider == "huggingface":
        return f'''# pip install langchain langchain-community huggingface_hub
import os
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])

with open("photo.jpg", "rb") as f:
    image_bytes = f.read()

# Captioning
caption = client.image_to_text(
    image=image_bytes,
    model="Salesforce/blip-image-captioning-large",
)
print(caption)

# Or VQA with a custom question:
answer = client.visual_question_answering(
    image=image_bytes,
    question="What is the main object?",
    model="Salesforce/blip-vqa-base",
)
print(answer)
'''
    if provider == "ollama":
        return f'''# pip install langchain langchain-ollama
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Use a vision model: ollama pull llava
llm = ChatOllama(model="llava")
# Attach local image path in multimodal message (check Ollama vision docs)
print(llm.invoke([HumanMessage(content="Describe photo.jpg")]).content)
'''
    return _unsupported(provider, "image → text")


def _text_to_image(provider: str, model: str) -> str:
    if provider == "openai":
        return '''# pip install langchain langchain-openai langchain-community
import os
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate

# High-level wrapper (teaching pattern)
dalle = DallEAPIWrapper(api_key=os.environ["OPENAI_API_KEY"], model="dall-e-3")

prompt = PromptTemplate.from_template("A watercolor of {subject}")
# In practice: bind prompt vars then call dalle.run(...)
image_url = dalle.run("a robot reading in a library")
print(image_url)
'''
    if provider == "huggingface":
        return f'''# pip install huggingface_hub
import os
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
image = client.text_to_image(
    "A robot reading in a library, watercolor",
    model="{model}",
)
image.save("output.png")
'''
    return _unsupported(provider, "text → image")


def _text_to_audio(provider: str, model: str) -> str:
    if provider == "openai":
        return '''# pip install openai
import os
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# LangChain: community OpenAI TTS tool or direct SDK (shown here)
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello students! This is multimodal AI.",
)
Path("speech.mp3").write_bytes(response.content)
'''
    return _unsupported(provider, "text → audio")


def _audio_to_text(provider: str, model: str) -> str:
    if provider == "openai":
        return '''# pip install langchain-openai openai
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

with open("audio.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
    )
print(transcript.text)

# LangChain wrapper alternative:
# from langchain_community.document_loaders import OpenAIWhisperParserLocal
'''
    if provider == "google":
        return f'''# pip install langchain-google-genai google-genai
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

with open("audio.mp3", "rb") as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model="{model}",
    contents=[
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/mpeg"),
        "Transcribe this audio. Return only the transcript.",
    ],
)
print(response.text)
'''
    if provider == "huggingface":
        return f'''# pip install huggingface_hub
import os
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])

with open("audio.mp3", "rb") as f:
    result = client.automatic_speech_recognition(
        audio=f.read(),
        model="{model}",
    )
print(result["text"] if isinstance(result, dict) else result)
'''
    return _unsupported(provider, "audio → text")


def _video_to_text(provider: str, model: str) -> str:
    return f'''# Teaching pattern: Video → Text via LangChain + tools
# Step 1: Extract frames (OpenCV) — same as this app's src/services/video.py
# Step 2: Vision LLM summarizes frames

# pip install langchain langchain-openai opencv-python-headless
import base64
import cv2
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="{model}", max_tokens=2048)

def frame_to_b64(frame_bgr) -> str:
    import base64
    _, buf = cv2.imencode(".jpg", frame_bgr)
    return base64.standard_b64encode(buf).decode()

cap = cv2.VideoCapture("lecture.mp4")
content = [{{"type": "text", "text": "Summarize this video from the frames."}}]
for i in range(6):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i * 100)
    ok, frame = cap.read()
    if ok:
        b64 = frame_to_b64(frame)
        content.append({{
            "type": "image_url",
            "image_url": {{"url": f"data:image/jpeg;base64,{{b64}}"}},
        }})
cap.release()

print(llm.invoke([HumanMessage(content=content)]).content)
'''


def _text_to_video(provider: str, model: str) -> str:
    return '''# Text → Video (conceptual LangChain agent pattern)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

@tool
def generate_video(prompt: str) -> str:
    """Call external API: Runway, Luma, or OpenAI Sora when available."""
    # return video_job_id or url
    return "Video API not configured in classroom demo."

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [generate_video]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You create videos by calling tools."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
# executor.invoke({"input": "A sunset timelapse over mountains"})
'''


def _unsupported(provider: str, task: str) -> str:
    return f"# Provider '{provider}' does not support {task} in this demo.\n# Select OpenAI, Gemini, Anthropic, Hugging Face, Groq, OpenRouter, or Ollama.\n"


def _generic(provider: str, model: str) -> str:
    return f"# Generic LangChain pattern for provider={provider}, model={model}\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\n# ... attach provider-specific ChatModel ...\n"
