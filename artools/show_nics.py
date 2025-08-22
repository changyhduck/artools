from Lib.network import get_physical_nics

def main():
    nics = get_physical_nics()
    if not nics:
        print("找不到任何實體網路卡。")
    else:
        print("本機實體網路卡：")
        for nic in nics:
            print(f"- {nic['name']}  狀態: {nic['state']}  速度: {nic['speed']} Mbps  最大速度: {nic['max_speed']} Mbps")

if __name__ == "__main__":
    main()
