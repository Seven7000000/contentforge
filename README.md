# ContentForge

Turn any topic into a full content package: SEO-optimized blog post + Twitter, LinkedIn, and Instagram posts -- all generated in one click.

![ContentForge Screenshot](static/screenshot.png)
<!-- Replace with actual screenshot -->

## Features

- **SEO Blog Generation** -- Full blog posts with meta descriptions, proper heading structure (H2/H3), and keyword optimization
- **Multi-Platform Social** -- Generates platform-specific posts for Twitter/X, LinkedIn, and Instagram simultaneously
- **Tone Control** -- Professional, casual, persuasive, or custom tone settings
- **Length Options** -- Short (400 words), medium (800 words), or long (1,500 words) blog posts
- **Keyword Targeting** -- Specify target keywords for SEO-focused content
- **Instant Output** -- All content formats generated in a single API call

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI Model | Claude Sonnet 4 via OpenRouter |
| Frontend | HTML + TailwindCSS (CDN) |

## Quick Start

### Prerequisites

- Python 3.10+
- OpenRouter API key ([get one here](https://openrouter.ai/keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/Seven7000000/contentforge.git
cd contentforge

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENROUTER_API_KEY="your-key-here"

# Run the server
uvicorn main:app --port 8002 --reload
```

Open [http://localhost:8002](http://localhost:8002) in your browser.

## API Reference

### `POST /generate`

Generate a complete content package from a topic.

**Request:**
```json
{
  "topic": "The future of remote work in 2026",
  "tone": "professional",
  "length": "medium",
  "keywords": "remote work, hybrid teams, productivity"
}
```

**Response:**
```json
{
  "blog": "## Meta Description\n...\n\n# The Future of Remote Work...",
  "twitter": "Remote work isn't going anywhere... #RemoteWork #FutureOfWork",
  "linkedin": "The landscape of remote work is shifting...",
  "instagram": "The office is wherever you are..."
}
```

### Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `topic` | string | required | Content topic |
| `tone` | string | `"professional"` | Writing tone |
| `length` | string | `"medium"` | Blog length: short, medium, long |
| `keywords` | string | `""` | Target SEO keywords (comma-separated) |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |

## Project Structure

```
contentforge/
  main.py             # FastAPI application
  requirements.txt    # Python dependencies
  static/
    index.html         # Single-page frontend
```

## License

MIT
