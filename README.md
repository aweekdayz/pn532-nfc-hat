# Raspberry Pi NFC Music Player

This project turns a Raspberry Pi into a physical music player. NFC-tagged album cards select music, a rotary encoder controls volume and playback, and an infrared sensor detects the position of a model tonearm.

## What I Built

- Read album-card UIDs with a PN532 NFC module connected over SPI.
- Mapped each UID to album metadata and used MPD/MPC to load and play the matching album.
- Added a KY-040 rotary encoder for volume and play/pause control.
- Added an infrared sensor and a small state machine so lifting or returning the tonearm changes playback behavior.
- Wrote separate hardware tests before combining the components in `main_app.py`.

## Hardware and Software

- Raspberry Pi 4B
- Waveshare PN532 NFC HAT
- KY-040 rotary encoder
- Infrared sensor
- Linux, Python, RPi.GPIO, MPD/MPC, and ALSA

## Repository Guide

- `main_app.py` - integrated application and state machine
- `nfc_music_player.py` - NFC-to-album playback prototype
- `get_id.py` and `get_multi-id.py` - NFC tag registration helpers
- `test_encoder*.py`, `test_sensor.py`, and `volume_control.py` - component tests
- `pn532/` and `example_*.py` - PN532 library and examples retained from the original Waveshare-compatible implementation

## Project Scope

The PN532 driver and example structure come from a Waveshare-compatible open-source implementation and retain the original license and attribution. My project-specific work is the physical music-player integration, configuration, testing, and control logic.

I used AI coding assistance for parts of the project and personally assembled, configured, tested, and iterated on the working system.
