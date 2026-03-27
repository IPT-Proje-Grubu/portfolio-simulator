from __future__ import annotations

from dataclasses import dataclass

from src.data_processing.data_loader import DatasetInfo


@dataclass
class CleanedDataset:
    columns: list[str]
    row_count: int
    date_column: str | None
    price_columns: list[str]


class DataCleaner:
    """Prepares CSV metadata for future pandas-based cleaning steps."""

    DATE_CANDIDATES = {"date", "timestamp", "datetime"}
    PRICE_CANDIDATES = {"close", "open", "high", "low", "price", "adj close"}

    def build_cleaning_plan(self, dataset_info: DatasetInfo) -> CleanedDataset:
        normalized_columns = [column.strip().lower() for column in dataset_info.columns]

        date_column = None
        for original, normalized in zip(dataset_info.columns, normalized_columns):
            if normalized in self.DATE_CANDIDATES:
                date_column = original
                break

        price_columns = [
            original
            for original, normalized in zip(dataset_info.columns, normalized_columns)
            if normalized in self.PRICE_CANDIDATES
        ]

        return CleanedDataset(
            columns=dataset_info.columns,
            row_count=dataset_info.row_count,
            date_column=date_column,
            price_columns=price_columns,
        )
