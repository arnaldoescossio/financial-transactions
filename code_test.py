

from application.use_cases.enums.transaction_use_case_type import TransactionUseCaseType


use_case_type = TransactionUseCaseType.CREATE
slug, use_case_class = use_case_type.value

print(f"Use case type: {use_case_type}, Slug: {slug}, Use case class: {use_case_class}")