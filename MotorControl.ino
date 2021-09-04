//Initializing LED Pin

int EN_A = PA0;      //Enable pin for first motor
int IN1 = PC15;       //control pin for first motor
int IN2 = PC14;       //control pin for first motor

int percentage = 0;
int pwm = 0;

//Communication
const int numChars = 32;
char receivedChars[numChars];
String receivedData = "";
boolean newData = false;

void setup() {

  Serial.begin(9600);
  pinMode(EN_A, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

}

void loop() {
    recvWithStartEndMarkers();
    percentage = getNewData();

    setSpeed(percentage);
}
 
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

int getNewData() {
    if (newData == true) {
        receivedData = receivedChars;
        newData = false;
    }
    return receivedData.toInt();
}

void setSpeed(int percentage)
{
  pwm = map(percentage, 0, 100, 0, 255);
  analogWrite(EN_A, pwm);
}
  
