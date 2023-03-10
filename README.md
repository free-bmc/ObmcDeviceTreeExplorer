# ObmcDeviceTreeExplorer Utility 
 OpenBMC Device Tree Explorer tool used as a primer tool to parse/build Device Tree files and gather device elements for ObmcEMCfgbuilder tool(Upcoming)
 This tool uses the DeviceCatalogDB.json generated by ObmcDevCheckUtil tool for cross referencing the supported devics 

 ## Rationale 
 1. As we all know Platform definition starts from the the Device Tree File for Linux, this makes it very important to derive the platform definition to 
 be used by Entity Manager and other OpenBMC components from the source to ensure alignment
 2. OpenBMC firmware team needs to be aware of the unsupported devices chosen in the device tree files 
 3. Build Device Objects that can be used by Entity Manager Tools and others to build their configuration 

 ## Impact 
 1. Allows the OpenBMC Firmware development to start from Platform definition 
 2. Allows the developers to spent more time on the Device Tree File definition 

## Version Information 

### 1.0 
- Using the Device Catalog Database build by the ObmcDevCheckUtil, will parse reasonable complex DTS file by connecting all the DTSI's 
- Scan a single file or a entire dts directory 
- Allows to select the architecture to search for the dts files 

### Future versions
- Builds DTS Json files with more system attributes that can be used by Entity Manager tools and other OpenBMC Tools 
- Builds standard formated Device Tree Files using platform design input 

## About the Tool 

The tool utilizes the OpenBMC Linux Source and the Device Catalog to cross reference 

### Tool Setup 

Set up the Linux Source Directory
export OBMC_LINUX_SOURCE_DIR=/home/hari/github/LinuxSource/linux-dev-6.0/

### Tool Usage 

