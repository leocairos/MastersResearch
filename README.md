Tool - Masters Research
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

You'll see a page like below:
  ![](https://github.com/leocairos/MastersResearch/blob/master/screenshots/tool_index.png?raw=yes)
    
Use Tool
-----

The following figure demonstrates the main tool usage screen. And just below a brief description of their areas and functions:
![](https://github.com/leocairos/MastersResearch/blob/master/screenshots/tool_slr_detail.png?raw=yes)
+ **A:** Title of the research/review that the researcher is performing. Informed in the moment of a research.
+ **B:** Field used to insert or change the Search String that will be processed on the repository. The "New search" button is responsible for executing the Repository Search String through the API.
+ **C:** Displays the last processed Search String.
+ **D:** Displays the list of words extracted from the Search String and also the words generated by the TF-IDF. This list is generated by clicking the "Skip-Gram vs. CBOW" link.
+ **E:** List with the most relevant words identified in each set. Next to the word is presented the index of relevance.
+ **F:** By positioning the mouse over any of the words in the group **D** is a list of related terms (generated by Skip-Gram and CBOW).
+ **G:** This table shows all the publications located in Scopus based on the search string used. Clicking the "Abstract" link displays the publication summary for reading. In this table it is also possible to classify each publication as Include or Exclude. When you sort the list in **E** it is automatically updated.
+ **H:** Area destined for the pagination of the result.

Note
----
+ To perform queries using the Scopus API, you must configure the "apiKey" and "insttoken" keys in rdlsc_util.py. These keys are for private use and are therefore not available.
+ apiKey can be generated at https://dev.elsevier.com/apikey/manage.
+ insttoken must be requested from Elsevier support at the same address.
