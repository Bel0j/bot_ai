from typing import Dict, Any
from aiogram.utils.markdown import hbold


def format_result(result: Dict[str, Any]) -> str:
    """Форматирует результат для отправки"""

    if "error" in result:
        return f"❌ <b>Ошибка:</b> {result['error']}"

    try:
        scores = result.get("scores", {})
        total = result.get("total_score", 0)
        level = result.get("level", "не определен")
        strengths = result.get("strengths", [])
        weaknesses = result.get("weaknesses", [])
        recommendations = result.get("recommendations", [])

        level_emoji = {"низкий": "🔴", "средний": "🟡", "высокий": "🟢"}.get(level.lower(), "⚪")

        response = f"{hbold('📊 РЕЗУЛЬТАТЫ ОЦЕНКИ')}\n\n"
        response += f"{level_emoji} {hbold('Уровень:')} {level.upper()}\n"
        response += f"{hbold('📈 Общий балл:')} {total}/60\n\n"

        response += f"{hbold('📝 Оценки по критериям:')}\n"

        for criterion, score in scores.items():
            stars = "★" * (score // 2) + "☆" * (5 - (score // 2))
            response += f"• {criterion}: {score}/10 {stars}\n"

        if strengths:
            response += f"\n{hbold('✅ Сильные стороны:')}\n"
            for s in strengths[:3]:
                response += f"• {s}\n"

        if weaknesses:
            response += f"\n{hbold('⚠️ Что можно улучшить:')}\n"
            for w in weaknesses[:3]:
                response += f"• {w}\n"

        if recommendations:
            response += f"\n{hbold('📌 Рекомендации:')}\n"
            for r in recommendations[:3]:
                response += f"• {r}\n"

        return response

    except Exception:
        return "❌ Ошибка при формировании результата"