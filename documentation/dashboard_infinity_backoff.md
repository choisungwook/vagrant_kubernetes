# 상황
* dashboard pod이 실행되지 않고 무한 backoff

![상황](./imgs/dashboard_backoff.png)

<br> pod 로그

<br>

# 해결
* 클러스터 생성시 pod network대역을 변경(172.16.0.0/16으로)
  * CNI(ex: calico) 네트워크 대역과 충돌하는 것으로 추측
```yaml
- name: Initialize the Kubernetes cluster using kubeadm
  command: > 
    kubeadm init 
    --apiserver-advertise-address="{{ ansible_host }}" 
    --apiserver-cert-extra-sans="{{ ansible_host }}" 
    --node-name "{{ master_name }}" 
    --pod-network-cidr=172.16.0.0/16
```

![해결](./imgs/dashboard_backoff.png)

<br> 해결한 후 pod dashboard 상태
# 참고자료
* https://github.com/kubernetes/dashboard/issues/3709