import yaml #pip install pyyaml
import subprocess
import pysftp

###########################################################################
####                        Grafana Conf Calss                         ####
###########################################################################
class grafana_conf():
    def __init__(self,master,  linux_slave_dic,windows_slave_dic) -> None:
        self.master = master
        self.linux_slave_dic = linux_slave_dic
        self.windows_slave_dic = windows_slave_dic
    
    ###########################################
    ###            Windows Conf             ###
    ###########################################
    def windows_conf_generator(self):
        yml_data = {}
        yml_data['scrape_configs'] = []

        for k, v in self.windows_slave_dic.items():
            yml_data['scrape_configs'].append({
                "job_name": f"""{k}""",
                "static_configs": [
                    
                        {
                            'targets': f"""["{v}:9182"]""",
                        }
                    ]
                }
            )
  
        array={
            "global": {
                "scrape_interval": "1m"
            },
        }
        
        with open('prometheus_windows.yml', 'w') as fw:
            yaml.dump(array, fw)
            yaml.dump(yml_data,fw)
            fw.close()
            
        grafana_conf.yaml_replace(self, 'windows')
        
    def linux_conf_generator(self):
        yml_data = {}
        yml_data['scrape_configs'] = []

        for k, v in self.linux_slave_dic.items():
            yml_data['scrape_configs'].append({
                "job_name": f"""{k}""",
                "static_configs": [
                        {
                            'targets': f"""["{v}:9100"]""",
                        }
                    ]
                }
            )
  
        array={
            "global": {
                "scrape_interval": "1m"
            },
        }
        
        with open('prometheus.yml', 'w') as fw:
            yaml.dump(array, fw)
            yaml.dump(yml_data,fw)

            fw.close()
            
        grafana_conf.yaml_replace(self, 'linux')

    ###########################################
    ###            Yaml Replace             ###
    ###########################################
    def yaml_replace(self, os):
        
        if os == 'windows':
            with open("prometheus_windows.yml", "rt") as windows_r:
                windows_read = windows_r.read()
                windows_r.close()
            
            with open("prometheus_windows.yml", "wt") as windows_w:
                windows_read = windows_read.replace('\'[', '[')
                windows_read = windows_read.replace(']\'', ']')
                windows_write = windows_w.write(windows_read)
                windows_w.close()

        elif os == 'linux':
            with open("prometheus.yml", "rt") as windows_r:
                windows_read = windows_r.read()
                windows_r.close()
            
            with open("prometheus.yml", "wt") as windows_w:
                windows_read = windows_read.replace('\'[', '[')
                windows_read = windows_read.replace(']\'', ']')
                windows_write = windows_w.write(windows_read)
                windows_w.close()
###########################################################################
####                        Ansible Conf Calss                         ####
###########################################################################     
class ansible_conf():
    def __init__(self, master, linux_slave_list) -> None:
        self.master = master
        self.linux_slave_list = linux_slave_list

    ###########################################
    ###          Create Inventory           ###
    ###########################################
    def create_inventory(self):
        #master
        master_list = []
        slave_list = []
        all_list = []
        
        master_list.append("[master]")
        slave_list.append("[node]")
        all_list.append("[all]")
        all_list.append(self.master)
        
        master_list.append(self.master)
        
        for slave in self.linux_slave_list:
            slave_list.append(slave)
            all_list.append(slave)
        
        with open("Inventory", "a") as inv:
            for master in master_list:
                inv.write(master + '\n')
            for slave in slave_list:
                inv.write(slave + '\n')
            for all in all_list:
                inv.write(all + '\n')
            inv.close()
            
###########################################################################
####                     SubProcess Conf Calss                         ####
########################################################################### 
class process_run():
    def __init__(self) -> None:
        pass 
    
    
    def docker_install(self):
        print("Docker Install")
        docker_install = subprocess.call("ansible-playbook -i /docker-compose/Inventory /docker-compose/docker_install.yaml", shell=True)
        print("Git Clone")
        git_clone = subprocess.call("ansible-playbook -i /docker-compose/Inventory /docker-compose/docker_install.yaml", shell=True)
    def ansible_run(self):
        print("Node Exporter UP")
        node_exporter = subprocess.call("ansible-playbook -i /docker-compose/Inventory /docker-compose/node_exporter_ansible.yaml", shell=True)
        
        print("Master Grafana UP")
        master = subprocess.call("ansible-playbook -i /docker-compose/Inventory /docker-compose/git_clone_ansible.yaml",shell=True)
        
