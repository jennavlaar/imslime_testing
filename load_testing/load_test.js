import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { Trend } from 'k6/metrics';

//  Custom Metrics 
export let loginDuration = new Trend('login_duration');
export let playDuration = new Trend('play_duration');

//  Test configuration 
const userCount = __ENV.USER_COUNT ? parseInt(__ENV.USER_COUNT) : 10;
const rampUp = __ENV.RAMP_UP === 'true'; // true for gradual ramp-up, false for all users at once
const scenario = __ENV.SCENARIO || 'login'; // 'login' to only login or 'full' to login and press play
const dataFile = __ENV.USER_DATA_FILE; // specifies number of registered/unregistered users

if (!dataFile) {
  throw new Error("Set USER_DATA_FILE env variable (e.g., USER_DATA_FILE=50_percent_registered.json)");
}

//  K6 options 
export let options = {
  stages: rampUp
    ? [
        { duration: `${userCount / 5 * 10}s`, target: userCount },
        { duration: '20s', target: userCount },
        { duration: '10s', target: 0 },
      ]
    : [
        { duration: '5s', target: userCount },
        { duration: '20s', target: userCount },
        { duration: '10s', target: 0 },
      ],
};

//  Load user data 
const users = new SharedArray('users', function () {
  return JSON.parse(open(`./data/${dataFile}`));
});

function getUser() {
  return users[Math.floor(Math.random() * users.length)];
}

//  Main Test 
export default function () {
  const user = getUser();

  // Getting user info
  const loginPayload = JSON.stringify({
    email: user.email,
    password: user.password,
  });

  const loginHeaders = { 'Content-Type': 'application/json' };

  // Logging in
  const loginRes = http.post('https://imslime.onrender.com/api/login', loginPayload, {
    headers: loginHeaders,
  });

  loginDuration.add(loginRes.timings.duration);

  check(loginRes, {
    'Login request returned 200': (res) => res.status === 200,
  });

  // If Scenario is full, press play
  if (scenario === 'full') {
    const authToken = loginRes.json('token');

    const authHeaders = {
      Authorization: `Bearer ${authToken}`,
    };

    // Press play
    const playRes = http.post('https://imslime.onrender.com/api/game', {}, { headers: authHeaders });

    playDuration.add(playRes.timings.duration);

    check(playRes, {
      'Play request returned 200': (res) => res.status === 200,
    });
  }

  sleep(1);
}
