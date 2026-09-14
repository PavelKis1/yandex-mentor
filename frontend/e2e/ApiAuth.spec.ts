import { test, expect } from '@playwright/test';

test('API access works with Basic Auth', async ({ request }) => {
  const response = await request.get('http://localhost:8000/api/roadmap', {
    headers: {
      'Authorization': 'Basic YWRtaW46YWRtaW4=' // admin:admin
    }
  });
  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  expect(data).toHaveProperty('roadmap');
});
