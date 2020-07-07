# Dockerfile to create a Mendix Docker image based on either the source code or
# Mendix Deployment Archive (aka mda file)
FROM ubuntu:bionic

#This version does a full build originating from the Ubuntu Docker images
LABEL Author="Think1st.App"
LABEL maintainer="my@think1st.app"

# When doing a full build: install dependencies & remove package lists
RUN apt-get -q -y update && \
 DEBIAN_FRONTEND=noninteractive apt-get upgrade -q -y && \
 DEBIAN_FRONTEND=noninteractive apt-get install -q -y wget curl libpq5 locales python3 python3-distutils libssl1.0.0 libgdiplus && \
 rm -rf /var/lib/apt/lists/* && \
 apt-get clean

# Set the locale to UTF-8 (needed for proper python3 functioning)
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Set the locale to UTF-8 (needed for proper python3 functioning)
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Copy content.
COPY scripts /opt/think1st

# Allow the root group to modify /etc/passwd so that the startup script can update the non-root uid
RUN chmod g=u /etc/passwd

# Add the runtime to pythonpath
ENV PYTHONPATH "$PYTHONPATH:/opt/think1st"

# Each comment corresponds to the script line:
# 1. Make the startup script executable
# 2. Update ownership of /opt/mendix so that the app can run as a non-root user
# 3. Update permissions of /opt/mendix so that the app can run as a non-root user
RUN chmod +rx /opt/think1st/startup &&\
    chgrp -R 0 /opt/think1st &&\
    chmod -R g=u /opt/think1st

WORKDIR /opt/think1st

USER 1001

ENV HOME "/opt/think1st"

# Expose nginx port
ENV PORT 8080
EXPOSE $PORT

ENTRYPOINT ["/opt/think1st/startup"]








