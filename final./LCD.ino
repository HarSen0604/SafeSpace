#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;
#include <TouchScreen.h>
#define MINPRESSURE 100
#define MAXPRESSURE 2000
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
// ALL Touch panels and wiring is DIFFERENT
// copy-paste results from TouchScreen_Calibr_native.ino
const int XP = 6, XM = A2, YP = A1, YM = 7; //ID=0x9341

const int TS_LEFT = 910, TS_RT = 169, TS_TOP = 900, TS_BOT = 180;

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

Adafruit_GFX_Button on_btn;
Adafruit_GFX_Button SOS_btn;

int pixel_x, pixel_y;     //Touch_getXY() updates global vars
int button;
bool Touch_getXY(void)
{
    TSPoint p = ts.getPoint();
    pinMode(YP, OUTPUT);      //restore shared pins
    pinMode(XM, OUTPUT);
    digitalWrite(YP, HIGH);   //because TFT control pins
    digitalWrite(XM, HIGH);
    bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
    if (pressed) {
        Serial.println("P.X:"+String(p.x));
        Serial.println("P.Y:"+String(p.y));
        pixel_x = map(p.x, TS_RT, TS_LEFT,  0, tft.width()); //.kbv makes sense to me
        pixel_y = map(p.y, TS_TOP, TS_BOT, 0, tft.height());
        Serial.println("X:"+String(pixel_x));
        Serial.println("Y:"+String(pixel_y));
        Serial.println("");
        tft.setTextColor(WHITE, BLACK);
    }
    if (p.y>960 && p.y<1000 && button == 1){
        button = 0;
    }
    if (p.y>-26 && p.y<-23 && button == 0){
        button = 1;
    }
    if(p.y>900 && p.y<915){
      button = 2;
    }
    //   tft.drawLine(160, 239,x,y, WHITE);
    if(pressed){
          tft.setTextSize(2);
       
          tft.setCursor(110,45);
          if (button == 0)
            tft.print("Start registered");
          else if(button == 2)
            tft.print("SOS registered");
          delay(1000);
          // Clear the area where the text was printed
          int textX = 110; // Example position where the text was printed
          int textY = 45;
          int textWidth = 200; // Example width and height of the printed text
          int textHeight = 20;
          uint16_t backgroundColor = BLACK; // Example background color

          // Clear the area where the text was printed
          tft.fillRect(textX, textY, textWidth, textHeight, backgroundColor);
    }
    delay(200);
    return pressed;
}


float i=0;
int randomvalue=-90;
int returnx=0;
float angle,x,y;
bool down;
unsigned long old =0;
unsigned long current =0;
long interval=0;
void setup(void)
{
    Serial.begin(9600);
    uint16_t ID = tft.readID();
    Serial.print("TFT ID = 0x");
    Serial.println(ID, HEX);
    Serial.println("Calibrate for your Touch Panel");
    if (ID == 0xD3D3) ID = 0x9486; // write-only shield
    tft.begin(ID);
    tft.setRotation(3);            //PORTRAIT
    tft.setTextSize(3);
    tft.fillScreen(BLACK);
    on_btn.initButton(&tft,  40, 70, 80, 50, WHITE, MAGENTA, WHITE, "Start", 2);
    SOS_btn.initButton(&tft,  40, 200, 80, 50, WHITE, RED, WHITE, "SOS", 2);
    
    on_btn.drawButton(false);
    SOS_btn.drawButton(false);
    
    i=randomvalue;
    
   tft.setTextSize(2);
   tft.fillRect(0,0,320,25,GREEN);
   tft.setTextColor(BLACK);
   tft.setCursor(0,5);
   tft.print("     Watch (beta 0.1)   ");
  //tft.setTextColor(YELLOW,BLACK);
}

void loop(void)
{
   current =millis();
   if( (current-old)/100>2)
   returnx=0;
    
   down = Touch_getXY();
    if (down)
    {
            on_btn.press(down && on_btn.contains(pixel_x, pixel_y));
            SOS_btn.press(down && on_btn.contains(pixel_x, pixel_y));
            Serial.print("Button: ");
            Serial.println(button);
        
            if (on_btn.justPressed() || button == 0 ) 
            {
              //  on_btn.drawButton(true);
               Serial.println("Start Button Pressed");
               on_btn.press(false);
               //on_btn.drawButton(false);
            }
            if (SOS_btn.justPressed() || button == 2) 
            {
              //  SOS_btn.drawButton(true);
               Serial.println("SOS Button Pressed");
               SOS_btn.press(false);
               //SOS_btn.drawButton(false);
            }
           
              i=randomvalue; 
              angle = (i/ 57.2958)  - 1.57; 
              x= 160 + cos(angle) * 80;
              y = 239+sin(angle) * 80;
              tft.drawLine(160, 239,x,y, BLACK);
         
              randomvalue=randomvalue+2; 
              i=randomvalue;
              if(i>90)
                { 
                  i=90;
                  randomvalue=90;
                }
            
              returnx=1;
              delay(30);
  
  }
  
  
  else if (!down && returnx ==0)
  {
          down = Touch_getXY();
          if(randomvalue<=-90 || down==1)
          return;
          i=randomvalue; 
        
        

          delay(30);
        }
 
}
