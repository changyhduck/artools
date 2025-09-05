import curses
import subprocess
import json
import os

def show_install_modules(stdscr):
    curses.curs_set(0)
    # Get list of json files
    json_files = [f for f in os.listdir('.') if f.startswith('Acro') and f.endswith('.json')]
    if not json_files:
        stdscr.clear()
        stdscr.addstr(2, 2, "No JSON files found. Press any key...")
        stdscr.refresh()
        stdscr.getch()
        return
    current_idx = 0
    button_selected = 0  # 0 for Install, 1 for Exit
    selected_file = None
    while selected_file is None:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        if 4 + len(json_files) + 2 >= h:
            stdscr.addstr(2, 2, "Too many JSON files to display. Press any key...")
            stdscr.refresh()
            stdscr.getch()
            return
        stdscr.addstr(2, 2, "Select a JSON file:")
        for i, f in enumerate(json_files):
            attr = curses.A_REVERSE if i == current_idx else curses.A_NORMAL
            stdscr.addstr(4 + i, 2, f, attr)
        # Draw buttons
        install_attr = curses.A_REVERSE if button_selected == 0 else curses.A_NORMAL
        exit_attr = curses.A_REVERSE if button_selected == 1 else curses.A_NORMAL
        stdscr.addstr(4 + len(json_files) + 2, 2, "[Install]", install_attr)
        stdscr.addstr(4 + len(json_files) + 2, 12, "[Exit]", exit_attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            if current_idx > 0:
                current_idx -= 1
            elif button_selected == 0:
                current_idx = len(json_files) - 1  # Wrap to last file
        elif key == curses.KEY_DOWN:
            if current_idx < len(json_files) - 1:
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
                selected_file = json_files[current_idx]
            elif button_selected == 1:  # Exit
                return
    # Load the selected file
    try:
        with open(selected_file, 'r') as f:
            modules = json.load(f)
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(2, 2, f"Error loading {selected_file}: {e}. Press any key...")
        stdscr.refresh()
        stdscr.getch()
        return
    # Derive the script name
    script_name = selected_file.replace('.json', '.sh')
    selected = [mod['default_selected'] for mod in modules]
    current_idx = 0
    button_selected = 0  # 0 for Install, 1 for Exit

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        if 2 + len(modules) + 2 >= h:
            stdscr.addstr(2, 2, "Terminal too small to display all modules. Resize and try again.")
            stdscr.refresh()
            stdscr.getch()
            return
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
                        stdscr.clear()
                        stdscr.addstr(2, 2, f"Installation successful. Execute {script_name}? (y/n)")
                        stdscr.refresh()
                        key = stdscr.getch()
                        if key == ord('y'):
                            try:
                                subprocess.run(["bash", script_name], check=True)
                                stdscr.addstr(4, 2, "Script executed successfully. Press any key...")
                            except subprocess.CalledProcessError as e:
                                stdscr.addstr(4, 2, f"Error executing script: {e}. Press any key...")
                        else:
                            stdscr.addstr(4, 2, "Press any key...")
                        stdscr.refresh()
                        stdscr.getch()
                break
            elif button_selected == 1:  # Exit
                break
