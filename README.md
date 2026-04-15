# Monster Gaming SDK for Python

Official Python client for [Monster Gaming](https://monstergaming.ai) — an AI-powered game development platform for Unreal Engine, Unity, Godot, and bespoke engines.

## Installation

```bash
pip install monstergaming
```

## Quick Start

```python
from monstergaming import MonsterGaming

client = MonsterGaming(api_key="mg_your_api_key")

response = client.chat.completions.create(
    model="monster-gpt",
    messages=[
        {"role": "user", "content": "Generate a UE5 C++ character controller with double jump"},
    ],
)

print(response["choices"][0]["message"]["content"])
```

## Monster-GPT

`monster-gpt` is Monster Gaming's flagship model. It auto-detects your game engine and routes your query to a specialist agent — shader programming, networking, animation, level design, QA, and 25+ other disciplines.

```python
response = client.chat.completions.create(
    model="monster-gpt",
    messages=[
        {"role": "system", "content": "Engine: Unity 6. Language: C#."},
        {"role": "user", "content": "Implement object pooling for projectiles"},
    ],
)
```

## Available Models

```python
models = client.models.list()
for model in models["data"]:
    print(model["id"])
```

Budget models (Free tier): `monster-gpt`, `claude-haiku`, `deepseek-chat`, `codestral`, `gemini-3-flash`

Standard models (Starter+): `claude-sonnet`, `gpt-4o`, `gemini-3.1-pro`, `mistral-large`

Premium models (Pro+): `claude-opus`, `o3`, `gpt-5.4`

## Pricing

Free tier available — no credit card required. See [monstergaming.ai/pricing](https://monstergaming.ai/pricing) for details.

## Documentation

Full documentation at [monstergaming.ai/quickstart](https://monstergaming.ai/quickstart).

## License

MIT
