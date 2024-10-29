<p align="center">
  <img src="https://github.com/user-attachments/assets/08ed8337-916c-4ae7-8c1c-66d26ff85329" alt="AWS Resource Inventory Extractor">
</p>

# AWS Resource Inventory Extractor

A module that uses awscli and the open-source tool Steampipe to extract AWS resources and export them to a structured inventory file.

This module supports a total of three modes.

- Extract pre-procesing inventory mode
  - VPC, VPC Endpoint, Peering Connection
  - Transit Gateway
  - Subnet
  - Security Groups
  - Network ACLs
  - EC2
  - ELB
  - Target Group
  - Auto Scaling
  - ElastiCache
  - CloudFront
  - S3
  - IAM Group, Role, User
  - RDS, DocumentDB

- Extract raw-data inventory mode
  - All active AWS resources

- Connect [Steampipe Query](https://steampipe.io/docs/query/query-shell) (In-Memory PostgreSQL Interface Tool) mode
  - Connect to In-MemoryDB

## Tech Stack
- [Steampipe wit aws plugin (Opensorce)](https://hub.steampipe.io/plugins/turbot/aws)
- awscli
- postgresql schema parser (In-house developed python code): v1.0.2

## Pre-requirements
- For fater extraction, 2 vCpu & 8 Ram are recommended
- Docker version: v27.3.1
- AWS Account: Read-Only Permissions (to security)
- Steampipe Config

## Execution Guide
### [ Prod Env ]
#### Dockerfile Build
```bash
docker build -t {{imageName}} .
```
#### Container Run
```bash
docker run --rm -it -v {{Your Host Directory}}:/app/inventory {{imageName}}
```
### [ Dev Env ]
#### Dockerfile Build
```bash
cd python
docker build -f Dockerfile -t {{dev-imageName}} .
```
#### Container Run
```bash
docker run -itd --name {{dev-containerName}} -v {{Your Host Directory}}:/app/inventory {{dev-imageName}}
```
#### Container exec
```bash
docker exec -it {{dev-containerName}} bash
```

## Steps of Operation
### [ 1 / 5 ] Authenticate with AWS using awscli: IAM or SSO.

- IAM Login
  - Input the below data to IAM login.
    ```
    AWS Access Key ID : (Your IAM user's Access Key ID here.)
    AWS Secret Access Key : (Your IAM user's Secret Access Key here.)
    Default region name : (Your Project Region)
    Default output format :json 
    ```

- SSO Login
  - Input the below data to SSO login.
    ```
    SSO session name (Recommended): hanwhavision
    SSO start URL [None]: https://htaic.awsapps.com/start
    SSO region [None]: us-west-2
    SSO registration scopes [sso:account:access]:
    ```
  - Open the following URL and enter the given code.
    
    ![image](https://github.com/user-attachments/assets/ade9aa67-a885-4117-ad52-375ae7ec55be)
  
  - After SSO login, allow access.
  
    ![image](https://github.com/user-attachments/assets/dd72cd0d-7060-45fb-8ae0-bf3b8f52967e)
  
  - If the login is successful and there are no issues with the permissions, the following screen will appear.
  - **Please select any option.**
  
    ![image](https://github.com/user-attachments/assets/d9119b03-fb31-40b4-a3c0-1985dd9deeb2)
  
  - Leave the "default client region", "default output format", and "profile name" fields blank.
  - Verify your role name.
  
    ![image](https://github.com/user-attachments/assets/89e1d050-121e-4bf0-8096-43efc0169251)
 
  - To overwrite aws config file, please enter the values in the format below.
  - **DO NOT USE "-". ONLY "_" IS ALLOWED**
    ```
    [profile {{project_1 profile name}}]
    sso_session = hanwhavision
    sso_account_id = {{project_1 AWS Account}}
    sso_role_name = {{Your role name}}
    region = us-east-1
    output = json
    [profile {{project_2 profile name}}]
    sso_session = hanwhavision
    sso_account_id = {{project_2 AWS Account}}
    sso_role_name = {{Your role name}}
    region = us-east-1
    output = json
    ...
    ```

### [ 2 / 5 ] Setup Steampipe config file.
#### IAM Login Method
- The IAM login Method Skips This Process.
- This module extracts AWS resources according to the default region configured in IAM.

#### SSO Login Method
- To overwrite steampipe config file, please enter the values in the format below.
- **DO NOT USE "-". ONLY "_" IS ALLOWED**
  ```
  connection "project_1 name" {
    plugin = "aws"
    profile = "project_1 profile name"
    regions = ["us-east-1"]
  }
  connection "project_2 name" {
    plugin = "aws"
    profile = "project_2 profile name"
    regions = ["us-east-1"]
  }
  ...
  ``` 
### [ 3 / 5 ] Extract AWS resources into an in-memory PostgreSQL.
- If all the above steps are completed successfully, extracting AWS resources into an in-memory PostgreSQL database will function properly.

  ![image](https://github.com/user-attachments/assets/15e94696-beb0-4c10-ad6e-9d9f3121d27b)

### [ 4 / 5 ] Select desired Mode.
- If you select Pre-processing or Raw-data mode, than go to step 5.
- If you select Steampipe Query, than conn to DB Session.

### [ 5 / 5 ] Extract an in-memory postgreSQL to structured inventory file.
- The inventory file(s) will be successfully created in the inventory volume.