###########################################################################
####                       Fluentd Conf Calss                          ####
########################################################################### 
class fluentd():
    def __init__(self, master,  linux_slave_dic, access_key, secret_key, bucket, master_name):
        self.master = master
        self.master_name = master_name
        self.linux_slave_dic = linux_slave_dic
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
    
    ###########################################
    ###            Fluentd Conf             ###
    ###########################################
    def replace(self):
        
        dic_tem = None
        for k, v in self.linux_slave_dic.items():
            if dic_tem == None:
                with open("/docker-compose/fluentd/fluent_cent.conf", "rt") as fluent_cent_r:
                        fluentd_read = fluent_cent_r.read()
                        fluent_cent_r.close()
                    
                with open("/docker-compose/fluentd/fluent_cent.conf", "wt") as fluentd_cent_w:
                        fluentd_read = fluentd_read.replace('<Server_NAME>', k)
                        fluentd_read = fluentd_read.replace('<access_key>', self.access_key)
                        fluentd_read = fluentd_read.replace('<secret_key>', self.secret_key)
                        fluentd_read = fluentd_read.replace('<bucket_name>', self.bucket)
                        fluentd_write = fluentd_cent_w.write(fluentd_read)
                        fluentd_cent_w.close()
                        
                with open("/docker-compose/fluentd/fluent_ubuntu.conf", "rt") as fluent_ubuntu_r:
                        fluentd_read = fluent_ubuntu_r.read()
                        fluent_ubuntu_r.close()
                    
                with open("/docker-compose/fluentd/fluent_ubuntu.conf", "wt") as fluentd_ubuntu_w:
                        fluentd_read = fluentd_read.replace('<Server_NAME>', k)
                        fluentd_read = fluentd_read.replace('<access_key>', self.access_key)
                        fluentd_read = fluentd_read.replace('<secret_key>', self.secret_key)
                        fluentd_read = fluentd_read.replace('<bucket_name>', self.bucket)
                        fluentd_write = fluentd_ubuntu_w.write(fluentd_read)
                        fluentd_ubuntu_w.close()
                        
                dic_tem = k
                fluentd.scp(self, v)
                
            elif dic_tem != None:
                with open("/docker-compose/fluentd/fluent_cent.conf", "rt") as fluent_cent_r:
                        fluentd_read = fluent_cent_r.read()
                        fluent_cent_r.close()
                    
                with open("/docker-compose/fluentd/fluent_cent.conf", "wt") as fluentd_cent_w:
                        fluentd_read = fluentd_read.replace(dic_tem, k)
                        fluentd_write = fluentd_cent_w.write(fluentd_read)
                        fluentd_cent_w.close()
                        
                with open("/docker-compose/fluentd/fluent_ubuntu.conf", "rt") as fluent_ubuntu_r:
                        fluentd_read = fluent_ubuntu_r.read()
                        fluent_ubuntu_r.close()
                    
                with open("/docker-compose/fluentd/fluent_ubuntu.conf", "wt") as fluentd_ubuntu_w:
                        fluentd_read = fluentd_read.replace(dic_tem, k)
                        fluentd_write = fluentd_ubuntu_w.write(fluentd_read)
                        fluentd_ubuntu_w.close()
                
                dic_tem = k
                fluentd.scp(self, v)
            
        with open("/docker-compose/fluentd/fluent_cent.conf", "rt") as fluentd_cent_r:
                fluentd_read = fluentd_cent_r.read()
                fluentd_cent_r.close()
                    
        with open("/docker-compose/fluentd/fluent_cent.conf", "wt") as fluentd_cent_w:
                fluentd_read = fluentd_read.replace(dic_tem, self.master_name)
                fluentd_write = fluentd_cent_w.write(fluentd_read)
                fluentd_cent_w.close()
                
        with open("/docker-compose/fluentd/fluent_ubuntu.conf", "rt") as fluentd_ubuntu_r:
                fluentd_read = fluentd_ubuntu_r.read()
                fluentd_ubuntu_r.close()
                    
        with open("/docker-compose/fluentd/fluent_ubuntu.conf", "wt") as fluentd_ubuntu_w:
                fluentd_read = fluentd_read.replace(dic_tem, self.master_name)
                fluentd_write = fluentd_ubuntu_w.write(fluentd_read)
                fluentd_ubuntu_w.close()

    ###########################################
    ###         Fluentd Conf Deploy         ###
    ###########################################
    def scp(self, ip):
        #Connection
        try:
            # Get the sftp connection object
            connection = pysftp.Connection(
                host=ip,
                username='root',
                port=22
            )
        except Exception as err:
            raise Exception(err)
        finally:
            print(f"Connected to {ip}as root.")
            
        #SCP File PUT
        try:
            print(
                f"uploading to {ip} as root "
            )

            # Download file from SFTP
            connection.put("/docker-compose/fluentd/fluent_cent.conf", "/docker-compose/fluentd/fluent_cent.conf")
            connection.put("/docker-compose/fluentd/fluent_ubuntu.conf", "/docker-compose/fluentd/fluent_ubuntu.conf")
            print("upload completed")

        except Exception as err:
            raise Exception(err)

            
        #Connection Close
        connection.close()




