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

## Attribution and AI Assistance

The PN532 driver and example structure are based on existing Waveshare-compatible open-source code and should retain the original license and attribution. My project-specific work is the physical music-player integration, configuration, testing, and control logic.

I used AI coding assistance while developing and debugging parts of the project. I assembled the hardware, adapted the code to the devices, tested the behavior on the Raspberry Pi, and iterated on the working system.

## Safety and Privacy

The album-card identifiers shown in the code are used only for this personal media interface. No authentication secrets or access credentials should be stored in the repository.
