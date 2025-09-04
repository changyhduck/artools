import curses
import os
import subprocess

def show_zfs_install(stdscr):
    curses.curs_set(0)
    # Get list of zfs*.sh files
    zfs_files = [f for f in os.listdir('.') if f.startswith('zfs') and f.endswith('.sh')]
    if not zfs_files:
        stdscr.clear()
        stdscr.addstr(2, 2, "No zfs*.sh files found. Press any key...")
        stdscr.refresh()
        stdscr.getch()
        return
    current_idx = 0
    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, "Select a ZFS script to run:")
        for i, f in enumerate(zfs_files):
            attr = curses.A_REVERSE if i == current_idx else curses.A_NORMAL
            stdscr.addstr(4 + i, 2, f, attr)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
        elif key == curses.KEY_DOWN and current_idx < len(zfs_files) - 1:
            current_idx += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            selected_file = zfs_files[current_idx]
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
