# Lab 33: Automating Scam Prevention with Ansible Playbooks

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-31

## Description

This lab simulates using Ansible to automate tasks related to scam prevention, inspired by the Meta article.  You will create playbooks to identify potentially malicious user accounts based on predefined criteria and apply mitigation actions.

## Learning Objectives

- Learn how to create and execute Ansible playbooks.
- Understand how to use Ansible modules for system administration tasks.
- Learn how to use Ansible variables and conditional statements to automate tasks based on specific criteria.
- Simulate automated response to potential scam accounts.

## Prerequisites

- Ansible installed and configured on your local machine.
- A virtual machine or remote server to target with Ansible (can be a local VM using Vagrant or VirtualBox).
- Basic understanding of YAML syntax.

## Lab Steps

### Step 1: Set up the Inventory

Create an Ansible inventory file named `inventory.ini`. This file will contain the details of the target host(s) where the playbook will be executed. Replace `your_target_host` with the IP address or hostname of your target machine. If you are using SSH keys for authentication, ensure they are configured correctly.

```ini
[targets]
your_target_host ansible_user=your_user ansible_ssh_private_key_file=~/.ssh/id_rsa

[targets:vars]
ansible_connection=ssh
ansible_python_interpreter=/usr/bin/python3 #or the correct path
```

Replace `your_user` with the appropriate username on the target host.  Adjust the `ansible_python_interpreter` to match the Python version on your target machine if necessary. Test connectivity with `ansible -i inventory.ini all -m ping`.

### Step 2: Create the Scam Detection Playbook

Create a file named `scam_detection.yml`. This playbook will simulate identifying potential scam accounts based on certain criteria (e.g., suspicious usernames, recent account creation, multiple posts with similar content). For simplicity, we'll focus on checking for usernames containing specific keywords.

```yaml
---
- name: Detect Potential Scam Accounts
  hosts: targets
  become: true
  vars:
    suspicious_keywords:
      - 'scam'
      - 'fraud'
      - 'promotion'
    log_file: /var/log/scam_detection.log

  tasks:
    - name: Check for Suspicious Usernames
      command: 'getent passwd | cut -d: -f1'
      register: user_list

    - name: Identify Suspicious Users
      debug:
        msg: "Potential scam account found: {{ item }}"
      loop: "{{ user_list.stdout_lines }}"
      when: item is search('{{ suspicious_keywords | join("|") }}')

    - name: Log Suspicious Activity
      lineinfile:
        path: "{{ log_file }}"
        line: "Suspicious account found: {{ item }}"
        create: yes
      loop: "{{ user_list.stdout_lines }}"
      when: item is search('{{ suspicious_keywords | join("|") }}')

    - name: Simulate Account Deactivation (Optional)
      user:
        name: "{{ item }}"
        state: absent
        remove: yes
      loop: "{{ user_list.stdout_lines }}"
      when: item is search('{{ suspicious_keywords | join("|") }}')
      ignore_errors: yes #Allow the playbook to continue if the user doesn't exist
```

This playbook does the following:

1.  Retrieves a list of all users on the target system using `getent passwd`.
2.  Identifies users whose usernames contain any of the keywords defined in `suspicious_keywords`.
3.  Logs the suspicious activity to a log file.
4.  (Optional) Simulates account deactivation for the identified users.

Note:  The account deactivation is optional and should be performed with caution in a real-world scenario. The `ignore_errors: yes` directive prevents the playbook from failing if a user does not exist.

### Step 3: Execute the Playbook

Run the playbook using the following command:

```bash
ansible-playbook -i inventory.ini scam_detection.yml
```

Review the output to see which users were flagged as potentially suspicious and if the logging and account deactivation tasks were executed successfully.  Check the contents of the `log_file` on the target machine to confirm that the suspicious activity was logged.

```bash
ssh your_target_host 'cat /var/log/scam_detection.log'
```

### Step 4: Enhance the Playbook (Optional)

You can enhance the playbook by adding more sophisticated detection criteria, such as checking for recent account creation dates, analyzing user activity patterns, or integrating with external threat intelligence feeds. You can also implement more robust mitigation actions, such as blocking the user's IP address, disabling certain features, or escalating the issue to a security team.

Consider adding these features to the playbook:

*   **Account Creation Date Check:** Use the `stat` module to retrieve the account creation date and flag accounts created within a specific timeframe.
*   **User Activity Analysis:** Simulate checking for suspicious activity by creating dummy files and modifying the playbook to detect changes to those files.
*   **Integration with External APIs:** Use the `uri` module to query external APIs for threat intelligence data and flag users based on the API's response.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure SSH keys are correctly configured for passwordless authentication.
2. Double-check the syntax of your YAML file. Indentation is crucial.
3. Use `ansible-lint` to validate your playbook for best practices.
4. If the playbook fails, examine the output carefully for error messages. Common issues include incorrect user permissions or missing dependencies on the target host.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating an Ansible playbook that retrieves user information, checks for suspicious usernames based on predefined keywords, logs the activity, and optionally deactivates the accounts. The inventory file needs to be configured correctly to target the remote host. Error handling using `ignore_errors` is included to prevent playbook failure. Further enhancements can be added to implement more sophisticated detection and mitigation strategies.

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
