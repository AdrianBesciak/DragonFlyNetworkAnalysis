import requests

# Dragonfly topology parameters
p = 2  # Number of hosts connected to each router
a = 4  # Number of routers in each group
h = 2  # Number of channels within each router used to connect to other groups
g = a * h + 1  # Number of groups in the system
# Balanced when a = 2 * p = 2 * h

# NetBox API settings
NETBOX_URL = "http://localhost:8000"
NETBOX_TOKEN = "" # TODO API token generated in NetBox

# Site, device roles and types defined in NetBox
site_id = 1
router_role_id = 1
host_role_id = 2
router_device_type_id = 1
host_device_type_id = 2

# Initialize the requests session
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Token {NETBOX_TOKEN}",
})

# Holds ids of created routers and hosts
routers = {}


# Create device using NetBox API
def create_device(name, type_id, role_id):
    device = {
        "name": name,
        "device_type": type_id,
        "device_role": role_id,
        "site": site_id,
    }

    response = session.post(f"{NETBOX_URL}/api/dcim/devices/", json=device)
    if response.status_code >= 400:
        print(f"Error creating device {name}: {response.text}")
        return

    id = response.json()["id"]
    print(f"Created device {name} with id {id}")

    return id


# Create interface for device using NetBox API
def create_interface(name, device_id):
    interface = {
        "name": name,
        "type": "1000base-t",
        "device": device_id,
    }

    response = session.post(f"{NETBOX_URL}/api/dcim/interfaces/", json=interface)
    if response.status_code >= 400:
        print(f"Error creating interface {name}: {response.text}")
        return

    id = response.json()["id"]
    print(f"Created interface {name} with id {id}")

    return id


# Create cable between two interfaces using NetBox API
def create_cable(interface1_id, interface2_id):
    cable = {
        "a_terminations": [
            {
                "object_type": "dcim.interface",
                "object_id": interface1_id,
            },
        ],
        "b_terminations": [
            {
                "object_type": "dcim.interface",
                "object_id": interface2_id,
            },
        ],
        "status": "connected",
    }

    response = session.post(f"{NETBOX_URL}/api/dcim/cables/", json=cable)
    if response.status_code >= 400:
        print(f"Error creating connection between {interface1_id} and {interface2_id} interfaces: {response.text}")
        return

    id = response.json()["id"]
    print(f"Created connection between {interface1_id} and {interface2_id} interfaces with id {id}")

    return id


def create_router(g_id, r_id):
    router_id = create_device(f"router-g{g_id}-r{r_id}", router_device_type_id, router_role_id)
    if router_id is None:
        return

    if g_id not in routers:
        routers[g_id] = {}
    routers[g_id][r_id] = {"id": router_id, "hosts": {}}


def create_host(g_id, r_id, h_id):
    host_id = create_device(f"host-g{g_id}-r{r_id}-h{h_id}", host_device_type_id, host_role_id)
    if host_id is None:
        return

    routers[g_id][r_id]["hosts"][h_id] = host_id


# Connect host to its router
def connect_host(g_id, r_id, h_id):
    # Make interfaces and connect them
    router_id = routers[g_id][r_id]["id"]
    host_id = routers[g_id][r_id]["hosts"][h_id]

    router_int_id = create_interface(f"int-g{g_id}-r{r_id}-h{h_id}", router_id)
    host_int_id = create_interface(f"int-g{g_id}-h{h_id}-r{r_id}", host_id)

    create_cable(router_int_id, host_int_id)


# Connect two routers
def connect_routers(g1_id, r1_id, g2_id, r2_id):
    # Make interfaces and connect them
    router1_id = routers[g1_id][r1_id]["id"]
    router2_id = routers[g2_id][r2_id]["id"]

    router1_int_id = create_interface(f"int-g{g1_id}-r{r1_id}-g{g2_id}-r{r2_id}", router1_id)
    router2_int_id = create_interface(f"int-g{g2_id}-r{r2_id}-g{g1_id}-r{r1_id}", router2_id)

    create_cable(router1_int_id, router2_int_id)


def generate_dragonfly(p, a, h, g):
    for g_id in range(g):
        for r_id in range(a):
            create_router(g_id, r_id)

            # Connect router within a group
            for r2_id in range(r_id):
                connect_routers(g_id, r_id, g_id, r2_id)

            # Connect router to specific routers in previous groups
            for g2_id in range(r_id * h, min((r_id + 1) * h, g_id)):
                if g2_id >= g_id:
                    g2_id += 1

                connect_routers(g_id, r_id, g2_id, (g_id - 1) // h)

            # Create and connect router's hosts
            for h_id in range(p):
                create_host(g_id, r_id, h_id)
                connect_host(g_id, r_id, h_id)


if __name__ == "__main__":
    generate_dragonfly(p, a, h, g)
