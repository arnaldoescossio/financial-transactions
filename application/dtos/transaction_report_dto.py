from dataclasses import dataclass

from application.dtos.base_dto import Dto

@dataclass
class TransactionReportDTO(Dto):
    valid_count: int
    total_amount: float
    average_amount: float
    failed_count: int
