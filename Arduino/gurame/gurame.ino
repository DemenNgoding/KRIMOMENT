#define aVIN 6 // 10// KANAN DEPAN
#define aIN1 47 // 28
#define aIN2 45 // 26

#define bVIN 5 // 11 // BELAKANG
#define bIN1 39 // 30
#define bIN2 41 // 32

#define cVIN 7 // 9 // Pengatur kecepatan motor A KIRI DEPANlastShoot
#define cIN1 33 // 24 // Pengatur arah putar motor A 
#define cIN2 35 // 22 // Pengatur arah putar motor A

#define drib1VIN 12
#define drib1IN1 35
#define drib1IN2 37

#define drib2VIN 13
#define drib2IN1 41
#define drib2IN2 39

#define shooter 48
#define charger 46

int pwmRoda = 40, pwmDrible = 200;
String action = "o";

int time = 0;

void setup()
{
    Serial.begin(2000000);

    pinMode(aVIN, OUTPUT);
    pinMode(bVIN, OUTPUT);
    pinMode(cVIN, OUTPUT);

    pinMode(aIN1, OUTPUT);
    pinMode(bIN1, OUTPUT);
    pinMode(cIN1, OUTPUT);

    pinMode(aIN2, OUTPUT);
    pinMode(bIN2, OUTPUT);
    pinMode(cIN2, OUTPUT);

    pinMode(drib1VIN, OUTPUT);
    pinMode(drib1IN1, OUTPUT);
    pinMode(drib1IN2, OUTPUT);

    pinMode(drib2VIN, OUTPUT);
    pinMode(drib2IN1, OUTPUT);
    pinMode(drib2IN2, OUTPUT);

    pinMode(shooter, OUTPUT);
    digitalWrite(shooter, HIGH);
}

void loop() {
  // Serial.println("maju");
  // maju(1000);

  // Serial.println("wiaitting");
  // parking(2000);

  // timing charger

    if (Serial.available())
    {
        action = Serial.readStringUntil('\n');

        if (action == "TEST_SERIAL")
        {
            digitalWrite(LED_BUILTIN, HIGH);
            delay(5000);
            digitalWrite(LED_BUILTIN, LOW);
        }

        Serial.println(action);
    }

    if (action == "w")
    {
        maju();
    }
    else if (action == "a")
    {
        kiri();
    }
    else if (action == "s")
    {
        mundur();
    }
    else if (action == "d")
    {
        kanan();
    }
    else if (action == "q")
    {
        putarkiri();
    }
    else if (action == "e")
    {
        putarkanan();
    }
    else if (action == "y")
    {
        drib_on_backward();
    }
    else if (action == "n")
    {
        drib_off();
    }
    else if (action == "=")
    {
        tendang();
    }
    else if (action == "o")
    {
        parking();
    }
    else if (action == "TEST_A")
    {
        testA();
        Serial.println("Motor A");
    }
    else if (action == "TEST_B")
    {
        testB();
        Serial.println("Motor B");
    }
    else if (action == "TEST_C")
    {
        testC();
        Serial.println("Motor C");
    }
    else
    {
        parking();
        Serial.println("Unknown Input Robot Stopping....");
        delay(1000);
    }

    if (millis() - time > 8000)
    {
        digitalWrite(charger, LOW);
    }
    else
    {
        digitalWrite(charger, HIGH);
    }
}

void tendang()
{
    digitalWrite(shooter, LOW);
    delay(1500);
    digitalWrite(shooter, HIGH);
    action = "o";
}

void testA()
{
    Serial.println("jalan");
    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, HIGH);
    analogWrite(aVIN, pwmRoda);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, LOW);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, LOW);
    analogWrite(cVIN, pwmRoda);
}

void testB()
{

    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, pwmRoda);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, LOW);
    analogWrite(cVIN, pwmRoda);
}

void testC()
{

    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, pwmRoda);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, LOW);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, pwmRoda);
}

