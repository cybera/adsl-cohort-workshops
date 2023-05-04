# Python Dashboarding-101

This repository describes the concept of python dashboarding using [voila](https://voila.readthedocs.io/en/stable/), [plotly dash](https://plotly.com/dash/), [streamlit](https://streamlit.io/) and [panel](https://panel.holoviz.org/). 

To get all the dashboards up and running, clone this repository to your local computer or a remote server and then open a terminal and run: 

```
cd adsl-cohort-workshops/python_dashboarding
docker compose up -d
```

The above `docker compose` command will download all the required docker images, install dependencies and spin up the specified containers. With the successful docker build, you can access the desired dashboards using the following links:

1. JupyterLab: http://localhost:8890
2. Voila: http://localhost:8867
3. Dash: http://localhost:8050
4. Streamlit: http://localhost:8501
5. Panel: http://localhost:5006

It is important to note that if you are running the docker containers remotely, please make sure to apply the port forwarding for each container and access the links with the forwarded ports.  

### References: 
1. [Plotly Dash Callbacks examples](https://dash.plotly.com/basic-callbacks)
2. [Country Indicators Plotly Datasets](https://github.com/plotly/datasets/blob/master/country_indicators.csv)