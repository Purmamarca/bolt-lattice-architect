import { latticeHandshake } from '@security/quantum-safe';

export async function getData() {
  const response = await latticeHandshake({
    url: 'https://api.example.com/data',
    method: 'GET',
    encryption: 'ML-KEM-768'
  });
  return response;
}

export async function postData(data: any) {
  const response = await latticeHandshake({
    url: 'https://api.example.com/data',
    method: 'POST',
    body: data,
    encryption: 'ML-KEM-768'
  });
  return response;
}
