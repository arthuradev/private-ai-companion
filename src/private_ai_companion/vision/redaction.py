from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern

from private_ai_companion.vision.models import (
    RedactionFinding,
    RedactionResult,
    ScreenshotImage,
)


@dataclass(frozen=True, slots=True)
class TextRedactionRule:
    rule_id: str
    pattern: Pattern[str]
    replacement: str


DEFAULT_TEXT_REDACTION_RULES = (
    TextRedactionRule(
        rule_id="email",
        pattern=re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        replacement="[redacted-email]",
    ),
    TextRedactionRule(
        rule_id="secret-assignment",
        pattern=re.compile(
            r"\b(api[_-]?key|token|secret|password)\s*[:=]\s*\S+",
            re.I,
        ),
        replacement=r"\1=[redacted-secret]",
    ),
)


@dataclass(frozen=True, slots=True)
class MetadataTextRedactor:
    enabled: bool = True
    rules: tuple[TextRedactionRule, ...] = DEFAULT_TEXT_REDACTION_RULES

    def redact(self, screenshot: ScreenshotImage) -> RedactionResult:
        visible_text = screenshot.metadata.get("visible_text", "")
        if not self.enabled or not visible_text:
            return RedactionResult(screenshot=screenshot, visible_text=visible_text)

        redacted_text = visible_text
        findings: list[RedactionFinding] = []
        for rule in self.rules:
            redacted_text, count = rule.pattern.subn(rule.replacement, redacted_text)
            if count > 0:
                findings.append(RedactionFinding(rule_id=rule.rule_id, count=count))

        metadata = dict(screenshot.metadata)
        metadata["visible_text"] = redacted_text
        return RedactionResult(
            screenshot=ScreenshotImage(
                screenshot_id=screenshot.screenshot_id,
                request_id=screenshot.request_id,
                content=screenshot.content,
                image_format=screenshot.image_format,
                width=screenshot.width,
                height=screenshot.height,
                source=screenshot.source,
                captured_at=screenshot.captured_at,
                persist=screenshot.persist,
                metadata=metadata,
            ),
            visible_text=redacted_text,
            findings=tuple(findings),
        )
