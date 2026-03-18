from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="ContentForge")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "anthropic/claude-sonnet-4-20250514"


class GenerateRequest(BaseModel):
    topic: str
    tone: str = "professional"
    length: str = "medium"
    keywords: str = ""


def call_ai(system: str, prompt: str, max_tokens: int = 3000) -> str:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": max_tokens,
            },
            timeout=90,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="AI request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


@app.post("/generate")
async def generate_content(req: GenerateRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic is required")

    kw_section = f"\nTarget keywords: {req.keywords}" if req.keywords.strip() else ""

    # Generate blog post
    blog_system = (
        "You are an expert SEO content writer. Write engaging, well-structured blog posts "
        "optimized for search engines. Use markdown formatting with proper headings (H2, H3), "
        "bullet points, and clear structure. Include a compelling introduction and conclusion."
    )
    blog_prompt = (
        f"Write a {req.length}-length SEO-optimized blog post about: {req.topic}\n"
        f"Tone: {req.tone}{kw_section}\n\n"
        f"Length guide: short=400 words, medium=800 words, long=1500 words.\n"
        f"Include a meta description at the top (150 chars max)."
    )
    blog = call_ai(blog_system, blog_prompt, 4000)

    # Generate social media posts
    social_system = (
        "You are a social media marketing expert. Create engaging, platform-optimized posts. "
        "Use relevant hashtags. Make content shareable and engaging."
    )
    social_prompt = (
        f"Based on this topic: {req.topic}\nTone: {req.tone}\n\n"
        f"Generate social media posts for each platform. Separate each with '---PLATFORM---' markers:\n\n"
        f"---TWITTER---\n(Write a Twitter/X post, max 280 chars, with hashtags)\n\n"
        f"---LINKEDIN---\n(Write a LinkedIn post, professional, 150-300 words, with hashtags)\n\n"
        f"---INSTAGRAM---\n(Write an Instagram caption, engaging, with emojis and hashtags, include CTA)"
    )
    social = call_ai(social_system, social_prompt, 2000)

    # Parse social posts
    twitter = linkedin = instagram = ""
    parts = social.split("---")
    current = ""
    for part in parts:
        stripped = part.strip()
        if stripped.upper() in ("TWITTER", "TWITTER---"):
            current = "twitter"
        elif stripped.upper() in ("LINKEDIN", "LINKEDIN---"):
            current = "linkedin"
        elif stripped.upper() in ("INSTAGRAM", "INSTAGRAM---"):
            current = "instagram"
        elif current and stripped:
            if current == "twitter":
                twitter += stripped + "\n"
            elif current == "linkedin":
                linkedin += stripped + "\n"
            elif current == "instagram":
                instagram += stripped + "\n"

    # Fallback: if parsing failed, use whole social as linkedin
    if not twitter and not linkedin and not instagram:
        linkedin = social

    return {
        "blog": blog.strip(),
        "twitter": twitter.strip() or "Could not generate Twitter post. Try again.",
        "linkedin": linkedin.strip() or "Could not generate LinkedIn post. Try again.",
        "instagram": instagram.strip() or "Could not generate Instagram post. Try again.",
    }


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
