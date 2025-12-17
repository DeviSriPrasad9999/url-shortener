import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 2000,
  duration: '30s',
};

const BASE = 'http://localhost:9000';

export default function () {
  // let payload = JSON.stringify({ url: "https://example.com?q=" + Math.random() });

  // let res = http.post(`${BASE}/shorten/`, payload, {
  //   headers: { "Content-Type": "application/json" }
  // });

  // if (res.status !== 200) {
  //   console.error("Bad response:", res.status, res.body);
  //   return;
  // }

  // let code = JSON.parse(res.body).short_code;
  let code = 'eHHsA9X';

  let redirect = http.get(`${BASE}/${code}`, { redirects: 0 });

  check(redirect, {
    "redirect works": (r) => r.status === 302 || r.status === 307
  });

  sleep(0.1);
}
