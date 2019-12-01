/*
 * Authors:
 * Canute Rolin Cardoza
 * Akash Murthy
 * Reshma P Roy
 * Akhil Khubchandani
 */



/* G1 = straight / far turn (left or right)
 * G2 = direct turn (right or left)
 * G3 = U - Turn
*/

#include <SoftwareSerial.h>
SoftwareSerial mySerial(13,12);  // (Rx,Tx  > Tx,Rx)

char incomingByte;
String inputString;

class Signal
{
  public:
  int RLED;
  int r_state;
 
  int YLED;
  int y_state;
 
  int GLED;
  int g_state;
  int G2LED;
  int G3LED;
  int green_on;
  int red_on;

  unsigned long prev_red;
  unsigned long prev_green;
 
  Signal(int rpin, int ypin, int g1pin,int g2pin, int g3pin, int r_on,int g_on)
  {
    RLED=rpin;
    YLED=ypin;
    GLED=g1pin;
    G2LED=g2pin;
    G3LED=g3pin;
    pinMode(RLED,OUTPUT);
    pinMode(YLED,OUTPUT);
    pinMode(GLED,OUTPUT);
    pinMode(G2LED,OUTPUT);
    pinMode(G3LED,OUTPUT);

    green_on=g_on;
     
    r_state=LOW;
    y_state=LOW;
    g_state=LOW;
  }
};


Signal s3(30,28,26,24,22,5000,5000);
Signal s2(41,39,37,35,33,5000,5000);
Signal s1(45,47,49,51,53,5000,5000);
Signal arr[]={s1,s2,s3};

void off(int val, int sig)
{
  if(sig==1)
  {
    arr[val].g_state=LOW;
    digitalWrite(arr[val].GLED,arr[val].g_state);
    digitalWrite(arr[val].G2LED,arr[val].g_state);
    digitalWrite(arr[val].G3LED,arr[val].g_state);
  }
  else
  {
    arr[val].r_state=LOW;
    digitalWrite(arr[val].RLED,arr[val].r_state);
  }
}

void red(int val)
{
  arr[val].r_state=HIGH;
  digitalWrite(arr[val].RLED,arr[val].r_state);
}

void green(int val)
{
  arr[val].r_state=LOW;
  arr[val].g_state=HIGH;
  digitalWrite(arr[val].GLED,arr[val].g_state);
  digitalWrite(arr[val].G2LED,arr[val].g_state);
  digitalWrite(arr[val].G3LED,arr[val].g_state);
}

void yellow_single(int sig)
{
  arr[sig].y_state=HIGH;
  digitalWrite(arr[sig].YLED,arr[sig].y_state);
  delay(500);
  arr[sig].y_state=LOW;
  digitalWrite(arr[sig].YLED,arr[sig].y_state);
}

void yellow(int rtog, int gtor)
{
  arr[rtog].y_state=HIGH;
  arr[gtor].y_state=HIGH;
  off(rtog,0);
  off(gtor,1);
  digitalWrite(arr[rtog].YLED,arr[rtog].y_state);
  digitalWrite(arr[gtor].YLED,arr[gtor].y_state);
  delay(500);
  arr[rtog].y_state=LOW;
  arr[gtor].y_state=LOW;
  digitalWrite(arr[rtog].YLED,arr[rtog].y_state);
  digitalWrite(arr[gtor].YLED,arr[gtor].y_state);
}


void change(int grn, int r, bool first)
{
  if(r==-1)
  {
    for(int i=0;i<sizeof(arr)/sizeof(Signal);i++)
    {
      if(i==2 && !first)
        break;
      arr[i].r_state=HIGH;
      digitalWrite(arr[i].RLED,arr[i].r_state);
    }
    if(first)
    {
      delay(1000);
    }
   
    arr[grn].g_state=HIGH;
    arr[grn].y_state=HIGH;
    arr[grn].r_state=LOW;
    if(!first)
    {
      arr[2].g_state=LOW;
      digitalWrite(arr[2].GLED,arr[2].g_state);
      digitalWrite(arr[2].G2LED,arr[2].g_state);
      digitalWrite(arr[2].G3LED,arr[2].g_state);
    }
    digitalWrite(arr[grn].RLED,arr[grn].r_state);
    digitalWrite(arr[grn].YLED,arr[grn].y_state);
    if(!first)
    {
      arr[2].y_state=HIGH;
      digitalWrite(arr[2].YLED,arr[2].y_state);
    }
    delay(500);
    arr[grn].y_state=LOW;
    digitalWrite(arr[grn].YLED,arr[grn].y_state);
    if(!first)
    {
      arr[2].y_state=LOW;
      digitalWrite(arr[2].YLED,arr[2].y_state);
      arr[2].r_state=HIGH;
      digitalWrite(arr[2].RLED,arr[2].r_state);
    }
    digitalWrite(arr[grn].GLED,arr[grn].g_state);
    digitalWrite(arr[grn].G2LED,arr[grn].g_state);
    digitalWrite(arr[grn].G3LED,arr[grn].g_state);
   
  }
  else
  {
    yellow(grn,r);
    green(grn);
    red(r);
  }
}

bool first_iter=1;
void normal()
{
  int i=0;
  int siz=sizeof(arr)/sizeof(Signal);
  for(i;i<siz;i++)
  {
    if(i==0)
    {
      change(i,-1,first_iter);
      delay(arr[i].green_on);
      first_iter=0;
    }
    else
    {
      change(i,i-1,first_iter);
      delay(arr[i].green_on);
    }
    if(Serial.available() > 0){return;}
  }
}


