# Lab 36: Ansible: Home Inventory Management with YAML

![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-brightgreen) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-01

## Description

This lab introduces Ansible for managing a simple home inventory. You'll learn to create and manage inventory files in YAML format, define variables, and use Ansible playbooks to perform basic tasks on your simulated home devices.

## Learning Objectives

- Understand the structure of an Ansible inventory file in YAML format.
- Define host variables and group variables in Ansible inventories.
- Write and execute a basic Ansible playbook to interact with managed hosts.
- Apply variable precedence rules in Ansible.

## Prerequisites

- Ansible installed on your local machine (e.g., via pip install ansible)
- Python 3 installed
- Basic understanding of YAML syntax
- Virtual environment (optional, but recommended)

## Lab Steps

### Step 1: Set up the Environment

1.  Create a directory for this lab:

    ```bash
    mkdir ansible-home-inventory
    cd ansible-home-inventory
    ```

2.  (Optional) Create and activate a Python virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Create a `hosts.yml` file. This will be your Ansible inventory file.

    ```bash
    touch hosts.yml
    ```

4.  Create a playbook file named `home.yml`

    ```bash
    touch home.yml
    ```

### Step 2: Define the Inventory

Edit the `hosts.yml` file to define your home inventory.  Assume you have a smart TV, a Raspberry Pi server, and a smart lightbulb.

```yaml
all:
  hosts:
    smarttv:
      ansible_host: 192.168.1.10
      device_type: smart_tv
    raspberrypi:
      ansible_host: 192.168.1.20
      device_type: server
    smartbulb:
      ansible_host: 192.168.1.30
      device_type: lightbulb
  vars:
    ansible_user: your_username
    ansible_ssh_pass: your_password  #WARNING: Not recommended for production. Use SSH keys.
    location: living_room

smart_devices:
  hosts:
    smarttv:
    smartbulb:
  vars:
    power_source: mains
```

Replace `your_username` and `your_password` with appropriate values for your *simulated* devices.  **Do not use real credentials.** This example uses passwords for simplicity, but SSH keys are strongly recommended for real-world scenarios.

**Explanation:**

*   `all`:  The top-level group containing all hosts.
*   `hosts`:  A list of individual hosts.
*   `ansible_host`:  The IP address or hostname of the managed host.  These are example IPs, don't use real IPs unless you are configuring real devices.
*   `device_type`:  A custom variable defining the type of device.
*   `vars`:  Variables that apply to the group or host.
*   `ansible_user`:  The username to use for SSH connections.
*   `ansible_ssh_pass`:  The password to use for SSH connections (again, for demonstration purposes only).
*   `smart_devices`: A group containing only smart devices.
*   `power_source`: A variable specific to smart devices.

### Step 3: Create a Simple Playbook

Edit the `home.yml` file to create a simple Ansible playbook to gather facts from the hosts and print some variables.

```yaml
---
- name: Gather facts and display variables
  hosts: all
  gather_facts: yes

  tasks:
    - name: Display hostname
      debug:
        msg: "Hostname: {{ ansible_hostname }}"

    - name: Display device type
      debug:
        msg: "Device Type: {{ device_type }}"

    - name: Display location
      debug:
        msg: "Location: {{ location }}"

    - name: Display power source (if applicable)
      debug:
        msg: "Power Source: {{ power_source | default('Not applicable') }}"
```

**Explanation:**

*   `name`:  A description of the playbook.
*   `hosts`:  The group of hosts to target (in this case, all hosts).
*   `gather_facts`:  Instructs Ansible to gather facts about the managed hosts.
*   `tasks`:  A list of tasks to execute.
*   `debug`:  A module that prints a message.
*   `msg`:  The message to print, using Jinja2 templating to access variables.
* `power_source | default('Not applicable')`:  Uses the `default` filter to provide a default value if the `power_source` variable is not defined for a host.

### Step 4: Run the Playbook

Run the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i hosts.yml home.yml --ask-pass
```

You will be prompted for the SSH password (since we are using `--ask-pass`).  If you have SSH keys configured, you can omit the `--ask-pass` option.

Observe the output.  You should see the hostname, device type, location, and power source (if applicable) printed for each host.

**Troubleshooting:**

*   If you encounter connection errors, ensure that the `ansible_host`, `ansible_user`, and `ansible_ssh_pass` variables are correctly configured.
*   Check the YAML syntax in your `hosts.yml` and `home.yml` files.  YAML is sensitive to indentation.
*   If you are not prompted for the password, and you get a 'Permission denied' error, then you need to verify the ansible user and password.

### Step 5: Experiment with Variable Precedence

Modify the `hosts.yml` file to define a `location` variable specifically for the `smarttv` host:

```yaml
all:
  hosts:
    smarttv:
      ansible_host: 192.168.1.10
      device_type: smart_tv
      location: bedroom  # Override the global location
    raspberrypi:
      ansible_host: 192.168.1.20
      device_type: server
    smartbulb:
      ansible_host: 192.168.1.30
      device_type: lightbulb
  vars:
    ansible_user: your_username
    ansible_ssh_pass: your_password  #WARNING: Not recommended for production. Use SSH keys.
    location: living_room

smart_devices:
  hosts:
    smarttv:
    smartbulb:
  vars:
    power_source: mains
```

Run the playbook again:

```bash
ansible-playbook -i hosts.yml home.yml --ask-pass
```

Observe that the `location` variable for `smarttv` is now "bedroom", demonstrating that host variables take precedence over group variables. This is an important concept in Ansible variable precedence rules.


<details>
<summary> Hints (click to expand)</summary>

1. Double-check the indentation in your YAML files.  Incorrect indentation is a common cause of errors.
2. Ensure that the IP addresses in your `hosts.yml` file are valid.  If you don't have real devices, use example private IP ranges.
3. Use SSH keys instead of passwords for connecting to your managed hosts in a production environment.
4. If the playbook fails, check the Ansible output for error messages.  Pay close attention to the line numbers in the error messages.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a YAML inventory file (`hosts.yml`) defining the managed hosts and their variables. A playbook (`home.yml`) is then created to gather facts and display the defined variables, demonstrating how Ansible can be used to manage and configure devices in a home environment. Variable precedence is shown by overriding a group variable with a host-specific variable.

</details>


---

## Notes

- **Difficulty:** Easy
- **Estimated time:** 30-45 minutes
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
