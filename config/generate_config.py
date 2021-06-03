import chevron
import argparse
from ping3 import ping
from exception import UserDefinedException
import os
from pathlib import Path

# parsing input
parser = argparse.ArgumentParser()
parser.add_argument("--controlPlaneIPS", type=str, required=True, help="control-plane IPS")
parser.add_argument("--controlPlaneCPU", type=str, required=False, default="4", help="control-plane CPU")
parser.add_argument("--controlPlaneMemory", type=str, required=False, default="4096", help="control-plane Mmeory") # 4GB
parser.add_argument("--workerIPS", type=str, required=True, help="worker-node IPS")
parser.add_argument("--workerCPU", type=str, required=False, default="4", help="worker-node CPU")
parser.add_argument("--workerMemory", type=str, required=False, default="16384", help="worker-node Memory") # 16GB
parser.add_argument("--bootstrapIP", type=str, required=True, help="bootstrap IPS")
parser.add_argument("--bootstrapCPU", type=str, required=False, default="2", help="bootstrap CPU") 
parser.add_argument("--bootstrapMemory", type=str, required=False, default="2048", help="bootstrap Memory") # 2GB
args = parser.parse_args()


def split_args(arguments):
    """
        ","구분자로 split
        리턴: list
    """
    try:
        return arguments.split(",")
    except UserDefinedException as e:
        raise UserDefinedException(f"[-] split_args Error split: {e}")

def generate_template(config):
    '''
        yaml템플릿 생성
    '''
    try:
        with open('template.yml', 'r') as f:
            return chevron.render(f, 
                {
                    'config_key': config['keyname'],
                    'image': config['image'],
                    'name': config['name'],
                    'ip': config['ip'],
                    'memory': config['memory'],
                    'cpu': config['cpu']
                }
            )
    except Exception as e:
        raise UserDefinedException(f"[-] generate_template Error: {e}")

def create_vagrant_configfile(bootstrap_config, controlplane_configs, worker_configs):
    '''
        vagrant_config파일 생성
        생성위치: ../config.yml
    '''
    
    if not bootstrap_config:
        raise UserDefinedException(f"[-] create_vagrant_configfile Error: bootstrap_config is None")
    if not controlplane_configs or len(controlplane_configs) == 0:
        raise UserDefinedException(f"[-] create_vagrant_configfile Error: controlplane_configs is None")
    if not worker_configs or len(worker_configs) == 0:
        raise UserDefinedException(f"[-] create_vagrant_configfile Error: controlplane_configs is None")

    print()
    try:
        with open('vagrant_template.yml', 'r') as f:
            vagrant_config = chevron.render(f, 
                {
                    'masters': bootstrap_config,
                    'worekrs': "\n".join(controlplane_configs),
                    'numberOfworkers': len(worker_configs),
                    'bootstrap': "\n".join(worker_configs),
                }
            )

        output_path = os.path.join(Path(os.getcwd()).parent, 'config.yml')
        with open(output_path, 'w') as f:
            f.write(vagrant_config)
    except Exception as e:
        raise UserDefinedException(f"[-] generate_template Error: {e}")

def ping_to_configIP(target):
    """
        ping test
    """
    try:
        result = ping(target)

        return True if result else False
    except Exception as e:
        raise UserDefinedException(f"[-] ping error: {e}")

if __name__=="__main__":
    try:
        vagrant_image = "centos/7"
        bootstrap_IP = args.bootstrapIP
        controlplane_IPS = split_args(args.controlPlaneIPS)
        worker_IPS = split_args(args.workerIPS)
        controlplane_configs = []
        worker_configs = []
        bootstrap_config = None

        print("[*] print IPS")
        print(f"bootstrap: {bootstrap_IP}")
        print(f"masterIPs: {controlplane_IPS}")
        print(f"workerIPS: {worker_IPS}")
        print("\n")

        # 1. ping test
        print("[*] ping test start")
        if ping_to_configIP(bootstrap_IP):
            raise UserDefinedException(f"bootstrap IP is already exists: {bootstrap_IP}")

        for controlplane_IP in controlplane_IPS:
            if ping_to_configIP(controlplane_IP):
                raise UserDefinedException(f"master IP is already exists: {controlplane_IP}")

        for worekr_IP in worker_IPS:
            if ping_to_configIP(worekr_IP):
                raise UserDefinedException(f"worker IP is already exists: {worekr_IP}")
        print("[*] ping test done")
        print("\n")

        # 2. genreate template
        print("[*] generate bootstrap config")
        bootstrap_nodename= f"vagrant-bootstrap"
        bootstrap_config_dict = {
            'keyname': bootstrap_nodename,
            'image': vagrant_image,
            'name': bootstrap_nodename,
            'ip': args.bootstrapIP,
            'memory': args.bootstrapMemory,
            'cpu': args.bootstrapCPU
        }
        bootstrap_config = generate_template(bootstrap_config_dict)
        print("[*] generate bootstrap done")

        print("[*] generate controlplane_configs config")
        for idx, controlplane_IP in enumerate(controlplane_IPS):
            nodename= f"vagrant-controlpalne-{idx+1}"
            config = {
                'keyname': nodename,
                'image': vagrant_image,
                'name': nodename,
                'ip': controlplane_IP,
                'memory': args.controlPlaneMemory,                
                'cpu': args.controlPlaneCPU
            }
            controlplane_configs.append(generate_template(config))
        print("[*] generate controlplane_configs done")

        print("[*] generate worker config")
        for idx, worekr_IP in enumerate(worker_IPS):
            nodename= f"vagrant-worker-{idx+1}"
            config = {
                'keyname': nodename,
                'image': vagrant_image,
                'name': nodename,
                'ip': worekr_IP,
                'memory': args.workerMemory,
                'cpu': args.workerCPU
            }
            worker_configs.append(generate_template(config))
        print("[*] generate worker done")

        # 3. create vagrant_config.yml
        create_vagrant_configfile(bootstrap_config, controlplane_configs, worker_configs)

        
    except Exception as e:
        print(f"error: {e}")



