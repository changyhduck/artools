#!/bin/bash
systemctl --user --now disable pipewire.socket pipewire-pulse.socket pipewire pipewire-pulse wireplumber
dnf -y swap pipewire-pulseaudio pulseaudio --allowerasing
dnf -y install pulseaudio-utils.x86_64
reboot
