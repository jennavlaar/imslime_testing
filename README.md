# I'm Slime Testing

Testing the software performance of [I'm Slime](https://imslime.onrender.com/#/Login), a web-based online multiplayer versus gacha game.


## Load Testing

To run load testing, ensure you have k6 installed on your computer. Type **k6 run load_test.js** with the desired targeted dataset and configuration as follows:

```k6 run load_test.js --env USER_DATA_FILE=filename --env USER_COUNT=count --env RAMP_UP=true --env SCENARIO=login```

Where *USER_DATA_FILE* can be **0_percent_registered.json**, **25_percent_registered.json**, **50_percent_registered.json**, **75_percent_registered.json** or **100_percent_registered.json**. This controls the percentage of registered users that will attempt to login to the system

Where *USER_COUNT* can be any integer i.e. 10, 25, 35, 50. This controls the number of concurrent users.

Where *RAMP_UP* can be **true** or **false**. This controls whether there will be a gradual ramp-up of 5 users every 10 seconds or all users at once.

Where *SCENARIO* can be **login** or **full**. This controls whether the user will login or will login and press play.

Example:
```
    k6 run load_test.js --env USER_DATA_FILE=0_percent_registered.json --env USER_COUNT=10 --env RAMP_UP=false --env SCENARIO=full
    k6 run load_test.js --env USER_DATA_FILE=25_percent_registered.json --env USER_COUNT=25 --env RAMP_UP=true --env SCENARIO=login
```