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

const users = new SharedArray('users', function () {
  return JSON.parse(open('./users.json'));
});

function getUser() {
  return users[Math.floor(Math.random() * users.length)];
}

export default function () {
  let user = getUser();

  let loginPayload = JSON.stringify({
    email: user.email,
    password: user.password,
  });

  let loginHeaders = { 'Content-Type': 'application/json' };

  // Perform login request
  let loginRes = http.post('https://imslime.onrender.com/#/Login', loginPayload, {
    headers: loginHeaders,
    redirect: 'follow',
  });

  check(loginRes, {
    'Login successful': (res) => res.status === 200,
  });

  let authToken = loginRes.json('token');

  let authHeaders = {
    'Authorization': `Bearer ${authToken}`,
  };

  let playRes = http.post('https://imslime.onrender.com/#/game', {}, { headers: authHeaders });

  check(playRes, {
    'Play button triggered successfully': (res) => res.status === 200,
  });

  sleep(1);
}
