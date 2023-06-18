import requests
import argparse
import string
import random

# NetBox API settings
NETBOX_URL = "http://127.0.0.1"
NETBOX_TOKEN = "" # TODO API token generated in NetBox

# Site, device roles and types defined in NetBox
site_id = 0
router_role_id = 0
host_role_id = 0
router_device_type_id = 0
host_device_type_id = 0

# Initialize the requests session
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Token {NETBOX_TOKEN}",
})

# Holds ids of created routers and hosts
routers = {}
# Tag of the generated topology
tag = None


# Create generic resource using NetBox API
def netbox_create(name, path, model, put_tags=False):
    if put_tags:
        model["tags"] = [tag]
    response = session.post(f"{NETBOX_URL}{path}", json=model)
    if response.status_code >= 400:
        print(f"Error creating {name}: {response.text}")
        return

    print(f"Created {name} with id {response.json()['id']}")

    return response.json()["id"]


# Get id of generic resource using NetBox API
def netbox_get_id(name, path):
    response = session.get(f"{NETBOX_URL}{path}")
    if response.status_code >= 400:
        print(f"Error getting {name}: {response.text}")
        return

    return response.json()["results"][0]["id"]


# Create custom field using NetBox API
def create_custom_field(name, field_type, content_types, validation_minimum=0):
    custom_field = {
        "name": name,
        "type": field_type,
        "content_types": content_types,
        "validation_minimum": validation_minimum
    }

    return netbox_create(f"custom field {name}", "/api/extras/custom-fields/", custom_field)


# Create random tag using NetBox API
def create_random_tag():
    def generate_random_id():
        return ''.join(random.choice(string.ascii_letters) for i in range(6))

    tag_id = generate_random_id()
    tag = {
        "name": f"Dragonfly {tag_id}",
        "slug": f"dragonfly-{tag_id}"
    }

    netbox_create(f"tag {tag['name']}", "/api/extras/tags/", tag)

    return tag


# Create site using NetBox API
def create_site(name, slug):
    site = {
        "name": name,
        "slug": slug
    }

    return netbox_create(f"site {name}", "/api/dcim/sites/", site)


# Create device role using NetBox API
def create_device_role(name, slug, color="888888"):
    device_role = {
        "name": name,
        "slug": slug,
        "color": color
    }

    return netbox_create(f"device role {name}", "/api/dcim/device-roles/", device_role)


# Create manufacturer using NetBox API
def create_manufacturer(name, slug):
    manufacturer = {
        "name": name,
        "slug": slug
    }

    return netbox_create(f"manufacturer {name}", "/api/dcim/manufacturers/", manufacturer)


# Create device type using NetBox API
def create_device_type(model, slug, manufacturer_id, price):
    device_type = {
        "model": model,
        "slug": slug,
        "manufacturer": manufacturer_id,
        "custom_fields": {
            "price": price
        }
    }

    return netbox_create(f"device type {model}", "/api/dcim/device-types/", device_type)


# Create device using NetBox API
def create_device(name, type_id, role_id):
    device = {
        "name": name,
        "device_type": type_id,
        "device_role": role_id,
        "site": site_id
    }

    return netbox_create(f"device {name}", "/api/dcim/devices/", device, put_tags=True)


# Create interface for device using NetBox API
def create_interface(name, device_id):
    interface = {
        "name": name,
        "type": "1000base-t",
        "device": device_id,
    }

    return netbox_create(f"interface {name}", "/api/dcim/interfaces/", interface, put_tags=True)


# Create cable between two interfaces using NetBox API
def create_cable(interface1_id, interface2_id, length, price_per_meter, description, cable_type):
    cable = {
        "type": cable_type,
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
        "length": length,
        "length_unit": "m",
        "description": description,
        "custom_fields": {
            "price": length * price_per_meter
        }
    }

    return netbox_create(f"connection between {interface1_id} and {interface2_id} interfaces", "/api/dcim/cables/", cable, put_tags=True)


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

    create_cable(router_int_id, host_int_id, 10, price_per_meter=40, description="UGREEN RJ45 Cat.8 Ethernet", cable_type="cat8")


# Connect two routers
def connect_routers(g1_id, r1_id, g2_id, r2_id):
    # Make interfaces and connect them
    router1_id = routers[g1_id][r1_id]["id"]
    router2_id = routers[g2_id][r2_id]["id"]

    router1_int_id = create_interface(f"int-g{g1_id}-r{r1_id}-g{g2_id}-r{r2_id}", router1_id)
    router2_int_id = create_interface(f"int-g{g2_id}-r{r2_id}-g{g1_id}-r{r1_id}", router2_id)

    create_cable(router1_int_id, router2_int_id, 1000, price_per_meter=3968, description="Mellanox MFS1S50-H020V", cable_type="aoc")


def generate_dragonfly(p, a, h):
    # Dragonfly topology parameters
    # p - Number of hosts connected to each router
    # a - Number of routers in each group
    # h - Number of channels within each router used to connect to other groups
    # Balanced when a = 2 * p = 2 * h
    g = a * h + 1 # Number of groups in the system

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


def setup_models():
    global site_id, router_role_id, host_role_id, router_device_type_id, host_device_type_id

    create_custom_field("price", "decimal", ["dcim.cable", "dcim.devicetype"])
    site_id = create_site("Dragonfly site", "dragonfly-site")
    router_role_id = create_device_role("Router", "router")
    host_role_id = create_device_role("Host", "host")
    nvidia_id = create_manufacturer("Mellanox", "Nvidia")
    dell_id = create_manufacturer("Dell", "Dell")
    router_device_type_id = create_device_type("Mellanos MQM8790-HS2F", "Router_Mellanos_MQM8790", nvidia_id, 71472) #  US$18,344.00 (PLN zł71,472.17) 
    host_device_type_id = create_device_type("Dell PowerEdge R450", "Host_Dell_PowerEdge", dell_id, 21000)   #PLN 21000 zł


def find_models_ids():
    global site_id, router_role_id, host_role_id, router_device_type_id, host_device_type_id

    site_id = netbox_get_id("site", "/api/dcim/sites?slug=dragonfly-site")
    router_role_id = netbox_get_id("router role", "/api/dcim/device-roles?slug=router")
    host_role_id = netbox_get_id("host role", "/api/dcim/device-roles?slug=host")
    router_device_type_id = netbox_get_id("router type", "/api/dcim/device-types?slug=router")
    host_device_type_id = netbox_get_id("host type", "/api/dcim/device-types?slug=host")


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", help="Setup sites, manufacturers, device roles and device types", action="store_true")
    parser.add_argument("--hosts", help="Number of hosts connected to each router", default=2, type=int)
    parser.add_argument("--routers", help="Number of routers in each group", default=4, type=int)
    parser.add_argument("--channels", help="Number of channels within each router used to connect to other groups", default=2, type=int)
    return parser.parse_known_args()[0]


if __name__ == "__main__":
    args = parse_command_line()
    if args.setup:
        setup_models()
    else:
        find_models_ids()
    
    tag = create_random_tag()

    generate_dragonfly(args.hosts, args.routers, args.channels)
