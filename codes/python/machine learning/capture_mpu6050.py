import serial
import serial.tools.list_ports
import sys
import time
from datetime import datetime


def list_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found")
        sys.exit(1)
    print("Available ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p.device} - {p.description}")
    return ports


def select_port(ports):
    while True:
        try:
            idx = int(input("Select port number: "))
            if 0 <= idx < len(ports):
                return ports[idx].device
        except ValueError:
            pass
        print("Invalid selection")


def main():
    ports = list_ports()
    port = select_port(ports)

    ser = serial.Serial(port, 115200, timeout=10)
    ser.reset_input_buffer()

    print(f"\nConnected to {port}")
    print("Waiting for CSV header...")

    header = None
    samples = []
    capture_start = None
    results_start = False

    while True:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if not line:
            continue

        if line.startswith("ax_raw,ay_raw,az_raw,gx_raw,gy_raw,gz_raw"):
            header = line.split(",")
            samples = []
            capture_start = time.time()
            print("Capture started (reading 200 samples)...")
            continue

        if header is not None and len(samples) < 200:
            try:
                vals = [float(v) for v in line.split(",")]
                if len(vals) == 6:
                    samples.append(vals)
                    if len(samples) % 50 == 0:
                        print(f"  {len(samples)} samples...")
            except ValueError:
                pass

            if len(samples) == 200:
                elapsed = time.time() - capture_start
                print(f"\nCaptured {len(samples)} samples in {elapsed:.1f}s")

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mpu6050_raw_{ts}.csv"
                with open(filename, "w") as f:
                    f.write(",".join(header) + "\n")
                    for s in samples:
                        f.write(",".join(f"{v:.6f}" for v in s) + "\n")
                print(f"Saved to {filename}")

                print("\n--- Calibration results ---")

        if "=== CALIBRATION RESULTS ===" in line:
            results_start = True
            continue

        if results_start:
            if "=== CALIBRATED READINGS ===" in line:
                break
            print(f"  {line}")

    ser.close()


if __name__ == "__main__":
    main()
