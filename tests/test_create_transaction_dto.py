import pytest
from pytest_mock import MockerFixture
from application.dtos.create_transaction_dto import CreateTransactionDTO
from domain.entities.transaction import TransactionBase
from domain.enums.transaction_status import TransactionStatus


@pytest.fixture
def dto_with_zero_amount():
    return CreateTransactionDTO(0.0, "SUCCESS")


@pytest.fixture
def dto_with_large_amount():
    return CreateTransactionDTO(999999.99, "SUCCESS")


@pytest.fixture
def dto_with_decimal_amount():
    return CreateTransactionDTO(123.45, "PENDING")


@pytest.fixture
def entity_with_pending_status():
    return TransactionBase(
        id=2,
        amount=50.0,
        status=TransactionStatus.PENDING
    )


@pytest.fixture
def entity_with_failed_status():
    return TransactionBase(
        id=3,
        amount=75.50,
        status=TransactionStatus.FAILED
    )


class TestCreateTransactionDTOEdgeCases:
    """Test edge cases for CreateTransactionDTO"""

    def test_to_entity_with_zero_amount(self, dto_with_zero_amount):
        """Test conversion with zero amount"""
        result = dto_with_zero_amount.to_entity()
        
        assert isinstance(result, TransactionBase)
        assert result.amount == 0.0
        assert result.status == TransactionStatus.SUCCESS

    def test_to_entity_with_large_amount(self, dto_with_large_amount):
        """Test conversion with large amount"""
        result = dto_with_large_amount.to_entity()
        
        assert isinstance(result, TransactionBase)
        assert result.amount == 999999.99
        assert result.status == TransactionStatus.SUCCESS

    def test_to_entity_with_decimal_precision(self, dto_with_decimal_amount):
        """Test that decimal values are preserved"""
        result = dto_with_decimal_amount.to_entity()
        
        assert result.amount == 123.45
        assert result.status == TransactionStatus.PENDING

    def test_to_entity_id_is_always_none(self, dto_with_zero_amount):
        """Test that to_entity always sets id to None"""
        result = dto_with_zero_amount.to_entity()
        
        assert result.id is None


class TestCreateTransactionDTOFromEntityComprehensive:
    """Comprehensive tests for from_entity static method"""

    def test_from_entity_with_pending_status(self, entity_with_pending_status):
        """Test from_entity with PENDING status"""
        result = CreateTransactionDTO.from_entity(entity_with_pending_status)
        
        assert isinstance(result, CreateTransactionDTO)
        assert result.amount == 50.0
        assert result.status == "PENDING"

    def test_from_entity_with_failed_status(self, entity_with_failed_status):
        """Test from_entity with FAILED status"""
        result = CreateTransactionDTO.from_entity(entity_with_failed_status)
        
        assert isinstance(result, CreateTransactionDTO)
        assert result.amount == 75.50
        assert result.status == "FAILED"

    def test_from_entity_preserves_amount_as_float(self, entity_with_pending_status):
        """Test that amount is converted to float"""
        result = CreateTransactionDTO.from_entity(entity_with_pending_status)
        
        assert isinstance(result.amount, float)
        assert result.amount == 50.0

    def test_from_entity_status_is_string(self, entity_with_pending_status):
        """Test that status is a string value"""
        result = CreateTransactionDTO.from_entity(entity_with_pending_status)
        
        assert isinstance(result.status, str)
        assert result.status == "PENDING"


class TestCreateTransactionDTORoundTrip:
    """Test round-trip conversions (DTO -> Entity -> DTO)"""

    def test_round_trip_to_entity_and_back(self):
        """Test converting DTO to Entity and back to DTO"""
        original_dto = CreateTransactionDTO(200.0, "SUCCESS")
        
        # DTO -> Entity
        entity = original_dto.to_entity()
        
        # Entity -> DTO
        result_dto = CreateTransactionDTO.from_entity(entity)
        
        assert result_dto.amount == original_dto.amount
        assert result_dto.status == original_dto.status

    def test_round_trip_preserves_decimal_values(self):
        """Test that decimal precision is preserved in round-trip"""
        original_dto = CreateTransactionDTO(99.99, "PENDING")
        
        entity = original_dto.to_entity()
        result_dto = CreateTransactionDTO.from_entity(entity)
        
        assert result_dto.amount == 99.99

    def test_round_trip_with_pending_status(self):
        """Test round-trip with PENDING status"""
        original_dto = CreateTransactionDTO(150.50, "PENDING")
        
        entity = original_dto.to_entity()
        result_dto = CreateTransactionDTO.from_entity(entity)
        
        assert result_dto.status == "PENDING"


class TestCreateTransactionDTODataTypes:
    """Test data type handling and validation"""

    def test_amount_field_accepts_float(self):
        """Test that amount field accepts float"""
        dto = CreateTransactionDTO(100.5, "SUCCESS")
        assert isinstance(dto.amount, float)

    def test_amount_field_accepts_int(self):
        """Test that amount field accepts int"""
        dto = CreateTransactionDTO(100, "SUCCESS")
        assert isinstance(dto.amount, int)

    def test_status_field_is_string(self):
        """Test that status field is a string"""
        dto = CreateTransactionDTO(100.0, "SUCCESS")
        assert isinstance(dto.status, str)

    def test_dto_creation_with_different_status_values(self):
        """Test DTO creation with all valid status values"""
        statuses = ["SUCCESS", "PENDING", "FAILED"]
        
        for status in statuses:
            dto = CreateTransactionDTO(100.0, status)
            assert dto.status == status


class TestCreateTransactionDTOErrorHandling:
    """Test error handling and invalid inputs"""

    def test_to_entity_with_invalid_status_raises_value_error(self):
        """Test that invalid status raises ValueError"""
        dto = CreateTransactionDTO(100.0, "INVALID_STATUS")
        
        with pytest.raises(ValueError):
            dto.to_entity()

    def test_from_entity_with_mock(self, mocker: MockerFixture):
        """Test from_entity with mocked entity"""
        mock_entity = mocker.MagicMock(spec=TransactionBase)
        mock_entity.amount = 250.0
        mock_entity.status = TransactionStatus.SUCCESS
        
        result = CreateTransactionDTO.from_entity(mock_entity)
        
        assert result.amount == 250.0
        assert result.status == "SUCCESS"