void putarkiri()
{

    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, HIGH);
    analogWrite(aVIN, pwmRoda * 0.5);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, pwmRoda * 0.5);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, pwmRoda * 0.5);
}

void putarkanan()
{

    digitalWrite(aIN1, HIGH);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, pwmRoda * 0.5);

    digitalWrite(bIN1, HIGH);
    digitalWrite(bIN2, LOW);
    analogWrite(bVIN, pwmRoda * 0.5);

    digitalWrite(cIN1, HIGH);
    digitalWrite(cIN2, LOW);
    analogWrite(cVIN, pwmRoda * 0.5);
}

void kiri()
{

    digitalWrite(aIN1, HIGH);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, pwmRoda);

    digitalWrite(bIN1, HIGH);
    digitalWrite(bIN2, LOW);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, HIGH);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, pwmRoda);
}

void kanan()
{

    digitalWrite(aIN1, HIGH);
    digitalWrite(aIN2, HIGH);
    analogWrite(aVIN, pwmRoda);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, pwmRoda);
}

void brake()
{
    digitalWrite(aIN1, HIGH);
    digitalWrite(aIN2, HIGH);
    analogWrite(aVIN, 15);

    digitalWrite(bIN1, HIGH);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, 15);

    digitalWrite(cIN1, HIGH);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, 15);
}

void parking()
{
    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, 0);

    digitalWrite(bIN1, LOW);
    digitalWrite(bIN2, LOW);
    analogWrite(bVIN, 0);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, LOW);
    analogWrite(cVIN, 0);
}

void mundur()
{

    digitalWrite(aIN1, LOW);
    digitalWrite(aIN2, HIGH);
    analogWrite(aVIN, pwmRoda * 1.3);

    digitalWrite(bIN1, HIGH);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, pwmRoda);

    digitalWrite(cIN1, HIGH);
    digitalWrite(cIN2, LOW);
    analogWrite(cVIN, pwmRoda *1.3);
}

void maju()
{
    digitalWrite(aIN1, HIGH);
    digitalWrite(aIN2, LOW);
    analogWrite(aVIN, pwmRoda * 1.3);

    digitalWrite(bIN1, HIGH);
    digitalWrite(bIN2, HIGH);
    analogWrite(bVIN, pwmRoda * 1.3);

    digitalWrite(cIN1, LOW);
    digitalWrite(cIN2, HIGH);
    analogWrite(cVIN, pwmRoda * 1.3);
}

void drib_on_backward()
{
    digitalWrite(drib1IN1, HIGH);
    digitalWrite(drib1IN2, LOW);
    analogWrite(drib1VIN, pwmDrible);

    digitalWrite(drib2IN1, HIGH);
    digitalWrite(drib2IN2, LOW);
    analogWrite(drib2VIN, pwmDrible);
}

void drib_on_right()
{
    digitalWrite(drib1IN1, LOW);
    digitalWrite(drib1IN2, HIGH);
    analogWrite(drib1VIN, pwmDrible);

    digitalWrite(drib2IN1, HIGH);
    digitalWrite(drib2IN2, LOW);
    analogWrite(drib2VIN, pwmDrible * 1 / 8);
}

void drib_on_left()
{
    digitalWrite(drib1IN1, LOW);
    digitalWrite(drib1IN2, HIGH);
    analogWrite(drib1VIN, pwmDrible * 1 / 8);

    digitalWrite(drib2IN1, HIGH);
    digitalWrite(drib2IN2, LOW);
    analogWrite(drib2VIN, pwmDrible);
}

void drib_off()
{
    digitalWrite(drib1IN1, LOW);
    digitalWrite(drib1IN2, LOW);
    digitalWrite(drib1VIN, LOW);

    digitalWrite(drib2IN1, LOW);
    digitalWrite(drib2IN2, LOW);
    digitalWrite(drib2VIN, LOW);
}