from typing import Dict, Any
from config.config import QWEN_MODEL
import asyncio
import json
import openai


async def ai_on(text: str) -> Dict[str, Any]:
    prompt = f"""Ты - эксперт по оценке исследовательских работ школьников. 
Оцени работу по критериям (каждый от 0 до 10):

1. АКТУАЛЬНОСТЬ - насколько тема важна и современна, есть ли обоснование выбора темы, ссылки на актуальные источники
2. НОВИЗНА - есть ли новые идеи, оригинальность подхода, отличие от аналогичных работ, сформулирована ли гипотеза
3. СТРУКТУРА - наличие введения, глав первой и второй, заключения, списка литературы, логичность построения, связность разделов
4. МЕТОДОЛОГИЯ - корректность выбранных методов, их описание, обоснование, репрезентативность выборки
5. ЗНАЧИМОСТЬ - практическая и теоретическая значимость, возможность применения результатов, конкретные рекомендации
6. ГРАМОТНОСТЬ - качество изложения, язык, стиль, отсутствие орфографических и пунктуационных ошибок

Текст работы:
\"\"\"{text[:80000]}\"\"\"

Верни ответ ТОЛЬКО в формате JSON:
{{
    "scores": {{
        "актуальность": число,
        "новизна": число,
        "структура": число,
        "методология": число,
        "значимость": число,
        "грамотность": число
    }},
    "total_score": число,
    "level": "низкий/средний/высокий",
    "strengths": ["сильная сторона 1", "сильная сторона 2", "сильная сторона 3"],
    "weaknesses": ["слабая сторона 1", "слабая сторона 2", "слабая сторона 3"],
    "recommendations": ["рекомендация 1", "рекомендация 2", "рекомендация 3"]
}}
"""

    try:
        def sync_call():
            return openai.ChatCompletion.create(
                model=QWEN_MODEL,
                messages=[
                    {"role": "system",
                     "content": "Ты эксперт по оценке исследовательских работ. Отвечай только в формате JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=8000
            )

        response = await asyncio.to_thread(sync_call)
        result_text = response.choices[0].message.content

        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()

        return json.loads(result_text)

    except Exception as e:
        return {"error": str(e)}