import curses
import subprocess
import json
import os

def show_web_install(stdscr):
    curses.curs_set(0)
    # Load Web.json directly
    try:
        with open('Web.json', 'r') as f:
            modules = json.load(f)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(2, 2, f"Error loading Web.json: {e}. Press any key...")
        stdscr.refresh()
        stdscr.getch()
        return
    selected = [mod['default_selected'] for mod in modules]
    current_idx = 0
    button_selected = 0  # 0 for Install, 1 for Exit

    while True:
        stdscr.clear()
        # Draw checkboxes
        for i, mod in enumerate(modules):
            check = "[X]" if selected[i] else "[ ]"
            attr = curses.A_REVERSE if i == current_idx else curses.A_NORMAL
            stdscr.addstr(2 + i, 2, f"{check} {mod['name']}", attr)
        # Draw buttons
        install_attr = curses.A_REVERSE if button_selected == 0 else curses.A_NORMAL
        exit_attr = curses.A_REVERSE if button_selected == 1 else curses.A_NORMAL
        stdscr.addstr(2 + len(modules) + 2, 2, "[Install]", install_attr)
        stdscr.addstr(2 + len(modules) + 2, 12, "[Exit]", exit_attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            if current_idx > 0:
                current_idx -= 1
            elif button_selected == 0:
                current_idx = len(modules) - 1  # Wrap to last checkbox
        elif key == curses.KEY_DOWN:
            if current_idx < len(modules) - 1:
                current_idx += 1
            else:
                button_selected = 0  # Move to buttons
        elif key == ord(' '):
            if current_idx < len(modules):
                selected[current_idx] = not selected[current_idx]
        elif key == curses.KEY_LEFT:
            if button_selected > 0:
                button_selected -= 1
        elif key == curses.KEY_RIGHT:
            if button_selected < 1:
                button_selected += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            if button_selected == 0:  # Install
                selected_modules = [mod for i, mod in enumerate(modules) if selected[i]]
                if selected_modules:
                    stdscr.clear()
                    stdscr.addstr(2, 2, f"Installing: {', '.join([m['name'] for m in selected_modules])}")
                    stdscr.refresh()
                    success = True
                    for mod in selected_modules:
                        try:
                            if mod['is_group']:
                                subprocess.run(["dnf", "group", "install", "-y", mod['name']], check=True)
                            else:
                                subprocess.run(["dnf", "install", "-y", mod['name']], check=True)
                        except subprocess.CalledProcessError as e:
                            stdscr.addstr(4, 2, f"Error installing {mod['name']}: {e}. Press any key...")
                            success = False
                            break
                    if success:
                        stdscr.addstr(4, 2, "Installation successful. Press any key...")
                    stdscr.refresh()
                    stdscr.getch()
                break
            elif button_selected == 1:  # Exit
                break
