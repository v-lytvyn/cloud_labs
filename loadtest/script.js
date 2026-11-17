import http from 'k6/http';
import { check, sleep } from 'k6';

const VUS = Number(__ENV.VUS || 40);
const BASE_URL = (__ENV.BASE_URL || 'http://localhost:5000').replace(/\/$/, '');

export const options = {
  stages: [
    { duration: '3m', target: VUS },
    { duration: '5m', target: VUS },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
  },
};

export function setup() {
  const jsonHeaders = { 'Content-Type': 'application/json' };

  const loginRes = http.post(
    `${BASE_URL}/auth/login`,
    JSON.stringify({ username: 'admin', password: 'admin' }),
    { headers: jsonHeaders }
  );

  const token = loginRes.status === 200 ? loginRes.json('access_token') : null;
  if (!token) {
    throw new Error(`Помилка авторизації! Статус: ${loginRes.status}, Тіло: ${loginRes.body}`);
  }

  const authHeaders = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };

  let doctorId = 1;
  const docRes = http.post(
    `${BASE_URL}/doctors/`,
    JSON.stringify({
      first_name: 'John',
      last_name: 'Doe',
      specialization: 'Surgeon',
      phone: '+380501234567',
      email: `doc_${Date.now()}@hospital.com`,
    }),
    { headers: authHeaders }
  );
  if (docRes.status === 200 || docRes.status === 201) {
    const docBody = docRes.json();
    doctorId = docBody.doctor_id || docBody.id || doctorId;
  }

  let patientId = 1;
  const patRes = http.post(
    `${BASE_URL}/patients/`,
    JSON.stringify({
      first_name: 'Jane',
      last_name: 'Doe',
      phone: '+380671234567',
      email: `pat_${Date.now()}@example.com`,
    }),
    { headers: authHeaders }
  );
  if (patRes.status === 200 || patRes.status === 201) {
    const patBody = patRes.json();
    patientId = patBody.patient_id || patBody.id || patientId;
  }

  return { token, doctorId, patientId };
}

export default function (data) {
  const authParams = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${data.token}`,
    },
  };

  const apptPayload = JSON.stringify({
    doctor_id: data.doctorId,
    patient_id: data.patientId,
    appointment_datetime: '2026-11-20 10:00:00',
    status: 'planned',
    notes: `Load test ${__VU}-${__ITER}`,
  });

  const createRes = http.post(`${BASE_URL}/appointments/`, apptPayload, authParams);
  check(createRes, {
    'POST /appointments/ is 200': (r) => r.status === 200,
  });

  let createdApptId = 1;
  try {
    const body = createRes.json();
    if (body && body.appointment_id) {
      createdApptId = body.appointment_id;
    }
  } catch (e) {}

  for (let i = 0; i < 3; i++) {
    const listRes = http.get(`${BASE_URL}/appointments/`);
    check(listRes, { 'GET /appointments/ is 200': (r) => r.status === 200 });
  }

  for (let i = 0; i < 2; i++) {
    const oneRes = http.get(`${BASE_URL}/appointments/${createdApptId}`);
    check(oneRes, { 'GET /appointments/:id is 200': (r) => r.status === 200 });
  }

  for (let i = 0; i < 2; i++) {
    const docRes = http.get(`${BASE_URL}/doctors/${data.doctorId}`);
    check(docRes, { 'GET /doctors/:id is 200': (r) => r.status === 200 });
  }

  const patRes = http.get(`${BASE_URL}/patients/${data.patientId}`);
  check(patRes, { 'GET /patients/:id is 200': (r) => r.status === 200 });

  const svcRes = http.get(`${BASE_URL}/services/`);
  check(svcRes, { 'GET /services/ is 200': (r) => r.status === 200 });

  sleep(0.5);
}
