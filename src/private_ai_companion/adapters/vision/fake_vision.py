from __future__ import annotations

from dataclasses import dataclass

from private_ai_companion.vision import (
    VisionAnalysisRequest,
    VisionAnalysisResult,
    VisionAnalysisStatus,
)


@dataclass(frozen=True, slots=True)
class FakeVisionProvider:
    provider_id: str = "fake-vision"

    async def analyze(self, request: VisionAnalysisRequest) -> VisionAnalysisResult:
        text_summary = (
            request.visible_text
            if request.visible_text
            else "sem texto visivel informado"
        )
        return VisionAnalysisResult(
            provider_id=self.provider_id,
            request_id=request.request_id,
            status=VisionAnalysisStatus.READY,
            summary=(
                "Contexto visual fake local; nenhuma imagem foi enviada para "
                f"API externa. Texto observado: {text_summary}"
            ),
            labels=("fake-screen", "local-only"),
            visible_text=request.visible_text,
            safety_notes=("temporary-context", "no-external-api"),
        )
