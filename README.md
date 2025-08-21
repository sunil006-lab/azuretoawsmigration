# Azure-to-AWS Migration AI Agent

## Overview
This project provides an AI-powered agent to automate IAM policy validation and CI/CD pipeline mapping during Azure-to-AWS cloud migration. The solution streamlines migration, 
reduces manual effort, and ensures compliance and operational continuity.

## Features
- Automated IAM policy validation and migration from Azure to AWS.
- CI/CD pipeline mapping from Azure DevOps to AWS CodePipeline (or other AWS CI/CD services).
- Modular, extensible architecture for easy integration of new features.
- Logging and reporting for migration activities.

## Project Structure
- **AzuretoAWS_migration.py**: Main entry point for the migration agent.
- **iam_validation/**: Contains logic and modules for validating and migrating IAM policies from Azure to AWS.
  - **azure/**: Modules for handling Azure IAM policies.
  - **aws/**: Modules for handling AWS IAM policies.
  - **utils/**: Utility functions and classes used for IAM validation.
  - **tests/**: Unit tests for IAM validation logic.
- **cicd_mapping/**: Contains logic for mapping and automating CI/CD pipeline migration between Azure and AWS.
  - **azure/**: Modules for extracting and analyzing Azure DevOps pipelines.
  - **aws/**: Modules for generating AWS CodePipeline configurations.
  - **utils/**: Utility functions for pipeline mapping.
  - **tests/**: Unit tests for CI/CD mapping logic.
- **utils/**: Shared utility functions and helpers used across the project.
- **data/**: Sample data, configuration files, and migration templates.
- **tests/**: Integration and end-to-end tests for the overall migration process.
- **docs/**: Documentation, guides, and reference materials for users and developers.

## Requirements
- Python 3.8 or higher
- Azure SDK for Python
- Boto3 (AWS SDK for Python)
- Pytest (for testing)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/AzuretoAWS-migration.git
    cd AzuretoAWS-migration
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your Azure and AWS credentials:
    - For Azure, set the environment variables `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET`.
    - For AWS, configure your credentials using the AWS CLI or set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
4. Run the migration agent:
    ```bash
    python AzuretoAWS_migration.py
    ```
5. Monitor the migration process:
    - Check the logs for any errors or warnings.
    - Verify the migrated IAM policies and CI/CD pipelines in AWS.
6. Run tests to ensure everything is working correctly:
    ```bash
    pytest tests/
    ```

## Troubleshooting
- If you encounter any issues, check the logs for error messages.
- Ensure that your Azure and AWS credentials are correctly configured.
- Refer to the documentation for the Azure SDK and Boto3 for additional help.

## Contributing
Contributions are welcome! Please submit pull requests or open issues for feature requests and bug reports.

## License
This project is licensed under the MIT License.

## Contact
For support or inquiries, please contact the project team at [kumarm.1@tcs.com & sunilmkr79@gmail.com].