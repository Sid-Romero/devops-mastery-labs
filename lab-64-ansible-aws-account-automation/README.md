# Lab 64: Ansible: Automating AWS Account Creation (Simplified)

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-18

## Description

This lab simulates automating AWS account creation using Ansible. It focuses on creating IAM users and groups with specific permissions, mimicking the initial steps of account setup before infrastructure deployment.

## Learning Objectives

- Learn how to create Ansible playbooks for AWS automation.
- Understand how to use the `iam_user` and `iam_group` Ansible modules.
- Learn to define and apply IAM policies using Ansible.
- Practice using Ansible Vault for storing sensitive AWS credentials.

## Prerequisites

- Ansible installed and configured on your local machine.
- AWS CLI installed and configured with credentials that have permissions to create IAM users and groups.
- Python 3.6 or higher installed.
- boto3 and botocore python packages installed (`pip install boto3 botocore`)
- Ansible AWS modules installed (`ansible-galaxy collection install amazon.aws`)
- Basic understanding of AWS IAM concepts.

## Lab Steps

### Step 1: Set up the Ansible Project Directory

Create a directory for your Ansible project. Inside the directory, create the following structure:

```
mkdir ansible-aws-iam
cd ansible-aws-iam
mkdir roles
mkdir inventories
touch ansible.cfg
```

Create an `inventories/hosts` file with the following content (replace `localhost` with your Ansible control node if it's not the local machine):

```
[local]
localhost ansible_connection=local
```

Create an `ansible.cfg` file. This file configures Ansible. Add the following to it:

```ini
[defaults]
inventory = inventories/hosts
roles_path = roles
```

### Step 2: Create the IAM User Role

Create a role to handle IAM user creation. Inside the `roles` directory, create a directory named `iam_user` and then create the necessary subdirectories and files:

```
mkdir -p roles/iam_user/tasks
mkdir roles/iam_user/vars
touch roles/iam_user/tasks/main.yml
touch roles/iam_user/vars/main.yml
```

In `roles/iam_user/vars/main.yml`, define the user details:

```yaml
username: 'testuser'
state: 'present'
```

In `roles/iam_user/tasks/main.yml`, add the task to create the IAM user:

```yaml
- name: Create IAM user
  iam_user:
    name: "{{ username }}"
    state: "{{ state }}"
  register: iam_user_result

- name: Print IAM user details
  debug:
    msg: "IAM user {{ username }} created with ID {{ iam_user_result.user.user_id }}"
  when: iam_user_result.changed
```

### Step 3: Create the IAM Group Role

Create a role to handle IAM group creation. Inside the `roles` directory, create a directory named `iam_group` and then create the necessary subdirectories and files:

```
mkdir -p roles/iam_group/tasks
mkdir roles/iam_group/vars
touch roles/iam_group/tasks/main.yml
touch roles/iam_group/vars/main.yml
```

In `roles/iam_group/vars/main.yml`, define the group details:

```yaml
group_name: 'developers'
state: 'present'
users: ['testuser'] # the IAM user we created previously
```

In `roles/iam_group/tasks/main.yml`, add the task to create the IAM group and add the user to it:

```yaml
- name: Create IAM group
  iam_group:
    name: "{{ group_name }}"
    state: "{{ state }}"
  register: iam_group_result

- name: Add user to group
  iam_group:
    name: "{{ group_name }}"
    users: "{{ users }}"
    state: "{{ state }}"
  when: iam_group_result.changed
```

### Step 4: Create the Playbook

Create a playbook named `main.yml` in the root directory of your Ansible project:

```yaml
---
- hosts: local
  gather_facts: false
  roles:
    - iam_user
    - iam_group
```

### Step 5: Run the Playbook

Execute the playbook using the following command:

```bash
ansible-playbook main.yml
```

Verify that the IAM user and group are created in the AWS console.

### Step 6: Add an IAM Policy to the Group

Modify the `iam_group` role to attach a policy to the group.  First, define the policy document in `roles/iam_group/vars/main.yml`.  For example, to allow read-only access to S3:

```yaml
group_name: 'developers'
state: 'present'
users: ['testuser']
policy_name: 'ReadOnlyS3'
policy_document:
  Version: '2012-10-17'
  Statement:
    - Effect: 'Allow'
      Action: 's3:Get*'
      Resource: '*'
```

Then, add a task to attach the policy in `roles/iam_group/tasks/main.yml`:

```yaml
- name: Create IAM group
  iam_group:
    name: "{{ group_name }}"
    state: "{{ state }}"
  register: iam_group_result

- name: Add user to group
  iam_group:
    name: "{{ group_name }}"
    users: "{{ users }}"
    state: "{{ state }}"
  when: iam_group_result.changed

- name: Add policy to group
  iam_policy:
    iam_type: group
    iam_name: "{{ group_name }}"
    name: "{{ policy_name }}"
    policy: "{{ policy_document }}"
    state: present
```

Run the playbook again to apply the policy.

### Step 7: Using Ansible Vault for Credentials

Instead of hardcoding AWS credentials in your Ansible configuration, it's best practice to use Ansible Vault.  First, create a vault file (e.g., `vault.yml`) and encrypt it:

```bash
ansible-vault create vault.yml
```

Ansible Vault will prompt you for a password.  Inside `vault.yml`, you can store your AWS access key and secret key:

```yaml
aws_access_key: 'YOUR_AWS_ACCESS_KEY'
aws_secret_key: 'YOUR_AWS_SECRET_KEY'
```

Then, in your playbook or roles, you can reference these variables. You'll need to pass the `--ask-vault-pass` flag when running the playbook, or provide a vault password file.

To use the variables, first include the vault variables in the playbook:

```yaml
---
- hosts: local
  gather_facts: false
  vars_files:
    - vault.yml
  roles:
    - iam_user
    - iam_group
```

Modify the `iam_user` role to use the vault variables for authentication. You'll need to add `aws_access_key` and `aws_secret_key` to the `iam_user` task in `roles/iam_user/tasks/main.yml`:

```yaml
- name: Create IAM user
  iam_user:
    name: "{{ username }}"
    state: "{{ state }}"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  register: iam_user_result

- name: Print IAM user details
  debug:
    msg: "IAM user {{ username }} created with ID {{ iam_user_result.user.user_id }}"
  when: iam_user_result.changed
```

Run the playbook with the vault password prompt:

```bash
ansible-playbook main.yml --ask-vault-pass
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your AWS credentials have the necessary permissions to create IAM users and groups.
2. Double-check the spelling of module names and parameters in your playbooks.
3. Use `ansible-lint` to check your playbook for syntax errors.
4. Remember to install the required Python packages (`boto3`, `botocore`) if you encounter errors related to AWS modules.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The complete solution involves creating Ansible playbooks and roles that define the desired state of IAM users and groups.  The playbooks use the `iam_user` and `iam_group` modules to create, modify, and delete IAM resources.  Ansible Vault is used to securely store AWS credentials.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
- **Technology:** Ansible

##  Cleanup

Don't forget to clean up resources after completing the lab:

```bash
# Example cleanup commands (adjust based on lab content)
docker system prune -f
# or
kubectl delete -f .
# or
helm uninstall <release-name>
```

---

*This lab was auto-generated by the [Lab Generator Bot](../.github/workflows/generate-lab.yml)*
