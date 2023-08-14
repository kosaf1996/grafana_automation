import yaml #pip install pyyaml

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
                "job_name": k,
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
                "job_name": k,
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

###########################################
###           Main Function             ###
###########################################
if __name__ == "__main__":
    
    #Conf Value Input
    master = input("Master IP : ")
    linux_slave_num = int(input("Linux Salve Node Num : ")) + 1
    windows_slave_num = int(input("Windows Salve Node Num : ")) +1
    
    linux_slave_ip_list = []
    linux_salve_name_list = []
    
    windows_slave_ip_list = []
    windows_salve_name_list = []
    
    
    for i  in range(1, linux_slave_num ):
        linux_slave_ip = input("Linux Salve IP : ")
        linux_slave_ip_list.append(linux_slave_ip)
        linux_slave_name = input("Linux Salve Name : ")
        linux_salve_name_list.append(linux_slave_name)
    
    for i in range(1, windows_slave_num):
        windows_slave_ip = input("Windows Salve IP : ")
        windows_slave_ip_list.append(windows_slave_ip)
        windows_slave_name = input("Windows Salve Name : ")
        windows_salve_name_list.append(windows_slave_name)
        
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
    
    #Windows Confg Call
    grafana_conf_call.windows_conf_generator()
    #Linux Confg Call
    grafana_conf_call.linux_conf_generator()
    #Inventory Conf Call
    ansible_conf_call.create_inventory()
