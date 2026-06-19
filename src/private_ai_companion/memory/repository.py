from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from private_ai_companion.memory.models import (
    MemoryAuditEntry,
    MemoryCandidate,
    MemoryRecord,
    MemorySensitivity,
    MemorySource,
    MemoryStatus,
)


class SQLiteMemoryRepository:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        if database_path != Path(":memory:"):
            database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def create_from_candidate(
        self,
        candidate: MemoryCandidate,
        *,
        status: MemoryStatus,
        reason: str,
    ) -> MemoryRecord:
        now = datetime.now(UTC)
        memory_id = str(uuid4())
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO memories (
                    memory_id, content, source, sensitivity, confidence,
                    status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    memory_id,
                    candidate.content.strip(),
                    candidate.source.value,
                    candidate.sensitivity.value,
                    candidate.confidence,
                    status.value,
                    self._serialize_datetime(candidate.created_at),
                    self._serialize_datetime(now),
                ),
            )
            self._insert_audit_entry(
                connection,
                memory_id=memory_id,
                action="candidate_created",
                status=status,
                reason=reason,
            )
        return self.get(memory_id)

    def get(self, memory_id: str) -> MemoryRecord:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT memory_id, content, source, sensitivity, confidence,
                       status, created_at, updated_at
                FROM memories
                WHERE memory_id = ?
                """,
                (memory_id,),
            ).fetchone()

        if row is None:
            raise KeyError(memory_id)
        return self._row_to_record(row)

    def list_by_status(self, status: MemoryStatus) -> tuple[MemoryRecord, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT memory_id, content, source, sensitivity, confidence,
                       status, created_at, updated_at
                FROM memories
                WHERE status = ?
                ORDER BY created_at ASC
                """,
                (status.value,),
            ).fetchall()
        return tuple(self._row_to_record(row) for row in rows)

    def search_approved(self, query: str) -> tuple[MemoryRecord, ...]:
        normalized_query = query.strip()
        if not normalized_query:
            return ()

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT memory_id, content, source, sensitivity, confidence,
                       status, created_at, updated_at
                FROM memories
                WHERE status = ?
                  AND content LIKE ?
                ORDER BY updated_at DESC
                """,
                (MemoryStatus.APPROVED.value, f"%{normalized_query}%"),
            ).fetchall()
        return tuple(self._row_to_record(row) for row in rows)

    def update_status(
        self,
        memory_id: str,
        *,
        status: MemoryStatus,
        reason: str,
    ) -> MemoryRecord:
        now = datetime.now(UTC)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE memories
                SET status = ?, updated_at = ?
                WHERE memory_id = ?
                """,
                (status.value, self._serialize_datetime(now), memory_id),
            )
            if cursor.rowcount == 0:
                raise KeyError(memory_id)
            self._insert_audit_entry(
                connection,
                memory_id=memory_id,
                action=f"status_changed_to_{status.value}",
                status=status,
                reason=reason,
            )
        return self.get(memory_id)

    def update_content(
        self,
        memory_id: str,
        *,
        content: str,
        reason: str,
    ) -> MemoryRecord:
        normalized_content = content.strip()
        if not normalized_content:
            raise ValueError("memory content cannot be empty")

        existing = self.get(memory_id)
        now = datetime.now(UTC)
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE memories
                SET content = ?, updated_at = ?
                WHERE memory_id = ?
                """,
                (normalized_content, self._serialize_datetime(now), memory_id),
            )
            if cursor.rowcount == 0:
                raise KeyError(memory_id)
            self._insert_audit_entry(
                connection,
                memory_id=memory_id,
                action="content_updated",
                status=existing.status,
                reason=reason,
            )
        return self.get(memory_id)

    def delete(self, memory_id: str, *, reason: str) -> MemoryRecord:
        return self.update_status(memory_id, status=MemoryStatus.DELETED, reason=reason)

    def audit_entries(self, memory_id: str) -> tuple[MemoryAuditEntry, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT audit_id, memory_id, action, status, reason, created_at
                FROM memory_audit_log
                WHERE memory_id = ?
                ORDER BY created_at ASC
                """,
                (memory_id,),
            ).fetchall()
        return tuple(self._row_to_audit_entry(row) for row in rows)

    def _initialize_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT NOT NULL,
                    sensitivity TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_memories_status
                    ON memories(status);

                CREATE TABLE IF NOT EXISTS memory_audit_log (
                    audit_id TEXT PRIMARY KEY,
                    memory_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(memory_id) REFERENCES memories(memory_id)
                );

                CREATE INDEX IF NOT EXISTS idx_memory_audit_memory_id
                    ON memory_audit_log(memory_id);
                """
            )

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection]:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _insert_audit_entry(
        self,
        connection: sqlite3.Connection,
        *,
        memory_id: str,
        action: str,
        status: MemoryStatus,
        reason: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO memory_audit_log (
                audit_id, memory_id, action, status, reason, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid4()),
                memory_id,
                action,
                status.value,
                reason,
                self._serialize_datetime(datetime.now(UTC)),
            ),
        )

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> MemoryRecord:
        return MemoryRecord(
            memory_id=str(row["memory_id"]),
            content=str(row["content"]),
            source=MemorySource(str(row["source"])),
            sensitivity=MemorySensitivity(str(row["sensitivity"])),
            confidence=float(row["confidence"]),
            status=MemoryStatus(str(row["status"])),
            created_at=SQLiteMemoryRepository._parse_datetime(str(row["created_at"])),
            updated_at=SQLiteMemoryRepository._parse_datetime(str(row["updated_at"])),
        )

    @staticmethod
    def _row_to_audit_entry(row: sqlite3.Row) -> MemoryAuditEntry:
        return MemoryAuditEntry(
            audit_id=str(row["audit_id"]),
            memory_id=str(row["memory_id"]),
            action=str(row["action"]),
            status=MemoryStatus(str(row["status"])),
            reason=str(row["reason"]),
            created_at=SQLiteMemoryRepository._parse_datetime(str(row["created_at"])),
        )

    @staticmethod
    def _serialize_datetime(value: datetime) -> str:
        return value.astimezone(UTC).isoformat()

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
