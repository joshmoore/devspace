FROM jenkins
MAINTAINER OME

USER root
RUN usermod -u SPACEUSER jenkins
RUN chown -R jenkins /usr/share/jenkins/
USER jenkins

COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN /usr/local/bin/plugins.sh /usr/share/jenkins/plugins.txt
