import sys
import importlib

packages_to_test = [
    "fastapi_config_patterns",
    "fastapi_middleware_toolkit",
    "postgres_data_sanitizers",
    "pydantic_response_models",
    "python_app_exceptions",
    "python_cqrs_core",
    "python_cqrs_dispatcher",
    "python_domain_events",
    "python_dto_mappers",
    "python_infrastructure_exceptions",
    "python_input_validation",
    "python_mediator",
    "python_outbox_core",
    "python_structlog_config",
    "python_technical_primitives",
    "sqlalchemy_async_repositories",
    "sqlalchemy_async_session_factory"
]

def main():
    print("Testing imports for all 17 packages from TestPyPI...")
    
    success_count = 0
    failed_packages = []
    
    for pkg in packages_to_test:
        try:
            # We use importlib to dynamically import the module by its name
            module = importlib.import_module(pkg)
            print(f"[\u2713] Successfully imported: {pkg} (from {module.__file__})")
            success_count += 1
        except Exception as e:
            print(f"[x] Failed to import {pkg}: {e}")
            failed_packages.append(pkg)

    print("\n--- Summary ---")
    print(f"Total tested: {len(packages_to_test)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(failed_packages)}")
    
    if failed_packages:
        print("\nFailed to import the following packages:")
        for pkg in failed_packages:
            print(f" - {pkg}")
        sys.exit(1)
    else:
        print("\nAll 17 libraries installed and imported successfully! \U0001f389")

if __name__ == "__main__":
    main()
