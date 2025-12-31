FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl

RUN apt-get install wget apt-transport-https gnupg lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y trivy

RUN trivy image --exit-code 1 --severity HIGH,CRITICAL ubuntu:latest || exit 1

CMD ["/bin/bash"]