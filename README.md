Masters Research
-----
This repository contains the files of the tool developed during academic master's project.

Latest Versions:

- On Github repo: [https://github.com/leocairos/MastersResearch](https://github.com/leocairos/MastersResearch).


Setting up
-----

To create an environment free of interferences and 100% compatible with the tool, we recommend the following installation:
1. Install Virtual Box 
2. Install Ubuntu Desktop
3. Install the necessary packages:
+ apt-get install python-pip
+ apt-get install git
+ apt-get install python3-pip
+ pip3 install git+https://github.com/webpy/webpy#egg=web.py
+ pip3 install sklearn
+ pip3 install numpy
+ pip3 install scipy
+ pip3 install requests
+ pip3 install jupyter
+ pip3 install gensim
+	pip3 install Cython --install-option="--no-cython-compile"
+	pip3 install fasttext
4. Run the rdlsc_app.py 
5. Open your browser and go to http://127.0.0.1:8080



3. The Interface:
  + Fire up your browser and go to [`http://localhost:5000/hello/`](http://localhost:5000/hello/). You'll see a page like below:
  ![](https://github.com/fastread/src/blob/master/tutorial/screenshots/start.png?raw=yes)
    
Use Tool
-----

1. Get data ready:
  + Put your candidate list (a csv file) in *workspace > data*.
  + The candidate list can be as the same format as the example file *workspace > data > Hall.csv* or a csv file exported from [IEEExplore](http://ieeexplore.ieee.org/).
  
2. Load the data:
  + Click **Target: Choose File** button to select your csv file in *workspace > data*. Wait a few seconds for the first time. Once the data is successfully loaded, you will see the following:
  ![](https://github.com/fastread/src/blob/master/tutorial/screenshots/load.png?raw=yes)
  

