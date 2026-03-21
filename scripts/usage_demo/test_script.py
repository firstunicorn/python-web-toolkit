import sys
from pydantic_response_models.responses import SuccessResponse, ErrorResponse, ErrorDetail
from python_technical_primitives.text.operations import to_sentence_case, sanitize_filename
from python_app_exceptions.base import BaseApplicationException

def main():
    print("Testing 'python-technical-primitives'...")
    text = "hello world from our new package"
    sentence = to_sentence_case(text)
    print(f"Original text: '{text}'")
    print(f"Sentence case: '{sentence}'")
    
    dirty_name = "my file?*<name>.txt"
    clean_name = sanitize_filename(dirty_name)
    print(f"Dirty filename: '{dirty_name}'")
    print(f"Clean filename: '{clean_name}'")
    
    print("\nTesting 'pydantic-response-models'...")
    success_resp = SuccessResponse(data={"user": "admin", "id": 42}, message="User fetched successfully")
    print("Success Response JSON:")
    print(success_resp.model_dump_json(indent=2))
    
    error_resp = ErrorResponse(
        error="Validation failed",
        code="VAL_001",
        details=[ErrorDetail(field="email", message="Invalid email format")]
    )
    print("Error Response JSON:")
    print(error_resp.model_dump_json(indent=2))

    print("\nTesting 'python-app-exceptions'...")
    try:
        raise BaseApplicationException(message="Resource not found", details="User ID 42 does not exist in the database.")
    except BaseApplicationException as e:
        print(f"Caught exception: {e}")
        print(f"Message property: {e.message}")
        print(f"Details property: {e.details}")

    print("\nAll tests passed successfully! Libraries are working from TestPyPI.")

if __name__ == "__main__":
    main()
