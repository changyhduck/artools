import curses
import platform
import os
import requests
import install_module
import install_zfs
import install_web

MENU_ITEMS = ["System Info", "Install Modules", "Change Sound", "After", "ZFS Install", "Web Install", "Network Setting", "Reboot", "Exit"]

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

def show_zfs_install(stdscr):
    install_zfs.show_zfs_install(stdscr)

def show_web_install(stdscr):
    install_web.show_web_install(stdscr)

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
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
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
            elif selected == "Network Setting":
                show_network_setting(stdscr)
            elif selected == "Reboot":
                show_reboot(stdscr)
            elif selected == "Exit":
                break

if __name__ == "__main__":
    curses.wrapper(main)