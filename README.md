# KKBOXsearchBot


## About

It is a Bot allow user search for top rank 50 songs in KKBOX

## Requirement

```
sudo pip3 install Flask
sudo pip3 install pygraphviz --install-option="--include-path='/usr/include/graphviz/'" --install-option="--library-path='/usr/lib/graphviz'"
sudo pip3 install transitions
sudo pip3 install requests
sudo pip3 install lxml
sudo pip3 install beautifulsoup4
```

## How to Run


1. Install module
2. set env
    - TOKEN
    - URL

3. Following the command
```
ngrok http -bind-tls=true 5000
./app.py
```

![state_diagram.png]
