var addresses=1;
msg.slave_ip="192.168.1.246";
let Counter = flow.get("Counter") || 0;
// variable not fixed
flow.set("DCDCD", 1);
if(Counter === 16){flow.set("Counter", 0);flow.set("DCDCD", 0);return null;}
if(Counter === 0)
{
// variable not fixed
let keys = Object.keys(msg.payload)
let ID = keys[1]
let value = msg.payload[keys[1]]
flow.set("ID", ID);
flow.set("value", value);
}
let ID    = flow.get("ID") || 0;
let value = flow.get("value") || 0;
Counter ++;
flow.set("Counter", Counter);

switch(ID) {
  case "DC_Dir":
    msg.payload = `61,${value},${Counter}`
    break;
  case "C_S":
    msg.payload = `62,${value},${Counter}`
    break;
  case "V_S":
    msg.payload = `63,${value},${Counter}`
    break;
  case "CMD":
    msg.payload = `99,${value},${Counter}`
    break;
  case "CT_M":
    msg.payload = `201,${value},${Counter}`
    break;
  case "Dir":
    msg.payload = `202,${value},${Counter}`
    break;
  case "S_P":
    msg.payload = `203,204,${value[0]},${value[1]},${Counter}`
    break;
  case "TOut":
    msg.payload = `206,${value},${Counter}`
    break;
    default:
    return null;
   }
return msg;