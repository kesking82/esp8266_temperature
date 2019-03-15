from machine import Pin,RTC
from dht import DHT11  
from time import sleep
from mqtt import connect,pubdata
import utime
import json
import ntptime

# MQTT服务器地址或域名
server = "xxxxx"

#MQTT服务器端口
port=xxx

#设备ID，可自定义
client_id = "xxxx"

#MQTT BORKER登陆用户名
username='xxx'

#MQTT BORKER登陆密码
password='xxx'


##于NTP服务器时间同步 
def ntpsettime():
    try:
      ntptime.time()  ##获取NTP服务器上的时间
      ntptime.settime()  ##时间写入时钟
      rtc=RTC()
      tampon1=utime.time()
      tampon2=tampon1+8*60*60 ##由于默认是UTC时区，需要增加8小时
      rtc.datetime ( utime.localtime(tampon2)[0:3] + (0,) + utime.localtime(tampon2)[3:6] + (0,))
      print("NTP同步成功")
      return 0
    except Exception as e:
      print("NTP同步失败")
      print(str(e))
      return 1

if __name__ == '__main__':  
    
    dht=DHT11(Pin(5))   ##需要和主板的PIN口一致
   
    #连接MQTT服务器
    c_mqtt=connect(client_id,server,port,username,password)
    
    #同步时间，如果同步不成功，则不会继续执行
    ntp_ret=1
    while ntp_ret==1:
      ntp_ret=ntpsettime()
      sleep(1) 
      
    #连接成功后主板亮灯起
    Pin(2,Pin.OUT,value=0)
    
    try:
      while (1): 
        (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime()
        data_time='{}{:0>02d}{:0>02d}{:0>02d}{:0>02d}{:0>02d}'.format(year,month,mday,hour,minute,second)
        print (year,'-','%02d'%month,'-','%02d'%mday, ' ','%2d'% hour,':','%02d'% minute,':','%02d'% second,sep = '')
        dht.measure()
        data_temperature=dht.temperature() 
        data_humidity=dht.humidity() 
        #msg={'datastreams':[{'id':'temperature','datapoints':[{'value':data_temperature}]},{'id':'humidity','datapoints':[{'value':data_temperature}]}]}
        msg={'temperature':data_temperature,'humidity':data_humidity}
        #msg_json=json.dumps(msg)
        data_dic={'value':msg,'time':data_time}
        #data_json=json.dumps(data_dic)
        result_str=pubdata(c_mqtt,data_dic)
        print(result_str)
        sleep(60)
    finally:
      c_mqtt.disconnect()
      Pin(2,Pin.OUT,value=1)











































