"""Repository testing mixin for common repository testing patterns.

This mixin provides common repository layer testing patterns that can be
inherited by repository test classes to reduce code duplication.

RULE: Maximum 100 lines per file.
"""


class RepositoryTestMixin:
    """Mixin providing common repository testing patterns."""
    
    def validate_repository_result_types(self, result, expected_type):
        """Validate that repository methods return expected types.
        
        Args:
            result: Result returned from repository method
            expected_type: Expected type or None
            
        Repository methods should return expected types or None for not found.
        """
        assert result is None or isinstance(result, expected_type), (
            f"Repository result should be {expected_type.__name__} or None, "
            f"got {type(result).__name__}"
        )
    
    def validate_boolean_repository_result(self, result):
        """Validate that repository methods return proper boolean values.
        
        Args:
            result: Result that should be a boolean
            
        Useful for existence checks, validation methods, etc.
        """
        assert isinstance(result, bool), (
            f"Repository result should be boolean, got {type(result).__name__}"
        )
    
    def validate_create_returns_object_with_id(self, created_obj):
        """Validate that create operations return object with identifier.
        
        Args:
            created_obj: Object returned from create operation
            
        Created objects should have some form of unique identifier.
        """
        assert created_obj is not None, "Create operation should return object"
        
        # Check for common identifier patterns
        has_id = hasattr(created_obj, 'id') and getattr(created_obj, 'id') is not None
        has_token = hasattr(created_obj, 'token') and getattr(created_obj, 'token') is not None
        has_uuid = hasattr(created_obj, 'uuid') and getattr(created_obj, 'uuid') is not None
        
        assert has_id or has_token or has_uuid, (
            "Created object should have non-null identifier (id, token, or uuid)"
        )
    
    def validate_retrieve_by_nonexistent_key_returns_none(self, repository, retrieve_method: str, nonexistent_key):
        """Validate that retrieving by non-existent key returns None.
        
        Args:
            repository: Repository instance to test
            retrieve_method: Name of the retrieve method to call
            nonexistent_key: Key that should not exist in repository
        """
        method = getattr(repository, retrieve_method)
        result = method(nonexistent_key)
        
        assert result is None, (
            f"Retrieving non-existent key should return None, got {type(result).__name__}"
        )
    
    def validate_update_preserves_id(self, original_obj, updated_obj):
        """Validate that update operations preserve object identifier.
        
        Args:
            original_obj: Original object before update
            updated_obj: Object after update operation
        """
        # Check if objects have ID field
        if hasattr(original_obj, 'id') and hasattr(updated_obj, 'id'):
            assert original_obj.id == updated_obj.id, (
                "Update operation should preserve object ID"
            )
        
        # Check if objects have token field
        if hasattr(original_obj, 'token') and hasattr(updated_obj, 'token'):
            assert original_obj.token == updated_obj.token, (
                "Update operation should preserve object token"
            )
