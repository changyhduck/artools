# 取得所有實體網路卡名稱（如 eth0, enp2s0 等）
import os
import re

def get_physical_nics():
	"""
	回傳所有實體網路卡資訊（名稱、連線狀態、目前速度、最大速度）。
	格式: [{"name":..., "state":..., "speed":..., "max_speed":...}, ...]
	"""
	nics = []
	net_path = "/sys/class/net"
	if os.path.isdir(net_path):
		for nic in os.listdir(net_path):
			if nic == "lo":
				continue
			nic_path = os.path.join(net_path, nic)
			if os.path.exists(os.path.join(nic_path, "device")):
				# 取得連線狀態
				state = "unknown"
				state_file = os.path.join(nic_path, "operstate")
				if os.path.isfile(state_file):
					with open(state_file) as f:
						state = f.read().strip()
				# 取得目前速度
				speed = None
				speed_file = os.path.join(nic_path, "speed")
				if os.path.isfile(speed_file):
					try:
						speed = int(open(speed_file).read().strip())
					except Exception:
						speed = None
				# 取得最大速度 (ethtool)
				max_speed = None
				try:
					import subprocess
					result = subprocess.run(["ethtool", nic], capture_output=True, text=True)
					for line in result.stdout.splitlines():
						if "Supported link modes" in line:
							# 之後的行可能有最大速度
							for l in result.stdout.splitlines():
								m = re.search(r"(\d+)baseT", l)
								if m:
									val = int(m.group(1))
									if max_speed is None or val > max_speed:
										max_speed = val
							break
				except Exception:
					pass
				nics.append({
					"name": nic,
					"state": state,
					"speed": speed,
					"max_speed": max_speed
				})
	return nics
