FROM ubuntu:18.04
RUN sed -i s/^deb-src.*// /etc/apt/sources.list
RUN apt-get update && apt-get install --yes iputils-ping silversearcher-ag wget python python-pip vim git-core && \
    pip install --upgrade pip

RUN wget -O /install_rally.sh https://raw.githubusercontent.com/openstack/rally/master/install_rally.sh
RUN bash /install_rally.sh --target /venv_rally
RUN echo 'source /venv_rally/bin/activate' >> /root/.bashrc
# COPY nvim /nvim

# RUN bash /nvim/nvim_install && \
#    bash /nvim/nvim_config
COPY openstack /root/openstack
ENV PATH="/venv_rally/bin:$PATH"
RUN pip install git+https://github.com/openstack/rally-openstack.git
RUN pip install 'urllib3==1.24.2' 'pyasn1<0.5.0,>=0.4.6'
