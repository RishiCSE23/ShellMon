import psutil as ps
from flask import Flask
from pprint import PrettyPrinter
import gloabal_vars 
import numpy as np
from threading import Thread
 
pp = PrettyPrinter(indent=2)




def get_cpu_info():
    # CPU data collection 
    cpu_info = gloabal_vars.cpu_info

    cpu_times = ps.cpu_times(percpu=False)
    cpu_times_per_cpu = ps.cpu_times(percpu=True)
    cpu_percent_per_cpu = ps.cpu_percent(interval=gloabal_vars.interval, percpu=True)
    cpu_percent = np.mean(cpu_percent_per_cpu)
    cpu_count_physical = ps.cpu_count(logical=False)
    cpu_count_logical = ps.cpu_count(logical=True)
    cpu_stats = ps.cpu_stats()
    cpu_freq=ps.cpu_freq(percpu=False)
    cpu_freq_per_cpu=ps.cpu_freq(percpu=True)
    cpu_avg_load = ps.getloadavg()

    # get cpu times
    cpu_info['cpu_times']['mean'] = {field: getattr(cpu_times, field) for field in cpu_times._fields} # dict comprehension {attr : val_of_attr}
    cpu_info['cpu_times']['per_cpu'] = {f'cpu_{cpu_times_per_cpu.index(inner_obj)}' :   # getting cpu index 
                                                { field :                                   # attr of each cpu    
                                                    getattr(inner_obj, field)               # val_of(attr) of each cpu      
                                                    for field in inner_obj._fields          # for attr in the field_list
                                                } 
                                                for inner_obj in cpu_times_per_cpu          # for each cpu in the cpu_list
                                        }

    # get cpu percent
    cpu_info['cpu_percent']['per_cpu']={ f'cpu_{cpu_percent_per_cpu.index(inner_val)}' :
                                             inner_val for inner_val in cpu_percent_per_cpu  
                                        }
    cpu_info['cpu_percent']['mean'] = cpu_percent

    # get cpu count
    cpu_info['cpu_count']['physical'] = cpu_count_physical
    cpu_info['cpu_count']['logical'] = cpu_count_logical

    # get cpu stats
    cpu_info['cpu_stats']={ field : getattr(cpu_stats, field) for field in cpu_stats._fields }

    # get cpu freq
    cpu_info['cpu_freq']['aggregate'] = {field: getattr(cpu_freq, field) for field in cpu_freq._fields}
    cpu_info['cpu_freq']['per_cpu'] = {f'cpu_{cpu_freq_per_cpu.index(cpu)}' : 
                                            {field: getattr(cpu_freq, field) 
                                                for field in cpu_freq._fields
                                            } 
                                            for cpu in cpu_freq_per_cpu
                                        }
    cpu_info['cpu_load'] = {
        '1m' : cpu_avg_load[0], 
        '5m' : cpu_avg_load[1],
        '15m' : cpu_avg_load[2]
    }
    
    return cpu_info

def get_mem_info():
    # MEM data colleciton
    mem_info = gloabal_vars.mem_info

    mem_virt = ps.virtual_memory()
    mem_swap = ps.swap_memory()

    mem_info['mem_virt'] = {field : getattr(mem_virt, field) for field in mem_virt._fields}
    mem_info['mem_swap'] = {field : getattr(mem_swap, field) for field in mem_swap._fields}

    return mem_info
    
def get_disk_info():
    # DISK data collection 
    disk_info = gloabal_vars.disk_info
    
    disk_part = ps.disk_partitions(all=True)
    disk_usage = ps.disk_usage('/')
    disk_io = ps.disk_io_counters()

    disk_info['disk_part'] = { f'part_{disk_part.index(part)}' : { field : getattr(part, field) for field in part._fields } for part in disk_part }
    disk_info['disk_util'] = {field : getattr(disk_usage, field) for field in disk_usage._fields}
    disk_info['disk_io'] = {field : getattr(disk_io, field) for field in disk_io._fields}

    return disk_info

def get_net_info():
    # NET Collection 
    net_info = gloabal_vars.net_info

    net_io = ps.net_io_counters(pernic=False, nowrap=True)
    net_io_per_nic = ps.net_io_counters(pernic=True, nowrap=True)
    net_if_addr = ps.net_if_addrs()
    net_if_status = ps.net_if_stats()

    net_info['net_io']['mean'] = {field : getattr(net_io, field) for field in net_io._fields}
    net_info['net_io']['per_nic'] = {iface : 
                                        { field : 
                                            getattr( net_io_per_nic[iface], field) 
                                            for field in net_io_per_nic[iface]._fields  
                                        } 
                                        for iface in net_io_per_nic
                                    } 
    
    net_info['net_if_status'] = { iface : 
                                    { field : getattr(net_if_status[iface], field) 
                                        for field in net_if_status[iface]._fields  
                                    } 
                                    for iface in net_if_status
                                }

    _net_if_addr = {}
    for iface in net_if_addr:  # key 
        addr={}
        for addr_obj in net_if_addr[iface]: # dict[key] = list
            if str(getattr(addr_obj, 'family')) == 'AddressFamily.AF_LINK':    # MAC
                addr['mac'] = getattr(addr_obj, 'address')
            elif str(getattr(addr_obj, 'family')) == 'AddressFamily.AF_INET':   # IPv4
                addr['ipv4'] = {
                    'addr' : getattr(addr_obj, 'address'),
                    'mask' : getattr(addr_obj, 'netmask')
                }
            elif str(getattr(addr_obj, 'family')) == 'AddressFamily.AF_INET6':  # IPv6
                addr['ipv6'] = getattr(addr_obj, 'address')
            
        _net_if_addr[iface] = addr

    net_info['net_if_addr'] = _net_if_addr

    return net_info

def get_collection():
    # thread_pool = []
    
    # thread_pool.append(Thread(target=get_cpu_info()))
    # thread_pool.append(Thread(target=get_mem_info()))
    # thread_pool.append(Thread(target=get_disk_info()))
    # thread_pool.append(Thread(target=get_net_info()))

    # for thread in thread_pool:
    #     thread.start()    

    result = {
        'cpu' : get_cpu_info(),
        'memory' : get_mem_info(),
        'disk': get_disk_info(),
        'netork': get_net_info()
    }

    #pp.pprint(result)
    return result

if __name__ == "__main__":
    get_collection()