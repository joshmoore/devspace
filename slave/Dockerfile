FROM openmicroscopy/omero-build-c6-multienv

MAINTAINER OME

ENV JENKINS_SWARM_VERSION 1.24
ENV HOME /home/jenkins-slave

RUN useradd -c "Jenkins Slave user" -d $HOME -m jenkins-slave
RUN usermod -u SPACEUSER jenkins-slave
RUN curl --create-dirs -sSLo /usr/share/jenkins/swarm-client-$JENKINS_SWARM_VERSION-jar-with-dependencies.jar http://maven.jenkins-ci.org/content/repositories/releases/org/jenkins-ci/plugins/swarm-client/$JENKINS_SWARM_VERSION/swarm-client-$JENKINS_SWARM_VERSION-jar-with-dependencies.jar \
  && chmod 755 /usr/share/jenkins

COPY jenkins-slave.sh /usr/local/bin/jenkins-slave.sh
RUN chmod a+x /usr/local/bin/jenkins-slave.sh

USER jenkins-slave

ENTRYPOINT ["/usr/local/bin/jenkins-slave.sh"]
