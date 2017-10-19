# Getting started

Devspace is a Continuous Integration tools managed by Jenkins CI providing
an automation framework that runs repeated jobs. The default deployment
initializes a Jenkins CI master with a predefined set of jobs.


Running and maintaining Devspace requires brief understanding of:

*  [Docker engine](https://docs.docker.com/)
*  [Docker compose](https://docs.docker.com/compose/)

Running and maintaining Devspace in OpenStack requires brief understanding of:

* [Docker engine](https://docs.docker.com/)
* [Docker compose](https://docs.docker.com/compose/)
* [ansible](http://docs.ansible.com/ansible/intro_getting_started.html)
    *  [inventory](http://docs.ansible.com/ansible/intro_inventory.html)
    *  [playbook](http://docs.ansible.com/ansible/playbooks.html)
*  access to openstack tenancy
*  own ssh key set in openstack tenancy, that name will be used as `vm_key_name`
*  [openrc.sh](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html)
*  snoopy ssh key, see [internal]()
*  gitconfig see [internal]()


## Installation

#### Manual

The following instructions explain how to deploy a devspace on a Docker host.

*   Install the prerequisites [Docker engine](https://docs.docker.com/) and
    [Docker compose](https://docs.docker.com/compose/) either globally or in
    a virtual environment:

        $ pip install docker-compose

*   Clone the ``devspace`` repository

        $ git clone https://github.com/openmicroscopy/devspace.git
        $ cd devspace

*   Generated self-signed SSL certificates for the Jenkins and Nginx
    containers:

        $ ./sslcert jenkins/sslcert HOST_IP
        $ ./sslcert nginx/sslcert HOST_IP

    alternatively put your own certificate `.crt and .key` in the above locations

*   Copy the SSH and Git configuration files used for fetching and pushing the
    Git repositories under `slave/.ssh` and `slave/.gitconfig`.

 *  Run `rename.py` to match your topic name. If you do not yet have
    topic branches available on origin, use "develop" or one of the
    main branches:

        $ ./rename.py MYTOPIC

*   Replace the USER_ID of the various Dockerfile with the ID of the user who
    will run the devspace:

        $ find . -iname Dockerfile -type f -exec sed -i -e 's/1000/<USER_ID>/g' {} \;

*   Set the environment variables in `.env`:

        USER_ID=<USER_ID>
        JENKINS_USERNAME=devspace
        JENKINS_PASSWORD=<password>

*   Optionally, commit all the deployment changes above on the local clone of the devspace repository.

Start and configure:

*   Start devspace using `docker-compose`:

        $ docker-compose up -d

    By default, this will use the name of the directory as the project name. In the case of a shared Docker host, it is possible to override the project name using th

        $ docker-compose up -p my_project -d

*   Retrieve the dynamic port of the Jenkins NGINX container. You can access
    the Jenkins UI from https://HOST_IP:PORT after accepting the self-signed
    certificate:

        $ docker-compose -p my_project port nginxjenkins 443

*   [Optional] Turn on Basic HTTP authentication for Jenkins

        sudo htpasswd -c jenkins/conf.d/passwdfile nginx 

    and update `jenkins/conf.d/jenkins.conf`:

        auth_basic "Restricted";
        auth_basic_user_file /etc/nginx/conf.d/passwdfile;


#### OpenStack

For that section, you will need to have an account on [OpenStack](https://pony.openmicroscopy.org).
Please use the sysadmin slack channel to request an account.

Generate an ``openrc``file:

* Log into [OpenStack](https://pony.openmicroscopy.org)
* Create a [OpenStack RC file](https://docs.openstack.org/zh_CN/user-guide/common/cli-set-environment-variables-using-openstack-rc.html)
* Download the OpenStack RC File v2, the file should be named ``omedev-openrc.sh``

Clone the ``infrastructure`` repository:

    $ git clone https://github.com/openmicroscopy/infrastructure.git

Set up a directory ``snoopy``:

    $ tree /path/to/snoopy
    snoopy
        ├── .gitconfig
        └── .ssh

Add the ssh keys to `snoopy/.ssh`, to obtain ssh key and token for snoopy, please go to [internal]():

        -rwx------.  1    74 Sep 13 15:25 config
        -rwx------.  1  1674 Sep 13 15:25 snoopycrimecop_github
        -rwx------.  1   405 Sep 13 15:25 snoopycrimecop_github.pub

Add variables to ``path/to/inventory/group_vars/devspace``:

        devspace_omero_branch: develop
        snoopy_dir_path: "/path/to/snoopy"

 To use a specific repository or branch of devspace:
        devspace_git_repo: "https://github.com/user_name/devspace.git"
        devspace_git_version: "your_branch"

    NOTE:

    **devspace_omero_branch** is the name of the git branch all the jobs will be using. By default it is using `https://github.com/openmicroscopy/openmicroscopy/tree/develop`.
    **devspace_git_repo** indicates the devspace repository to use. If you do not need to use a specific repository, `https://github.com/openmicroscopy/devspace.git` is used
    **devspace_git_version** indicates the branch or tag to use. By default it is `https://github.com/openmicroscopy/devspace/tree/master`.
    See `https://github.com/openmicroscopy/ansible-role-devspace` for a full list of supported parameters.

Create a virtual environment and install the dependencies:

    $ virtualenv dev
    $ . dev/bin/activate
    (dev) $ pip install -r infrastructure/requirements.txt
    Source the OpenStack RC File, Adjust to your local configuration
    (dev) $ . omedev-openrc.sh
    Enter your password



    NOTE: 

    VM will boot from volume, you no longer have to attach additional volumes. The size of the volume can be set by `-e vm_size=100`


Install the various ansible roles and run the playbook:

    (dev) $ cd infrastructure/ansible
    (dev) $ ansible-galaxy install -r requirements.yml
    Run the playbook to create and provision the devpace
    (dev) $ ansible-playbook os-devspace.yml -e vm_name=devspace-test -e vm_key_name=your_key
    (dev) $ ansible-playbook -l devspace-test -u centos devspace.yml


Devspace should be already started at https://your_host:8443.

## ADVANCE: Multiply containers

 * List of devspace containers can be controlled by custom runtime handler in `devspace_handler_tasks`.
   For more complex deployment see [devspace-runtime.yml](https://github.com/openmicroscopy/ansible-role-devspace/blob/master/tasks/devspace-runtime.yml) that uses [docker service module](https://docs.ansible.com/ansible/docker_service_module.html).

 * [common-services-v1.yml](common-services-v1.yml) contains a default list of basic containers that are suitable to extend:
    You can extend any service together with other configuration keys. For more details
    read [extends](https://docs.docker.com/v1.6/compose/extends/).

 * to override the basic containers keep in mind compose copies configurations from the
   original service over to the local one, except for links and volumes_from.

   Examples of how to extend existing containers.

    - baseomero: basic container starting OMERO.server process

            myomero:
                extends:
                    file: common-services-v1.yml
                    service: baseserver
                links:
                    - jenkins
                    - pg
                volumes:
                    - ./myservices/omero:/home/omero
                environment:
                    - SLAVE_NAME=myomero
                ports:
                    - "24064:24064"
                    - "24063:24063"

    - baseweb: basic container starting OMERO.web process

            myweb:
                extends:
                    file: common-services-v1.yml
                    service: baseweb
                links:
                    - jenkins
                    - redis
                    - myomero
                volumes:
                    - ./myservices/web:/home/omero
                    - ./myservices/nginx/conf.d:/home/omero/nginx
                environment:
                    - SLAVE_NAME=myweb

    - basenginx: basic container starting nginx process

            mynginx:
                extends:
                    file: common-services-v1.yml
                    service: basenginx
                links:
                    - jenkins
                    - myweb
                volumes:
                    - ./myservices/nginx/conf.d:/etc/nginx/conf.d
                    - ./myservices/web/static:/home/omero/static
                environment:
                    - SLAVE_NAME=mynginx
                ports:
                    - "8080:80"

    NOTE:

    **You have to create manually all new volume directories to avoid 
    permission issues. Copy from appropriate existing jobs and point to the new node.**


## Job workflow


The default deployment initializes a Jenkins server with a [predefined set of
jobs](homes/jobs). The table below lists the job names, the Jenkins node labels
they are associated with and a short description of the job:

| Job name               | Name            | Description                               |
| -----------------------|-----------------| ------------------------------------------|
| Trigger                |                 | Runs all the following jobs in order      |
| BIOFORMATS-push        | testintegration | Merges all Bio-Formats PRs                |
| BIOFORMATS-ant         | testintegration | Builds Bio-Formats and runs unit tests    |
| BIOFORMATS-maven       | testintegration | Builds Bio-Formats and runs unit tests    |
| OMERO-push             | testintegration | Merges all OMERO PRs                      |
| OMERO-build            | testintegration | Builds OMERO artifacts (server, clients)  |
| OMERO-server           | omero           | Deploys an OMERO.server                   |
| OMERO-web              | web             | Deploys an OMERO.web client               |
| OMERO-test-integration | testintegration | Runs the OMERO integration tests          |
| OMERO-robot            | testintegration | Runs the Robot tests                      |
| nginx                  | nginx           | Reloads the nginx server                  |
| OMERO-docs             | testintegration | Builds the OMERO documentation            |


Default packages:

| Name       | Version       | Optional                           |
| -----------|---------------| -----------------------------------|
| Java       | openJDK 1.8   | openJDK 1.8 devel, oracleJDK 1.8   |
| Python     | 2.7           | -                                  |
| Ice        | 3.6           | 3.5                                |
| PostgreSQL | latest        | https://hub.docker.com/_/postgres/ |
| Nginx      | 1.8           | -                                  |
| Redis      | latest        | https://hub.docker.com/_/redis/    |


## Customization:

* Updating omero-install scripts:

In order to install additional components it is required to first adjust update files in [omero-install](https://github.com/ome/omero-install).
Then fetch custom omero-install branch by updating each Dockerfile

    ├── nginx
    │   ├── Dockerfile
    ├── server
    │   ├── Dockerfile
    ├── slave
    │   ├── Dockerfile
    └── web
        ├── Dockerfile


    ## update omero-install to use custom fork
    RUN git --git-dir=$OMERO_INSTALL_ROOT/.git --work-tree=$OMERO_INSTALL_ROOT config --global user.email "you@example.com"
    RUN git --git-dir=$OMERO_INSTALL_ROOT/.git --work-tree=$OMERO_INSTALL_ROOT config --global user.name "Your Name"
    RUN git --git-dir=$OMERO_INSTALL_ROOT/.git --work-tree=$OMERO_INSTALL_ROOT remote add username https://github.com/username/omero-install.git
    RUN git --git-dir=$OMERO_INSTALL_ROOT/.git --work-tree=$OMERO_INSTALL_ROOT fetch username
    RUN git --git-dir=$OMERO_INSTALL_ROOT/.git --work-tree=$OMERO_INSTALL_ROOT merge username/yourbranch

## Limitations:

* Robot job is still under investigation as it fails due to webbrowser crash. Robot job requires manual changes of the domain. Make sure webhost is set to the correct VM IP e.g.

        --webhost "10.0.50.100"


## Upgrade

 *  Upgrade to 0.3.0:

    - Devspace should be run in VM.
    - Services are managed by ansible playbook run with inline v1 compose

    - It is possible to extend services using ansible playbook. If you already created new containers based on existing Dockerfiles, you may wish to review your customization and extend common services

 *  Upgrade to 0.2.0:

    If you made custom adjustments to the code and committed them, it is recommended to reset changes.

    Here are listed the most important changes:

     * Compose configuration was split into a few different files depending on the platform

            - docker-compose.yml main file
            - docker-compose.unixports.yml required for running container on UNIX platform
            - docker-compose.osx.yml required for running containers on OSX platform

       For how to run check deployment

     * All nodes are now systemd nodes that require adjusting the permissions. For what to change
       see deployment.

            - **Do not change Dockerfile** as this will load your USERID automatically
              If you did it in the past remove the change.

            - slave node:
              Since slave container user has changed from slave to omero.
              If you want to preserve the history, once you start your new devspace, you have to
              manually chown all files that belongs to slave user.

              `find . -user slave -group slave -exec chown omero:omero`
              `find . -user slave -group 8000 -exec chown omero:8000`
              `usermod -u 1234 omero`

     *  Run `rename.py` to match your topic name. If you do not yet have
        topic branches available on origin, use "develop" or one of the
        main branches.

            ./rename.py MYTOPIC
 
        Ignore the error

