# ESP-NOW Accelerometer + Ambient Sensors — Plan

## Architecture

```
[Accelerometer Sender] --ESP-NOW--> [Receiver] --> Serial monitor
[Ambient Sender]       --ESP-NOW--> [Receiver] --> Serial monitor
     (MPU6050)                       (1 board)      (1 USB cable)
     (BME280+3xDS18B20)
```

- 3 boards total, 1 USB cable (plugged into receiver only)
- Both senders are headless on the evaporator, printing to local Serial
- Receiver prints both data streams to Serial via USB
- Send rate: 3 seconds for all

## Shared Data Struct

```c
typedef struct {
  uint8_t type;       // 0 = accel, 1 = ambient
  float data[6];      // payload (max 6 floats)
} EspNowPacket;
```

- Accel sender: type=0, data[0..2] = ax, ay, az
- Ambient sender: type=1, data[0..5] = temp, humid, counter, a_temp, b_temp, c_temp

## Calibration Offsets (hardcoded)

- AX_BIAS = -0.005124
- AY_BIAS = -0.265409
- AZ_BIAS = 0.379842

## ESP-NOW Config

- Both senders scan for SSID "PLDTHOMEFIBRd2228" for channel detection
- Receiver MAC: 0x14, 0x63, 0x93, 0x8C, 0xFC, 0x78
- Both sender MACs added as peers on receiver

## Files to Create

| File | Purpose |
|------|---------|
| `accel_sender/accel_sender.ino` | MPU6050 ESP-NOW sender |
| `ambient_sender/ambient_sender.ino` | BME280+DS18B20 ESP-NOW sender |
| `receiver/receiver.ino` | Combined ESP-NOW receiver -> Serial |

## Flash Procedure (1 cable)

1. Flash accel_sender onto board A -> disconnect
2. Flash ambient_sender onto board B -> disconnect
3. Flash receiver onto board C -> keep connected for serial monitoring
4. Open Serial Monitor at 115200 on board C
5. Power on boards A and B with phone chargers or power banks
