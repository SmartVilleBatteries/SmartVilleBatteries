def backward(b):
    warningHelper = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]    
    warningMess = {1:"WRN_ONLY_SUB_RELAY_COMMAND",2:"BATTERY_HIGH_VOLTAGE",4:"BATTERY_LOW_VOLTAGE",8:"BATTERY_HIGH_TEMP",
    16:"BATTERY_LOW_TEMP", 32:"UNKNOWN_ww5", 64: "UNKNOWN_ww6", 128: "BATTERY_HIGH_CURRENT_DISCHARGE", 256: "BATTERY_HIGH_CURRENT_CHARGE", 512: "UNKNOWN_WW1",
     1024: "UNKNOWN_WW2", 2048: "BMS_INTERNAL", 4096: "CELL_IMBALANCE", 8192:"ALARM_SUB_PACK2_ERROR", 16384: "ALARM_SUB_PACK1_ERROR", 32768:"UNKNOWN_WW7"}
    
    BMS_LIMITS = "0x351#"
    BMS_SOC_SOH = "0x355#"
    BMS_VOLT_AMP_TEMP = "0x356#"
    BMS_WARN_ALARM = "0x35A#"

    if "voltage" in b:
        CAN_ID = 0x356
        val = int(b["voltage"] * 100)
        val = format(val,'04x')
        BMS_VOLT_AMP_TEMP += (val[2:4])
        BMS_VOLT_AMP_TEMP += (val[0:2])
    else: BMS_VOLT_AMP_TEMP.append("0000")
   
    if "current" in b:
        CAN_ID = 0x356
        val = int(b["current"] * 10)
        # handle neg value
        if val < 0:
            val = hex((val + (1 << 16)) % (1 << 16))
            BMS_VOLT_AMP_TEMP += (val[4:6])
            BMS_VOLT_AMP_TEMP += (val[2:4])
        else:
            val = format(val,'04x')
            BMS_VOLT_AMP_TEMP += (val[2:4])
            BMS_VOLT_AMP_TEMP += (val[0:2])
    else: BMS_VOLT_AMP_TEMP.append("0000")

    if "temp" in b:
        CAN_ID = 0x356
        val = int(b["temp"] * 10)
        val = format(val,'04x')
        BMS_VOLT_AMP_TEMP += (val[2:4])
        BMS_VOLT_AMP_TEMP += (val[0:2])

    else: BMS_VOLT_AMP_TEMP += ("0000")

    BMS_VOLT_AMP_TEMP += ("0000")
    
    if "maxVoltage" in b:
        CAN_ID = 0x351
        val = int(b["maxVoltage"] * 10)
        val = format(val,'04x')
        BMS_LIMITS += (val[2:4])
        BMS_LIMITS += (val[0:2])
    else: BMS_LIMITS += ("0000")


    if "maxChargeCurrent" in b:
        CAN_ID = 0x351
        val = int(b["maxChargeCurrent"] * 10)
        val = format(val,'04x')
        BMS_LIMITS += ( val[2:4])
        BMS_LIMITS += (val[0:2])
    else: BMS_LIMITS += ("0000")

    if "maxDischargeCurrent" in b:
        CAN_ID = 0x351
        val = int(b["maxDischargeCurrent"] * 10)
        val = format(val,'04x')
        BMS_LIMITS += (val[2:4])
        BMS_LIMITS += (val[0:2])
    else: BMS_LIMITS += ("0000")

    BMS_LIMITS  += ("0000")

    if "soc" in b:
        CAN_ID = 0x355
        val = format(b["soc"],'04x')
        BMS_SOC_SOH += (val[2:4])
        BMS_SOC_SOH += (val[0:2])
    else: BMS_SOC_SOH += ("0000")
    
    if "soh" in b:
        CAN_ID = 0x355
        val = format(b["soh"],'04x')
        BMS_SOC_SOH += (val[2:4])
        BMS_SOC_SOH += (val[0:2])
    else: BMS_SOC_SOH += ("0000")
    

    BMS_SOC_SOH += ("00000000")

    if ("warnings" in b):
        CAN_ID = 0x35A
        val = b["warnings"]
        counter = 0
        # print(len(b["warnings"]))
        for i in range(65536):
            for j in warningHelper:
                if (warningMess[j] not in val): break
                if(i&j) != 0:
                    if (warningMess[j] in val): counter += 1

            if counter == len(b["warnings"]):
                val = format(i,'04x')
                BMS_WARN_ALARM += (val[2:4])
                BMS_WARN_ALARM += (val[0:2])
            counter = 0

    if ("alarms" in b):
        CAN_ID = 0x35A
        val = b["alarms"]
        if val[0] == 'UNKNOWN_ALARM': BMS_WARN_ALARM += ("ffff")

    BMS_WARN_ALARM += ("00000000")


    print(BMS_VOLT_AMP_TEMP)
    print(BMS_SOC_SOH)
    print(BMS_WARN_ALARM)
    print(BMS_LIMITS)
        
backward({"soc":77,"soh":99,"voltage":54.51,"current":-1.9,"temp":18.6,"maxVoltage":57.7,"maxChargeCurrent":91.8,"maxDischargeCurrent":91.8,"warnings":["WRN_ONLY_SUB_RELAY_COMMAND","BATTERY_HIGH_VOLTAGE","BATTERY_LOW_VOLTAGE","BATTERY_HIGH_TEMP","BATTERY_LOW_TEMP","UNKNOWN_ww5","UNKNOWN_ww6","BATTERY_HIGH_CURRENT_DISCHARGE","BATTERY_HIGH_CURRENT_CHARGE","UNKNOWN_WW1","UNKNOWN_WW2","BMS_INTERNAL","CELL_IMBALANCE","ALARM_SUB_PACK2_ERROR","ALARM_SUB_PACK1_ERROR","UNKNOWN_WW7"],"alarms":["UNKNOWN_ALARM"]})