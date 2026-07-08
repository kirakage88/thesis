#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

const int NUM_SAMPLES = 200;
const float GRAVITY = 9.81;

float ax_bias, ay_bias, az_bias;
float gx_bias, gy_bias, gz_bias;

void collectSamples(float &ax, float &ay, float &az,
                    float &gx, float &gy, float &gz) {
  ax = ay = az = gx = gy = gz = 0;

  Serial.println(F("ax_raw,ay_raw,az_raw,gx_raw,gy_raw,gz_raw"));

  for (int i = 0; i < NUM_SAMPLES; i++) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    ax += a.acceleration.x;
    ay += a.acceleration.y;
    az += a.acceleration.z;
    gx += g.gyro.x;
    gy += g.gyro.y;
    gz += g.gyro.z;

    Serial.print(a.acceleration.x, 6); Serial.print(F(","));
    Serial.print(a.acceleration.y, 6); Serial.print(F(","));
    Serial.print(a.acceleration.z, 6); Serial.print(F(","));
    Serial.print(g.gyro.x, 6); Serial.print(F(","));
    Serial.print(g.gyro.y, 6); Serial.print(F(","));
    Serial.println(g.gyro.z, 6);

    delay(5);
  }

  ax /= NUM_SAMPLES;
  ay /= NUM_SAMPLES;
  az /= NUM_SAMPLES;
  gx /= NUM_SAMPLES;
  gy /= NUM_SAMPLES;
  gz /= NUM_SAMPLES;
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println(F("MPU6050 Calibration"));
  Serial.println(F("Keep the sensor perfectly still during calibration."));
  Serial.println();

  if (!mpu.begin()) {
    Serial.println(F("Sensor init failed"));
    while (1) yield();
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.print(F("Collecting "));
  Serial.print(NUM_SAMPLES);
  Serial.println(F(" raw samples for calibration..."));
  delay(1000);

  float ax, ay, az, gx, gy, gz;
  collectSamples(ax, ay, az, gx, gy, gz);

  gx_bias = gx;
  gy_bias = gy;
  gz_bias = gz;

  ax_bias = ax;
  ay_bias = ay;
  az_bias = az - GRAVITY;

  Serial.println();
  Serial.println(F("=== CALIBRATION RESULTS ==="));
  Serial.print(F("Gyro bias (rad/s): "));
  Serial.print(gx_bias, 6); Serial.print(F(", "));
  Serial.print(gy_bias, 6); Serial.print(F(", "));
  Serial.println(gz_bias, 6);

  Serial.print(F("Accel offset (m/s^2): "));
  Serial.print(ax_bias, 6); Serial.print(F(", "));
  Serial.print(ay_bias, 6); Serial.print(F(", "));
  Serial.println(az_bias, 6);
  Serial.println();

  Serial.print(F("Copy these into your sketch:"));
  Serial.println();
  Serial.print(F("const float gx_bias = "));
  Serial.print(gx_bias, 6);
  Serial.println(F(";"));
  Serial.print(F("const float gy_bias = "));
  Serial.print(gy_bias, 6);
  Serial.println(F(";"));
  Serial.print(F("const float gz_bias = "));
  Serial.print(gz_bias, 6);
  Serial.println(F(";"));
  Serial.print(F("const float ax_bias = "));
  Serial.print(ax_bias, 6);
  Serial.println(F(";"));
  Serial.print(F("const float ay_bias = "));
  Serial.print(ay_bias, 6);
  Serial.println(F(";"));
  Serial.print(F("const float az_bias = "));
  Serial.print(az_bias, 6);
  Serial.println(F(";"));
  Serial.println();

  Serial.println(F("=== CALIBRATED READINGS ==="));
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float ax = a.acceleration.x - ax_bias;
  float ay = a.acceleration.y - ay_bias;
  float az = a.acceleration.z - az_bias;
  float gx = g.gyro.x - gx_bias;
  float gy = g.gyro.y - gy_bias;
  float gz = g.gyro.z - gz_bias;

  Serial.print(F("Accel: "));
  Serial.print(ax, 3); Serial.print(F(", "));
  Serial.print(ay, 3); Serial.print(F(", "));
  Serial.print(az, 3); Serial.print(F(" | Gyro: "));
  Serial.print(gx, 3); Serial.print(F(", "));
  Serial.print(gy, 3); Serial.print(F(", "));
  Serial.println(gz, 3);

  delay(1000);
}
