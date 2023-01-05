interval = 2

cpu_info = {
        'cpu_times':{
            'mean': None,
            'per_cpu': None
        },
        'cpu_percent':{
            'mean': None,
            'per_cpu': None
        },
        'cpu_count':{
            'physical': None,
            'logical': None
        },
        'cpu_stats': None,
        'cpu_freq':{
            'aggregate': None,
            'per_cpu': None
        },
        'cpu_load': None
    }

mem_info = {
    'mem_virt' : None,
    'mem_swap' : None
}

disk_info = {
    'disk_part': None,
    'disk_util': None,
    'disk_io': None
}

net_info = {
    'net_io' : {
        'mean' : None,
        'per_nic' : None
    },
    'net_iface' : None,
    'net_if_addr' : None, 
    'net_if_stat' : None 
}