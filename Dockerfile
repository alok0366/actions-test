FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends --yes ca-certificates curl gnupg && \
    echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_11/ /" > /etc/apt/sources.list.d/kubic.list && \
    curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_11/Release.key" | apt-key add - && \
    apt-get update && \
    apt-get install --yes podman && \
    apt-get install --yes python3-jinja2 python3-requests python3-yaml python3-ruamel.yaml linux-image-amd64 && \
    rm /usr/sbin/iptables && \
    ln -s /usr/sbin/iptables-legacy /usr/sbin/iptables && \
    apt-get purge --yes gnupg && \
    apt-get autoremove --purge --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY share/pind/containers.conf /etc/containers/containers.conf

RUN apt-get update && \
    apt-get install --yes podman jq && \
    apt-get install --yes python3-jinja2 python3-requests python3-yaml python3-ruamel.yaml linux-image-amd64 python3-pip git xz-utils wget && \
    rm /usr/sbin/iptables && \
    ln -s /usr/sbin/iptables-legacy /usr/sbin/iptables && \
    apt-get purge --yes gnupg && \
    apt-get autoremove --purge --yes && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install git+https://gitlab.com/Linaro/tuxsuite

RUN pip3 install tuxrun

RUN pip3 install --force-reinstall git+https://gitlab.com/Linaro/tuxmake

RUN wget -O ccache.tar.xz https://github.com/ccache/ccache/releases/download/v4.9.1/ccache-4.9.1-linux-x86_64.tar.xz && tar -xf ccache.tar.xz && cd ccache* && make install

COPY generate_pipeline.py /usr/bin/generate_pipeline

COPY update_plan.py /usr/bin/update_plan

COPY analyse_results.py  /usr/bin/analyse_results

USER root
