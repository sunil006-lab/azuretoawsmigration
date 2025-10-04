# Azure-to-AWS Migration Agent 🚀
# AI-Driven Cloud Service Conversion Tool” (CCT)
## Overview - AI-Driven Cloud Service Conversion Tool” (CCT)
This AI-powered migration agent automates the transition of IAM policies, CI/CD pipelines, and cloud service configurations from Azure to AWS. Built with a modular architecture, it enables seamless integration of new services and ensures compliance, traceability, and operational continuity.

## 🔧 Features
- IAM policy validation and migration (Azure AD → AWS IAM)
- CI/CD pipeline mapping (Azure DevOps → AWS CodePipeline)
- Extensible service modules (S3, Lambda, RDS, etc.)
- Centralized logging, error handling, and reporting
- Config-driven orchestration for flexible execution

## 🧩 Directory Structure
migration_agent/
├── core/                  # Shared orchestration logic
│   └── runner.py
├── services/              # Each cloud service gets its own module
│   ├── iam/
│   ├── cicd/
│   ├── s3/
│   ├── lambda/
│   └── rds/
├── utils/                 # Common helpers (logging, config, auth)
├── config/                # YAML/JSON configs for service mappings
└── main.py
|-- run_all.py             # Script to run all services


## 🚀 Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AzuretoAWS-migration-agent.git
cd AzuretoAWS-migration-agent

Install Dependencies
```bash
pip install -r requirements.txt
```
### 2. Configure Migration Settings
Edit the `config/migration_config.yaml` file to specify your Azure and AWS credentials, target
regions, and any specific service mappings you need.
Set environment variables or use SDK config files:
• 	Azure:  AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECERET
• 	AWS: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
### 3. Run the Migration Agent
```bash
python main.py --config config/default.yaml
```

### 4. Monitor Progress
Check the logs in `logs/migration.log` for detailed progress and any errors encountered during the migration.
## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details
## 📞 Support
For issues or feature requests, please open an issue on GitHub or contact the maintainers at
[AzuretoAWS-migration-agent](https://github.com/your-username/AzuretoAWS-migration-agent)

🧠Adding a New Service
To add a new cloud service migration:
- Create a folder under services/ (e.g., services/ec2)
- Implement a run(config, logger) method
- Register the service in core/runner.py
- Add config templates in config/
- Write unit tests in tests/
🤝 Contributing
Pull requests and feature ideas are welcome! Please follow modular design principles and include test coverage.
📜 License
MIT License
📬 Contact
For support or collaboration, reach out to the project team at [kumarm.1@tcs.com, sunilmkr79@gmail.com]

## Run instructions: (select specific services to migrate)
```bash
python main.py --services iam s3 lambda rds cicd --config config/default.yaml
```
## 🧪 Testing
```bash
pytest tests/
```	
## Run instructions: (run all services)
```bash
python run_all.py
```
## 📝 Documentation
```bash	
python docs/generate_docs.py
```