//the way this works: first parameter is the signal from which the ambulance passes. second is the parameter to which it goes
//override is a keyword, so overtake...
void overtake_3(int signo, int dir)
{
  int siz=sizeof(arr)/sizeof(Signal);
  if(signo==1)
  {
    for(int i;i<siz;i++)
    {
      digitalWrite(arr[i].RLED,LOW);
      digitalWrite(arr[i].GLED,LOW);
      digitalWrite(arr[i].G2LED,LOW);
      digitalWrite(arr[i].G3LED,LOW);
    }
    if(dir==1)
    {
      for(int i=0;i<siz;i++)
      {
        digitalWrite(arr[i].G3LED,HIGH);
      }
    }
    else if(dir==2)
    {
      digitalWrite(arr[0].GLED,HIGH);
      digitalWrite(arr[1].G2LED,HIGH);
      digitalWrite(arr[1].GLED,HIGH);
      digitalWrite(arr[2].RLED,HIGH);
    }
    else if(dir==3)
    {
      digitalWrite(arr[0].G2LED,HIGH);
      digitalWrite(arr[2].GLED,HIGH);
      digitalWrite(arr[1].RLED,HIGH);
    }
  }
  if(signo==2)
  {
    for(int i;i<siz;i++)
    {
      digitalWrite(arr[i].RLED,LOW);
      digitalWrite(arr[i].GLED,LOW);
      digitalWrite(arr[i].G2LED,LOW);
      digitalWrite(arr[i].G3LED,LOW);
    }
    if(dir==1)
    {
      digitalWrite(arr[1].G2LED,HIGH);
      digitalWrite(arr[0].GLED,HIGH);
      digitalWrite(arr[2].RLED,HIGH);
    }
    else if(dir==2)
    {
      for(int i=0;i<siz;i++)
      {
        digitalWrite(arr[i].G3LED,HIGH);
      }
    }
    else if(dir==3)
    {
      digitalWrite(arr[1].GLED,HIGH);
      digitalWrite(arr[1].G2LED,HIGH);
      digitalWrite(arr[0].GLED,HIGH);
      digitalWrite(arr[2].RLED,HIGH);
    }
  }
  if(signo==3)
  {
    for(int i;i<siz;i++)
    {
      digitalWrite(arr[i].RLED,LOW);
      digitalWrite(arr[i].GLED,LOW);
      digitalWrite(arr[i].G2LED,LOW);
      digitalWrite(arr[i].G3LED,LOW);
    }
    if(dir==1)
    {
      digitalWrite(arr[2].GLED,HIGH);
      digitalWrite(arr[0].GLED,HIGH);
      digitalWrite(arr[1].GLED,HIGH);
    }
    if(dir==2)
    {
      digitalWrite(arr[2].G2LED,HIGH);
      digitalWrite(arr[2].GLED,HIGH);
      digitalWrite(arr[1].GLED,HIGH);
      digitalWrite(arr[0].RLED,HIGH);
    }
    if(dir==3)
    {
      for(int i=0;i<siz;i++)
      {
        digitalWrite(arr[i].G3LED,HIGH);
      }
    }
  }
}

int trigger=0;
void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);

  while(!mySerial.available()){
        mySerial.println("AT");
        delay(1000);
        Serial.println("Connecting...");
        }
      Serial.println("Connected!");  
      mySerial.println("AT+CMGF=1");  //Set SMS to Text Mode
      delay(1000);  
      mySerial.println("AT+CNMI=1,2,0,0,0");  //Procedure to handle newly arrived messages(command name in text: new message indications to TE)
      delay(1000);
      mySerial.println("AT+CMGL=\"REC UNREAD\""); // Read Unread Messages
}

void loop()
{
  if(mySerial.available()){
      delay(100);

      // Serial Buffer
      while(mySerial.available()){
        incomingByte = mySerial.read();
        inputString += incomingByte;
        }

        delay(10);      

        Serial.println(inputString);      

        delay(50);

        //Delete Messages & Save Memory
        if (inputString.indexOf("OK") == -1){
        mySerial.println("AT+CMGDA=\"DEL ALL\"");

        delay(1000);}

        inputString = "";
  }
 
  if(!trigger)
  {
    normal();
  }
  else if(trigger==1)
  {
    overtake_3(1,1);
  }
  else if(trigger==2)
  {
    overtake_3(1,2);
  }
  else if(trigger==3)
  {
    overtake_3(1,3);
  }
  else if(trigger==4)
  {
    overtake_3(2,1);
  }else if(trigger==5)
  {
    overtake_3(2,2);
  }else if(trigger==6)
  {
    overtake_3(2,3);
  }else if(trigger==7)
  {
    overtake_3(3,1);
  }
  else if(trigger==8)
  {
    overtake_3(3,2);
  }else if(trigger==9)
  {
    overtake_3(3,3);
  }
  while(Serial.available() > 0 )
  {
    String str = Serial.readString();
    if(str.indexOf("o11") > -1)
    {trigger=1;}
    else if(str.indexOf("o12")>-1)
    {trigger=2;}
    else if(str.indexOf("o13")>-1)
    {trigger=3;}
    else if(str.indexOf("o21")>-1)
    {trigger=4;}
    else if(str.indexOf("o22")>-1)
    {trigger=5;}
    else if(str.indexOf("o23")>-1)
    {trigger=6;}
    else if(str.indexOf("o31")>-1)
    {trigger=7;}
    else if(str.indexOf("o32")>-1)
    {trigger=8;}
    else if(str.indexOf("o33")>-1)
    {trigger=9;}
    else if(str.indexOf("break") > -1)
    {
      for(int i=0;i<(sizeof(arr)/sizeof(Signal));i++)
      {
        digitalWrite(arr[i].GLED,LOW);
        digitalWrite(arr[i].G2LED,LOW);
        digitalWrite(arr[i].G3LED,LOW);
      }
      trigger=0;
    }
  }
}
