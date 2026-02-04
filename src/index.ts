import { ml_kem } from '@security/quantum-safe';

export async function getData() {
  const response = await ml_kem.request('https://api.example.com/data');
  return response.json();
}

export async function postData(data: any) {
  const response = await ml_kem.request('https://api.example.com/data', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return response.json();
}
