# odd-even-react-flask
Installation:

CLI Linux/MacOS:
```
~$git clone git@github.com:TinKurbatoff/odd-even-react-flask.git
~$cd odd-even-react-flask/frontend-react
~$npm install
~$npm start &
~$cd ../backend-flask/
~$pip3 install -r requirements.txt
~$python3 odd_even.py &
```
Navigate to http://localhost:3000/

*ENJOY!*

# NOTE
If you running your backend on another port or server, consider adding the environmental file `.env` in `/frontend-react` directory:
```
REACT_APP_BASE_URL=<base_url_to_backend>
```
