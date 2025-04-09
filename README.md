# I'm Slime Testing

Testing the software performance of [I'm Slime](https://imslime.onrender.com/#/Login), a web-based online multiplayer versus gacha game.


## Load Testing

To run load testing, ensure you have k6 installed on your computer. Type **k6 run load_test.js** with the desired targetted dataset like so:
```
    k6 run load_test.js --env USER_DATA_FILE=0_percent_registered.json
    k6 run load_test.js --env USER_DATA_FILE=25_percent_registered.json
    k6 run load_test.js --env USER_DATA_FILE=50_percent_registered.json
    k6 run load_test.js --env USER_DATA_FILE=75_percent_registered.json
    k6 run load_test.js --env USER_DATA_FILE=100_percent_registered.json
```