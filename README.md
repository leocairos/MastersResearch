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
3.1  apt-get install python-pip
3.2 apt-get install git
* apt-get install python3-pip
* pip3 install git+https://github.com/webpy/webpy#egg=web.py
*. pip3 install sklearn
*. pip3 install numpy
*. pip3 install scipy
i. pip3 install requests
j. pip3 install jupyter
k. pip3 install gensim

10. https://pypi.python.org/pypi/fasttext
The. https://pypi.python.org/pypi/Cython/
B. pip3 install Cython --install-option = "- no-cython-compile"
w. pip3 install fasttext

jupyter notebook --no-browser --allow-root --ip = 192.168.20.213 --NotebookApp.token =

rdlsc-mestrado.ddns.net:8016

1. InstallSetting up Python:
  + We use anaconda by continuum.io (see [Why?](https://www.continuum.io/why-anaconda))
    - We won't need the entire distribution. [Download](http://conda.pydata.org/miniconda.html) a Python 2.7 version & install a minimal version of anaconda.
  + Make sure you select add to PATH during install.
  + Next, run `setup.bat`. This will install all the dependencies needed to run the tool.
  + If the above does not work well. Remember you only need a Python 2.7 and three packages listed in `requirements.txt` installed. So `pip install -r requirements.txt` will work.

2. Running script:
  + Navigate to *src* and run `index.py`.
  + If all is well, you'll be greeted by this:
  ![](https://github.com/fastread/src/blob/master/tutorial/screenshots/run.png?raw=yes)

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
  

