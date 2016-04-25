FROM jenkins:1.642.4
MAINTAINER OME

# Temp fix robot test results
ENV JAVA_OPTS "-Dhudson.model.DirectoryBrowserSupport.CSP="

COPY prefetched/ /tmp/
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
COPY curl /tmp/
RUN env PATH=/tmp:$PATH /usr/local/bin/plugins.sh /usr/share/jenkins/ref/plugins.txt
