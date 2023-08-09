import yaml #pip install pyyaml

###########################################################################
####                        Grafana Conf Calss                         ####
###########################################################################
class grafana_conf():
    def __init__(self,master, linux_slave_list,windows_slave_list) -> None:
        self.master = master
        self.linux_slave_list = linux_slave_list
        self.windows_slave_list = windows_slave_list
    
    ###########################################
    ###            Windows Conf             ###
    ###########################################
    def windows_conf_generator(self):
        yml_data = {}
        yml_data['scrape_configs'] = []

        for num, configs in enumerate(self.windows_slave_list, 1):
            yml_data['scrape_configs'].append({
                "job_name": "windows_prometheus-"+ str(num),
                "static_configs": 
                    
                        {
                            'targets': f"""["{configs}:9182"]""",
                        }
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

        for num, configs in enumerate(self.linux_slave_list, 1):
            yml_data['scrape_configs'].append({
                "job_name": "prometheus-"+ str(num),
                "static_configs": 
                    
                        {
                            'targets': f"""["{configs}:9182"]""",
                        }
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
            
            with open("prometheus_windows.yml", "wt") as windows_w:
                windows_read = windows_read.replace('\'[', '[')
                windows_read = windows_read.replace(']\'', ']')
                windows_write = windows_w.write(windows_read)

        elif os == 'linux':
            with open("prometheus.yml", "rt") as windows_r:
                windows_read = windows_r.read()
            
            with open("prometheus.yml", "wt") as windows_w:
                windows_read = windows_read.replace('\'[', '[')
                windows_read = windows_read.replace(']\'', ']')
                windows_write = windows_w.write(windows_read)
      

class git_call():
    def __init__(self) -> None:
        pass
        

###########################################
###           Main Function             ###
###########################################
if __name__ == "__main__":
    
    #Conf Value Input
    master = input("Master IP : ")
    linux_slave_num = int(input("Linux Salve Node Num : ")) + 1
    windows_slave_num = int(input("Windows Salve Node Num : ")) + 1
    
    linux_slave_list = []
    windows_slave_list = []
    
    for i  in range(1, linux_slave_num ):
        linux_slave = input("Linux Salve IP : ")
        linux_slave_list.append(linux_slave)
        
    
    for i in range(1, windows_slave_num):
        windows_slave = input("Windows Salve IP : ")
        windows_slave_list.append(windows_slave)
        
    #Init Function Conf
    grafana_conf_call = grafana_conf(
        master,
        linux_slave_list,
        windows_slave_list
    )
    
    #Windows Confg Call
    grafana_conf_call.windows_conf_generator()
    #Linux Confg Call
    grafana_conf_call.linux_conf_generator()
