import base64
import json
import re

from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def encode_image(path: str) -> str:
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def extract_json(text: str) -> dict:
    """
    Иногда ИИ может вернуть JSON с лишним текстом.
    Эта функция пытается достать JSON из ответа.
    """
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("ИИ не вернул JSON")

    return json.loads(match.group(0))


async def analyze_site_structure(
    url: str,
    screenshot_path: str,
    page_text: str
) -> dict:
    image_base64 = encode_image(screenshot_path)

    prompt = f"""
Ты — ИИ-аналитик структуры сайтов и специалист по Tilda.

Пользователь дал ссылку на сайт:
{url}

Твоя задача:
- Не копировать сайт.
- Не копировать тексты.
- Не копировать изображения.
- Не генерировать HTML, CSS или JavaScript.
- Только определить структуру страницы.
- Вернуть список пустых блоков Tilda, которые нужно поставить в редакторе.

Бот будет только добавлять пустые блоки.
Он НЕ будет заполнять тексты, картинки, кнопки, цвета и настройки.

Разрешенные типы секций:
hero, features, about, services, gallery, reviews, pricing, faq, form, footer, other.

HTML-текст страницы:
{page_text}

Верни строго JSON без пояснений.

Формат:

{{
  "page_type": "landing",
  "sections": [
    {{
      "order": 1,
      "section_type": "hero",
      "human_name": "Первый экран",
      "reason": "На странице есть крупный первый экран с заголовком и кнопкой"
    }}
  ]
}}
"""

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    raw = response.output_text

    return extract_json(raw)