###########################################
###           Main Function             ###
###########################################
if __name__ == "__main__":
    
    #Conf Value Input
    master = input("Master IP : ")
    master_name = input("Master Name : ")
    linux_slave_num = int(input("Linux Salve Node Num : ")) + 1
    windows_slave_num = int(input("Windows Salve Node Num : ")) +1
    
    #공백 제거
    master = master.strip()
    
    linux_slave_ip_list = []
    linux_salve_name_list = []
    
    windows_slave_ip_list = []
    windows_salve_name_list = []
    
    
    for i  in range(1, linux_slave_num ):
        linux_slave_ip = input("Linux Salve IP : ")
        linux_slave_ip = linux_slave_ip.strip()
        linux_slave_ip_list.append(linux_slave_ip)
        linux_slave_name = input("Linux Salve Name : ")
        linux_slave_name = linux_slave_name.strip()
        linux_salve_name_list.append(linux_slave_name)
    
    for i in range(1, windows_slave_num):
        windows_slave_ip = input("Windows Salve IP : ")
        windows_slave_ip = windows_slave_ip.strip()
        windows_slave_ip_list.append(windows_slave_ip)
        windows_slave_name = input("Windows Salve Name : ")
        windows_slave_name = windows_slave_name.strip()
        windows_salve_name_list.append(windows_slave_name)
        
    access_key = input("Access Key : ")
    secret_key = input("Secret Key : ") 
    bucket = input("Bucket Name : ")
        
    linux_slave_dic = dict(zip(linux_salve_name_list, linux_slave_ip_list))
    windows_slave_dic =  dict(zip(windows_salve_name_list, windows_slave_ip_list))
        
    #Init Function Conf
    grafana_conf_call = grafana_conf(
        master,
        linux_slave_dic,
        windows_slave_dic

    )
    ansible_conf_call = ansible_conf(
        master,
        linux_slave_ip_list
    )
    process_start = process_run()
    
    fluentd_conf_call = fluentd(
        master, 
        linux_slave_dic,
        access_key, 
        secret_key, 
        bucket,
        master_name
    )
    
    #Windows Confg Call
    grafana_conf_call.windows_conf_generator()
    #Linux Confg Call
    grafana_conf_call.linux_conf_generator()
    #Inventory Conf Call
    ansible_conf_call.create_inventory()
    #Docker-Install
    process_start.docker_install()
    #Fluentd
    fluentd_conf_call.replace()
    #Process Start 
    process_start.ansible_run()
