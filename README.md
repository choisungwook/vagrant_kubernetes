# centos_kubernetes
centos_kubernetes + NFS 설정

# NFS 설정
1. vagrantfile NFS_IP 수정
2. k8f_nfs_configuration/master/files/deployment.yml env, volume에서 IP 수정
```yml
  env:
    - name: PROVISIONER_NAME
      value: nfs-storage
    - name: NFS_SERVER
      value: 192.168.219.201
    - name: NFS_PATH
      value: /home/vagrant/nfs
volumes:
  - name: nfs-client-root
    nfs:
      server: 192.168.219.201
      path: /home/vagrant/nfs
```
3. k8f_nfs_configuration/master/files/storage의 provisioner이름과 k8f_nfs_configuration/master/files/deployment.yml의 env PROVISIONER_NAME과 일치

# 참고자료
* [1] dashboard 설치 영상: https://youtu.be/6MnsSvChl1E
* [2] install k8s playbooks role: https://github.com/geerlingguy/ansible-role-kubernetes/blob/master/tasks/main.yml
* [3] dashboard 공식문서: https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/
* [4] dashboard 공식git: https://github.com/kubernetes/dashboard
* [5] nfs 설정1: https://gruuuuu.github.io/cloud/k8s-volume/#
* [6] nfs 설정2: https://tommypagy.tistory.com/186
* [7] nfs 설정3: https://blog.exxactcorp.com/deploying-dynamic-nfs-provisioning-in-kubernetes/