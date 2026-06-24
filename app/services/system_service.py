import psutil


def get_cpu_data():
    return {
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count()
    }


def get_memory_data():
    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent
    }


def get_storage_data():
    partitions = psutil.disk_partitions()
    all_partitions_details = []

    for disk in partitions:
        try:
            usage = psutil.disk_usage(disk.mountpoint)

            all_partitions_details.append({
                "device": disk.device,
                "mountpoint": disk.mountpoint,
                "filesystem": disk.fstype,
                "options": disk.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })

        except PermissionError:
            continue

    return all_partitions_details


def get_processes_data():
    processes = []

    for process in psutil.process_iter([
        "pid",
        "name",
        "status",
        "memory_percent",
        "cpu_percent",
        "create_time"
    ]):
        try:
            processes.append(process.info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes


def get_ports_data():
    connections = []

    for connection in psutil.net_connections():
        connections.append({
            "local_address": connection.laddr.ip if connection.laddr else None,
            "local_port": connection.laddr.port if connection.laddr else None,
            "remote_address": connection.raddr.ip if connection.raddr else None,
            "remote_port": connection.raddr.port if connection.raddr else None,
            "status": connection.status,
            "pid": connection.pid
        })

    return connections


def get_summary_data():
    memory = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)

    total_storage = 0
    used_storage = 0
    free_storage = 0

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            total_storage += usage.total
            used_storage += usage.used
            free_storage += usage.free

        except PermissionError:
            continue

    return {
        "cpu": {
            "usage_percent": cpu_usage,
            "cores": psutil.cpu_count()
        },
        "memory": {
            "total": memory.total,
            "used": memory.used,
            "available": memory.available,
            "percent": memory.percent
        },
        "storage": {
            "total": total_storage,
            "used": used_storage,
            "free": free_storage
        },
        "processes_count": len(psutil.pids())
    }


def get_services_data():
    services = []

    try:
        for service in psutil.win_service_iter():
            try:
                info = service.as_dict()

                services.append({
                    "name": info["name"],
                    "display_name": info["display_name"],
                    "status": info["status"],
                    "start_type": info["start_type"],
                    "pid": info["pid"]
                })

            except psutil.Error:
                continue

    except AttributeError:
        return []

    return services


def kill_process_by_pid(pid: int):
    process = psutil.Process(pid)
    process.terminate()

    return {
        "pid": pid,
        "status": "terminated"
    }