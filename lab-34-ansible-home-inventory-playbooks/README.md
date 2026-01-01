# Lab 34: Ansible: Home Inventory with Playbooks

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-01

## Description

This lab introduces Ansible playbooks for managing a home inventory system, inspired by HomeBox. You'll learn to automate the creation of directories, files, and the installation of a basic web server to serve inventory data.

## Learning Objectives

- Understand the basic structure of an Ansible playbook.
- Learn how to use Ansible modules to manage files and directories.
- Practice installing and configuring software (nginx) using Ansible.
- Implement basic templating in Ansible to create dynamic configuration files.

## Prerequisites

- Ansible installed and configured on your local machine.
- Virtual machine or server to act as the target host (can be localhost if Ansible is configured for it).
- Basic knowledge of YAML syntax.

## Lab Steps

### Step 1: Set up the Ansible Inventory

First, create an Ansible inventory file that defines your target host. This file tells Ansible where to execute the playbook. Create a file named `inventory` and add your target host. If you're using localhost, it would look like this:

```
localhost ansible_connection=local
```

If you are using a remote server, replace `localhost` with the server's IP address or hostname.  You may need to configure SSH access to the remote server and provide Ansible with the appropriate credentials in the inventory file or via command line arguments. For example:

```
[webservers]
web1 ansible_host=your_server_ip ansible_user=your_user ansible_ssh_private_key_file=~/.ssh/id_rsa
```

Ensure your Ansible configuration is properly set up to connect to the target host.

### Step 2: Create the Home Inventory Directory Structure

Next, create a playbook that sets up the basic directory structure for your home inventory. Create a file named `home_inventory.yml` with the following content:

```yaml
---
- name: Create Home Inventory Directory Structure
  hosts: all
  become: true
  tasks:
    - name: Create base directory
      file:
        path: /opt/home_inventory
        state: directory
        mode: '0755'
        owner: root
        group: root

    - name: Create subdirectories for documents, images, and data
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
        owner: root
        group: root
      loop:
        - /opt/home_inventory/documents
        - /opt/home_inventory/images
        - /opt/home_inventory/data
```

This playbook creates a base directory `/opt/home_inventory` and subdirectories for documents, images, and data.  The `become: true` directive tells Ansible to execute the tasks with elevated privileges (sudo). The `file` module is used to manage files and directories.  The `loop` directive iterates over the list of subdirectories to create them all with the same attributes.

### Step 3: Install and Configure Nginx

Now, let's expand the playbook to install Nginx and configure it to serve a simple index page from the inventory directory. Add the following tasks to `home_inventory.yml` after the directory creation tasks:

```yaml
    - name: Install Nginx
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian" # Only run on Debian-based systems

    - name: Install Nginx (RedHat)
      yum:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat" # Only run on RedHat-based systems

    - name: Create simple index.html
      copy:
        dest: /opt/home_inventory/index.html
        content: |
          <html>
          <head><title>Home Inventory</title></head>
          <body><h1>Welcome to your Home Inventory!</h1></body>
          </html>

    - name: Configure Nginx to serve the inventory directory
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/home_inventory

    - name: Enable the site
      file:
        src: /etc/nginx/sites-available/home_inventory
        dest: /etc/nginx/sites-enabled/home_inventory
        state: link
      notify: Reload Nginx

  handlers:
    - name: Reload Nginx
      service:
        name: nginx
        state: reloaded
```

This adds tasks to install Nginx using the `apt` or `yum` module based on the operating system family. It also creates a simple `index.html` file and configures Nginx to serve the `/opt/home_inventory` directory. The `template` module is used to create the Nginx configuration file from a Jinja2 template. The `notify` directive tells Ansible to run the `Reload Nginx` handler when the configuration file changes. Create a file named `nginx.conf.j2` with the following content:

```nginx
server {
    listen 80;
    server_name localhost;
    root /opt/home_inventory;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

This template defines a basic Nginx configuration that listens on port 80 and serves files from the `/opt/home_inventory` directory.

### Step 4: Run the Playbook

Execute the playbook using the following command:

```bash
ansible-playbook -i inventory home_inventory.yml
```

This command tells Ansible to run the `home_inventory.yml` playbook using the `inventory` file to determine the target host.  Monitor the output for any errors. If the playbook runs successfully, Nginx should be installed and configured, and you should be able to access the `index.html` page in your browser by navigating to the target host's IP address or hostname.

### Step 5: Verify the Installation

Open a web browser and navigate to the IP address or hostname of your target server. You should see the 'Welcome to your Home Inventory!' message. Verify that the directory structure has been created on the target server in `/opt/home_inventory`.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure your Ansible inventory is correctly configured with the target host's IP address or hostname.
2. Double-check the paths in the playbook to make sure they match your desired directory structure.
3. If Nginx fails to start, check the Nginx error logs for clues.
4. Verify that the target host has internet access if you are installing Nginx from a package repository.
5. The `apt` and `yum` modules are distribution-specific. Ensure you are using the correct module for your target OS.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The complete solution involves creating a playbook that uses the `file` module to create directories, the `apt` or `yum` module to install Nginx, the `copy` module to create a simple index page, and the `template` module to configure Nginx. The Nginx configuration file serves the inventory directory. The playbook is then executed using `ansible-playbook`.

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