```
$ ./dtsexplorer.py
Welcome to Device Tree Explorer Utility
Linux Source Reference Directory is  /home/hari/github/LinuxSource/linux-dev-6.0
CLI started ...
type help to get started ...
Device Tree CLI >> help
Commands and Options:
        version       <options>                Version Info
        dtsfile       <dtsfile>                Set DTS File
        listarch                               List Arch Types
        setarch       <arch-type>              Set Arch Type
        devref        <file>                   Set Device Reference Json File
        setdbg                                  Set Debug ON/OFF toggle
        scan                                   Start DTS Scan Arch Directory using filters
        scanfile      <file>                   Start DTS Scan of File
        filter        <filter1,...>            Set DTS File Filters separated by commas
Device Tree CLI >> listarch
List of Architectures Found :
         csky
         riscv
         powerpc
         arc
         openrisc
         arm64
         nios2
         microblaze
         sh
         xtensa
         arm
         mips
         loongarch
Device Tree CLI >> setarch arm
Set Architecture to  /home/<user>/../LinuxSource/linux-dev-6.0/arch/arm/boot/dts
Device Tree CLI >> devref ./DeviceCatalogDB.json
Device Tree CLI >> scanfile ./sample.dts
Reading Device Catalog : [####################################################################################################] 4913/4913
                         DTS Name                            I2CBuss     I2CDevices     GPIOs         LEDs      IIODevices      Pwms        Tachos      Eeproms     UNSUPP
                        sample.dts                              11           14           72           22           32           8            8            3          0

Device Tree CLI >> filter aspeed-
Device Tree CLI >> scan
Reading Device Catalog : [####################################################################################################] 4913/4913
Scanning DTS Files : [####################################################################################################] 58/58
                         DTS Name                            I2CBuss     I2CDevices     GPIOs         LEDs      IIODevices      Pwms        Tachos      Eeproms     UNSUPP
               aspeed-bmc-ampere-mtjade.dts                     11           20           31           4            88           12           12           1          0
                aspeed-bmc-opp-lanyang.dts                      12           3            7            12           32           4            4            1          0
                aspeed-bmc-tyan-s7106.dts                       9            14           0            4            32           8            8            3          0
             aspeed-bmc-supermicro-x11spi.dts                   8            0            0            0            32           0            0            0          0
             aspeed-bmc-facebook-wedge40.dts                    0            0            0            0            2            4            4            0          0
             aspeed-bmc-facebook-wedge400.dts                   14           27           0            0            2            0            0            0          0
                aspeed-bmc-vegman-sx20.dts                      3            5            58           0            0            7            7            0          0
                aspeed-bmc-tyan-s8036.dts                       9            14           0            4            32           7            7            3          0
                aspeed-bmc-opp-vesnin.dts                       13           8            4            12           0            0            0            1          0
            aspeed-bmc-facebook-tiogapass.dts                   10           52           70           0            16           2            2            4          0
              aspeed-bmc-facebook-elbert.dts                    3            18           0            0            0            0            0            0          0
                aspeed-bmc-vegman-n110.dts                      3            5            48           0            0            6            6            0          0
               aspeed-bmc-facebook-fuji.dts                     4           155           0            0            0            0            0            0          0
              aspeed-bmc-qcom-dc-scm-v1.dts                     12           0            16           0            0            0            0            0          0
              aspeed-bmc-bytedance-g220a.dts                    14           73          118           2            32           6            6            0          0
              aspeed-bmc-inspur-on5263m5.dts                    2            4            0            2            16           2            2            1          0
           aspeed-bmc-facebook-cloudripper.dts                  7            62           0            0            0            0            0            0          0
            aspeed-bmc-facebook-yosemitev2.dts                  10           10           0            0            32           2            2            1          0
               aspeed-bmc-opp-palmetto.dts                      8            4            22           6            0            0            0            1          0
                 aspeed-bmc-opp-zaius.dts                       14           30           28           8            32           4            4            1          0
               aspeed-bmc-amd-ethanolx.dts                      9            9            48           4            2            8            8            1          0
                aspeed-bmc-opp-romulus.dts                      12           2            21           6            2            7            7            0          0
          aspeed-bmc-arm-stardragon4800-rep2.dts                10           12           2            4            18           0            0            2          2
             aspeed-bmc-facebook-wedge100.dts                   2            1            0            0            2            0            0            0          0
              aspeed-bmc-ibm-rainier-4u.dts                     1            2            0            0            0            0            0            0          0
           aspeed-bmc-inventec-transformers.dts                 11           18           10           4            0            0            0            6          0
                aspeed-bmc-vegman-rx20.dts                      3            16           67           8            0            7            7            3          0
             aspeed-bmc-asrock-e3c246d4i.dts                    2            2            52           4            26           0            0            1          0
             aspeed-bmc-portwell-neptune.dts                    7            5            0            6            0            2            2            1          0
              aspeed-bmc-inspur-nf5280m6.dts                    14           66           79           12           32           8            8            1          0
              aspeed-bmc-lenovo-hr855xg2.dts                    13           15           34           4            32           17           17           1          0
             aspeed-bmc-ampere-mtmitchell.dts                   11           22           72           0           128           0            0            2          0
                aspeed-ast2600-evb-a1.dts                       0            0            0            0            0            0            0            0          0
                 aspeed-bmc-opp-swift.dts                       9           104           30           20           4            0            0            6          7
                aspeed-bmc-quanta-q71l.dts                      10           36           0            6            24           8            8            13         0
                aspeed-bmc-opp-mowgli.dts                       14           27           20           16           20           10           10           1          0
            aspeed-bmc-facebook-galaxy100.dts                   1            0            0            0            2            0            0            0          0
               aspeed-bmc-amd-daytonax.dts                      12           0            11           4            32           16           16           0          0
                  aspeed-ast2500-evb.dts                        2            2            0            0            0            0            0            1          0
               aspeed-bmc-facebook-yamp.dts                     14           1            0            0            0            0            0            0          0
                aspeed-bmc-ibm-everest.dts                      16          272           28           10           2            0            0            48         7
                aspeed-bmc-quanta-s6q.dts                       13           48           13           6            32           0            0            4          0
             aspeed-bmc-facebook-minipack.dts                   14           96           0            0            0            0            0            0          0
                aspeed-bmc-opp-nicole.dts                       7            2            27           8            2            0            0            1          0
             aspeed-bmc-asrock-romed8hm3.dts                    9            5            50           4            32           4            4            1          0
                aspeed-bmc-ibm-rainier.dts                      16          183           33           8            2            0            0            22         9
             aspeed-bmc-ibm-rainier-1s4u.dts                    0            0            0            0            0            0            0            0          0
                  aspeed-ast2600-evb.dts                        14           3            0            0            0            0            0            1          0
                aspeed-bmc-ibm-bonnell.dts                      16           39           22           8            2            0            0            6          5
              aspeed-bmc-inspur-fp5280g2.dts                    13           75           39           16           32           8            8            1          0
               aspeed-bmc-lenovo-hr630.dts                      13           13           23           4            28           14           14           1          0
                aspeed-bmc-opp-mihawk.dts                       14          109           36           18           32           12           12           4          0
              aspeed-bmc-opp-witherspoon.dts                    9            53           29           22           6            0            0            1          5
             aspeed-bmc-microsoft-olympus.dts                   8            2            0            10           16           6            6            0          0
            aspeed-bmc-facebook-bletchley.dts                   12           65           61           0            32           0            0            8          6
               aspeed-bmc-facebook-cmm.dts                      10          207           0            0            16           0            0            0          0
                aspeed-bmc-opp-tacoma.dts                       12           55           24           0            4            0            0            1          7
               aspeed-bmc-intel-s2600wf.dts                     8            0            0            0            32           0            0            0          0
Device Tree CLI >>
```

### Notes for Users 

This version provides integity check and scans the dts file for device objects,  the subsequent versions will cover more definitions