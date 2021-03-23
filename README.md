- [1. 개요](#1-개요)
- [2. 설정](#2-설정)
  - [ip 수정](#ip-수정)
- [3. 설치](#3-설치)
- [4. 삭제](#4-삭제)
- [3. 참고자료](#3-참고자료)

# 1. 개요
* vagrant와 ansible을 이용하여 쿠버네티스 자동 설치
* node os: centos7

<br>

# 2. 설정
## ip 수정
* bootstrap
  * ansible_workspace/add_hosts.yaml 3번째 줄 수정
* masternode ip
  * ansible_workspace/add_hosts.yaml 12번째 줄 수정
  * Vagrantfile 4번째 줄 수정
* workernode ip
  * ansible_workspace/add_hosts.yaml 5번째 줄 수정
  * Vagrantfile 15번째 줄부터 수정

<br>

# 3. 설치
* cluster 설치
```sh
vagrant up
```

* kubeconfig 복사
```sh
vagrant ssh k8s-master
sudo su ; root계정 스위칭
cp -r /home/vagrant/.kube/ /root/.kube
```

<br>

# 4. 삭제
```sh
vagrant destroy
```

<br>

# 3. 참고자료
* [1] dashboard 설치 영상: https://youtu.be/6MnsSvChl1E
* [2] install k8s playbooks role: https://github.com/geerlingguy/ansible-role-kubernetes/blob/master/tasks/main.yml
* [3] dashboard 공식문서: https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/
* [4] dashboard 공식git: https://github.com/kubernetes/dashboard