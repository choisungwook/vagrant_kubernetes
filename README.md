# 개요
* centos에서 k8s 설치

# 각 노드 IP 수동 설정
* 제일 마지막줄에 --node-ip 추가
```
sudo vi /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf

ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS --node-ip [ip]
```
* 서비스 재실행
```
sudo systemctl daemon reload
sudo systemctl restart kubelet
```

# 대시보드 설치
* 헬름 설치
* 대시보드 설치
```
helm install stable/kubernetes-dashboard --generate-name
```
* 프록시
```
kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='.*'
```
* 접속
```
http://[마스터IP]:8001/api/v1/namespaces/default/services/https:kubernetes-dashboard-1606573807:/proxy/
```


# 참고자료
* [1] dashboard 설치 영상: https://youtu.be/6MnsSvChl1E
* [2] install k8s playbooks role: https://github.com/geerlingguy/ansible-role-kubernetes/blob/master/tasks/main.yml
* [3] dashboard 공식문서: https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/
* [4] dashboard 공식git: https://github.com/kubernetes/dashboard