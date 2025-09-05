import curses
import platform
import os
import requests
import subprocess
import install_module
import install_web
import zfs_install

MENU_ITEMS = ["System Info", "Install Modules", "Change Sound", "After", "ZFS Install", "Web Install", "SNMP Install", "First Firmware Install", "Network Setting", "Reboot", "Exit"]

def draw_menu(stdscr, selected_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(MENU_ITEMS):
        x = 2  # Left-align the menu items
        y = h//2 - len(MENU_ITEMS)//2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)
    stdscr.refresh()

def show_system_info(stdscr):
    stdscr.clear()
    # Get latest kernel version from kernel.org
    try:
        response = requests.get("https://www.kernel.org/releases.json", timeout=3)
        latest_kernel = None
        if response.ok:
            data = response.json()
            for rel in data.get("releases", []):
                if rel.get("moniker") == "stable":
                    latest_kernel = rel.get("version")
                    break
        if not latest_kernel:
            latest_kernel = "Unknown"
    except Exception:
        latest_kernel = "Unavailable"
    info = [
        f"System: {platform.system()}",
        f"Node: {platform.node()}",
        f"Release: {platform.release()}",
        f"Version: {platform.version()}",
        f"Kernel: {platform.uname().release}",
        f"Latest Kernel (Internet): {latest_kernel}",
        f"Machine: {platform.machine()}",
        f"Processor: {platform.processor()}"
    ]
    for idx, line in enumerate(info):
        stdscr.addstr(idx+2, 2, line)
    # Draw the Update Kernel button
    button_label = "[ Update Kernel ]"
    button_y = len(info) + 4
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(button_y, 2, button_label)
    stdscr.attroff(curses.color_pair(1))
    stdscr.addstr(button_y+2, 2, "Press ENTER to update kernel, any other key to return...")
    stdscr.refresh()
    key = stdscr.getch()
    if key in [curses.KEY_ENTER, ord('\n')]:
        stdscr.clear()
        stdscr.addstr(2, 2, "Updating kernel (dnf -y update)...")
        stdscr.refresh()
        import subprocess
        try:
            result = subprocess.run(["dnf", "-y", "update"], capture_output=True, text=True)
            output_lines = result.stdout.splitlines()
            max_lines = 20
            for i, line in enumerate(output_lines[:max_lines]):
                stdscr.addstr(4 + i, 2, line[:curses.COLS-4])
            if len(output_lines) > max_lines:
                stdscr.addstr(4 + max_lines, 2, "...output truncated...")
            stdscr.addstr(6 + max_lines, 2, "Update finished. Press any key to return...")
        except Exception as e:
            stdscr.addstr(4, 2, f"Error: {e}\nPress any key to return...")
        stdscr.refresh()
        stdscr.getch()

def show_install_modules(stdscr):
    install_module.show_install_modules(stdscr)

def show_web_install(stdscr):
    install_web.show_web_install(stdscr)

def show_zfs_install(stdscr):
    zfs_install.show_zfs_install(stdscr)

def show_snmp_install(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "Install SNMP Tools")
    stdscr.addstr(3, 2, "This will run snmp_install.sh. Confirm? (y/n)")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord('y'):
        import subprocess
        try:
            subprocess.run(["bash", "snmp_install.sh"], check=True)
            stdscr.addstr(5, 2, "SNMP tools installed successfully.")
        except subprocess.CalledProcessError:
            stdscr.addstr(5, 2, "Error installing SNMP tools.")
    else:
        stdscr.addstr(5, 2, "Operation cancelled.")
    stdscr.addstr(7, 2, "Press any key to return to menu.")
    stdscr.refresh()
    stdscr.getch()

def show_first_firmware_install(stdscr):
    curses.curs_set(0)
    # Get list of firmware*.sh files
    firmware_files = [f for f in os.listdir('.') if f.startswith('firmware') and f.endswith('.sh')]
    if not firmware_files:
        stdscr.clear()
        stdscr.addstr(2, 2, "No firmware*.sh files found. Press any key...")
        stdscr.refresh()
        stdscr.getch()
        return
    current_idx = 0
    button_selected = 0  # 0 for Install, 1 for Exit

    while True:
        stdscr.clear()
        # Draw the list
        for i, f in enumerate(firmware_files):
            attr = curses.A_REVERSE if i == current_idx else curses.A_NORMAL
            stdscr.addstr(2 + i, 2, f, attr)
        # Draw buttons
        install_attr = curses.A_REVERSE if button_selected == 0 else curses.A_NORMAL
        exit_attr = curses.A_REVERSE if button_selected == 1 else curses.A_NORMAL
        stdscr.addstr(2 + len(firmware_files) + 2, 2, "[Install]", install_attr)
        stdscr.addstr(2 + len(firmware_files) + 2, 12, "[Exit]", exit_attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            if current_idx > 0:
                current_idx -= 1
            elif button_selected == 0:
                current_idx = len(firmware_files) - 1  # Wrap to last file
        elif key == curses.KEY_DOWN:
            if current_idx < len(firmware_files) - 1:
                current_idx += 1
            else:
                button_selected = 0  # Move to buttons
        elif key == curses.KEY_LEFT:
            if button_selected > 0:
                button_selected -= 1
        elif key == curses.KEY_RIGHT:
            if button_selected < 1:
                button_selected += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            if button_selected == 0:  # Install
                selected_file = firmware_files[current_idx]
                stdscr.clear()
                stdscr.addstr(2, 2, f"Running {selected_file}...")
                stdscr.refresh()
                try:
                    subprocess.run(["bash", selected_file], check=True)
                    stdscr.addstr(4, 2, "Script executed successfully. Press any key...")
                except subprocess.CalledProcessError as e:
                    stdscr.addstr(4, 2, f"Error executing script: {e}. Press any key...")
                stdscr.refresh()
                stdscr.getch()
                break
            elif button_selected == 1:  # Exit
                break

def show_network_setting(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 2, "Network Setting (placeholder)")
    stdscr.addstr(4, 2, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()

def show_reboot(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 2, "Are you sure you want to reboot? (y/n)")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord('y'):
        import subprocess
        subprocess.run(["reboot"])
    # If 'n' or other, do nothing, return

def show_change_sound(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "Change Sound Settings")
    stdscr.addstr(3, 2, "This will run change_sound.sh. Confirm? (y/n)")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord('y'):
        import subprocess
        try:
            subprocess.run(["bash", "change_sound.sh"], check=True)
            stdscr.addstr(5, 2, "Sound settings changed successfully.")
        except subprocess.CalledProcessError:
            stdscr.addstr(5, 2, "Error changing sound settings.")
    else:
        stdscr.addstr(5, 2, "Operation cancelled.")
    stdscr.addstr(7, 2, "Press any key to return to menu.")
    stdscr.refresh()
    stdscr.getch()

def show_after(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "Run After Script")
    stdscr.addstr(3, 2, "This will run after.sh. Confirm? (y/n)")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord('y'):
        import subprocess
        try:
            subprocess.run(["bash", "after.sh"], check=True)
            stdscr.addstr(5, 2, "After script executed successfully.")
        except subprocess.CalledProcessError:
            stdscr.addstr(5, 2, "Error executing after script.")
    else:
        stdscr.addstr(5, 2, "Operation cancelled.")
    stdscr.addstr(7, 2, "Press any key to return to menu.")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    if curses.can_change_color():
        curses.init_color(8, 1000, 1000, 500)  # Light yellow
        curses.init_pair(1, curses.COLOR_BLACK, 8)
    else:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    selected_idx = 0

    while True:
        draw_menu(stdscr, selected_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(MENU_ITEMS) - 1:
            selected_idx += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            selected = MENU_ITEMS[selected_idx]
            if selected == "System Info":
                show_system_info(stdscr)
            elif selected == "Install Modules":
                show_install_modules(stdscr)
            elif selected == "Change Sound":
                show_change_sound(stdscr)
            elif selected == "After":
                show_after(stdscr)
            elif selected == "ZFS Install":
                show_zfs_install(stdscr)
            elif selected == "Web Install":
                show_web_install(stdscr)
            elif selected == "SNMP Install":
                show_snmp_install(stdscr)
            elif selected == "First Firmware Install":
                show_first_firmware_install(stdscr)
            elif selected == "Network Setting":
                show_network_setting(stdscr)
            elif selected == "Reboot":
                show_reboot(stdscr)
            elif selected == "Exit":
                break

if __name__ == "__main__":
    curses.wrapper(main)