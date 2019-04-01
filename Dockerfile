FROM centos:centos6

# ===============================================
# INSTALL BASIC TOOLS
# ===============================================
RUN yum -y update;
RUN yum -y clean all;
RUN yum install -y wget dialog curl sudo lsof vim axel telnet nano openssh-server openssh-clients bzip2 passwd tar bc git unzip
RUN yum install -y gcc openssl-devel bzip2-devel yum-utils 
RUN yum groupinstall -y "Development Tools"
RUN yum install -y epel-release
RUN yum install -y jq

# ===============================================
# INSTALL PYTHON 3.6
# ===============================================
RUN yum -y install https://centos6.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u python36u-pip python36u-devel
RUN yum -y install python36-numpy scipy
RUN echo "alias python=python3.6" >> ~/.bashrc
RUN echo "alias pip=pip3.6" >> ~/.bashrc
RUN source ~/.bashrc
RUN pip3.6 install --upgrade pip

# ===============================================
# INSTALL JAVA
# ===============================================
RUN yum install -y java-1.8.0-openjdk java-1.8.0-openjdk-devel 


# ===============================================
# CREATE GUEST USER. IMPORTANT: Change here UID 1000 to your host UID if you plan to share folders.
# ===============================================
RUN useradd guest -u 1000
RUN echo guest | passwd guest --stdin
ENV HOME /home/guest
WORKDIR $HOME

# ===============================================
# INSTALL APACHE KAFKA
# ===============================================
RUN wget https://www-eu.apache.org/dist/kafka/2.1.1/kafka_2.11-2.1.1.tgz
RUN tar xvzf kafka_2.11-2.1.1.tgz
RUN mv kafka_2.11-2.1.1 kafka
# ===============================================
# INSTALL SPARK
# ===============================================
#Install Spark (Spark 2.1.1 - 02/05/2017, prebuilt for Hadoop 2.7 or higher)
RUN wget https://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz
RUN tar xvzf spark-2.2.0-bin-hadoop2.7.tgz
RUN mv spark-2.2.0-bin-hadoop2.7 spark
RUN rm -f spark-2.2.0-bin-hadoop2.7.tgz
ENV SPARK_HOME $HOME/spark

# ===============================================
# INSTALL ELASTICSEARCH
# ===============================================
ADD elasticsearch.repo /etc/yum.repos.d/elasticsearch.repo
RUN yum install -y elasticsearch
ADD elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

# ===============================================
# INSTALL KIBANA
# ===============================================
ADD kibana.repo /etc/yum.repos.d/kibana.repo
RUN yum install -y kibana
ADD kibana.yml /etc/kibana/kibana.yml

# ===============================================
# ENVIRONMENT VARIABLES FOR SPARK & JAVA
# ===============================================
ADD setenv.sh /home/guest/setenv.sh
RUN chown guest:guest setenv.sh
RUN echo . ./setenv.sh >> .bashrc

# ===============================================
# SCRIPT TO START SERVICES (SSH,Zookeeper, Kafka producer...)
# ===============================================
ADD startup_script.sh /usr/bin/startup_script.sh
RUN chmod +x /usr/bin/startup_script.sh


# ===============================================
# Copy project folder
# ===============================================
COPY dataset-services /home/guest/

