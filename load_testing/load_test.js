import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

export let options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '20s', target: 10 },
    { duration: '10s', target: 0 },
  ],
};

// Get dataset filename from environment variable
const fileName = __ENV.USER_DATA_FILE;

if (!fileName) {
  throw new Error("Please set the USER_DATA_FILE environment variable, e.g., USER_DATA_FILE=50_percent_registered.json");
}

const users = new SharedArray('users', function () {
  return JSON.parse(open(`./data/${fileName}`));
});

function getUser() {
  return users[Math.floor(Math.random() * users.length)];
}

export default function () {
  const user = getUser();

  const loginPayload = JSON.stringify({
    email: user.email,
    password: user.password,
  });

  const loginHeaders = { 'Content-Type': 'application/json' };

  // Attempt to login
  const loginRes = http.post('https://imslime.onrender.com/api/login', loginPayload, {
    headers: loginHeaders,
  });

  check(loginRes, {
    'Login request returned 200': (res) => res.status === 200,
  });

  const authToken = loginRes.json('token');

  const authHeaders = {
    Authorization: `Bearer ${authToken}`,
  };

  const playRes = http.post('https://imslime.onrender.com/api/game', {}, { headers: authHeaders });

  check(playRes, {
    'Play request returned 200': (res) => res.status === 200,
  });

  sleep(1);
}
