# BIOL2103-ELISA

BIOL2103-ELISA is a script that help automatically analyzing the result of ELISA experiment from lab course BIOL2103 Biological science laboratory course, provided by Department of Biological Sciences, The University of Hong Kong. The script can help determine the origin and generate route map by input the table of experimental result (mix and signal).

## Requirement

+ Python 3.x
+ graphviz module
+ [Graphviz software](https://graphviz.org/download/)

## Install

> You should download Graphviz software first in order to draw the route map no matter which platform you choose

#### Graphviz

+ [Windows](https://graphviz.org/download/#windows)
+ [Mac](https://graphviz.org/download/#mac)
+ [Linux](https://graphviz.org/download/#linux)



**! --- Graphviz do not being added to system path in default but you should choose to add it --- !**

![Choose Add Graphviz to the system PATH](https://github.com/hkumaster/BIOL2103-ELISA/raw/main/Documentation/Pictures/GraphvizInstallChoice.png)

### Windows 10

You can [click here](https://github.com/hkumaster/BIOL2103-ELISA/releases/tag/v0.0) to download the [BIOL2103-ELISA_v0_win.exe](https://github.com/hkumaster/BIOL2103-ELISA/releases/download/v0.0/BIOL2103-ELISA_v0_win.exe) executable and use it directly.

### Other Platform (Mac/Linux/Windows)

Please first install the ```graphviz``` module using pip

```bash
pip install graphviz
```

Then you can directly download the [Source code](https://github.com/hkumaster/BIOL2103-ELISA/releases/tag/v0.0) and run it by command

```shell
python Result_analysis.py
```

## Usage

You should first make a csv document that recorded the table of experimental result. The csv file should be separated by comma in format. You can get the reference of the format from [Result_Demo.csv](https://github.com/hkumaster/BIOL2103-ELISA/blob/main/Result_Demo.csv)

![How to make the csv file by Microsoft Excel](https://github.com/hkumaster/BIOL2103-ELISA/raw/main/Documentation/Pictures/MakeCSV.gif)

Then you can execute the program.

```shell
Name of the .csv file you want to load
>
```

And you just need to input the file name of the csv you had just made, for example, ```Result.csv``` or you can use absolute path ```D:/BIOL2103/Result.csv```

It will calculate some data that may be useful for you to write into the report.

![Part of the Data](https://github.com/hkumaster/BIOL2103-ELISA/raw/main/Documentation/Pictures/ProgramDemo.png)

The route map of the origin will be automatically generated and named in ```route_map.pdf``` in the directory you run the program. 

![route map of origin sample](https://github.com/hkumaster/BIOL2103-ELISA/raw/main/Documentation/Pictures/RouteMapOrigin.png)

After that you can choose to make the route map of other sample by input the letter code or exit by enter any non letter code character.