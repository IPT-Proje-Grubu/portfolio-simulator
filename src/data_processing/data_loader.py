from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatasetInfo:
    path: Path
    columns: list[str]
    row_count: int


class DataLoader:
    """Loads lightweight CSV metadata before full pandas integration."""

    def inspect_csv(self, file_path: str) -> DatasetInfo:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Dosya bulunamadi: {file_path}")
        if path.suffix.lower() != ".csv":
            raise ValueError("Su anda sadece CSV dosyalari destekleniyor.")

        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            try:
                columns = next(reader)
            except StopIteration as error:
                raise ValueError("CSV dosyasi bos.") from error

            row_count = sum(1 for _ in reader)

        normalized_columns = [column.strip() for column in columns]
        return DatasetInfo(path=path, columns=normalized_columns, row_count=row_count)
