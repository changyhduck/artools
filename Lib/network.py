import os

def list_nic_interfaces():
    """
    List network interfaces, excluding 'lo', bridges, and bondings.
    """
    interfaces = []
    sys_class_net = "/sys/class/net"
    for iface in os.listdir(sys_class_net):
        if iface == "lo":
            continue
        iface_path = os.path.join(sys_class_net, iface)
        # Exclude bridges
        if os.path.exists(os.path.join(iface_path, "bridge")):
            continue
        # Exclude bondings
        if os.path.exists(os.path.join(iface_path, "bonding")):
            continue
        interfaces.append(iface)
    return interfaces

def main():
    interfaces = list_nic_interfaces()
    print("Available network interfaces (excluding 'lo', bridges, and bondings):")
    for iface in interfaces:
        print(f"- {iface}")

if __name__ == "__main__":
    main()
