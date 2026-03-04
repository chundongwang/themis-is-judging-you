import type { Test } from '@/lib/types'
import { apiFetch, delay } from './client'

const FIXTURE_TESTS: Test[] = [
  {
    id: 'test-001',
    name: 'Headshot Attractiveness',
    created_at: '2026-02-28T13:00:00Z',
    prompt_template:
      'You are a {{gender}}, aged {{age}}, working as {{occupation}}. ' +
      'Rate the attractiveness of the following person on a scale from 1 to 10. ' +
      'Respond with just the number and one sentence reason.\n\nPerson: {{text}}',
    scale: { min: 1, max: 10, label: 'attractiveness' },
    population_id: 'us-general',
    panel_size: 20,
    subjects: [
      {
        id: 'subject-1',
        text: 'A person with warm brown eyes and a natural smile.',
        image: null,
      },
    ],
  },
  {
    id: 'test-002',
    name: 'Profile Photo Quality',
    created_at: '2026-02-27T09:00:00Z',
    prompt_template:
      'You are a {{gender}}, aged {{age}}. Rate the quality of this profile photo on a scale of 1-10.',
    scale: { min: 1, max: 10, label: 'quality' },
    population_id: 'cn-mainland',
    panel_size: 10,
    subjects: [
      {
        id: 'subject-2',
        text: 'A professional headshot with neutral background.',
        image: null,
      },
    ],
  },
]

export async function listTests(): Promise<Test[]> {
  await delay()
  return FIXTURE_TESTS
}

export async function getTest(id: string): Promise<Test> {
  await delay()
  const test = FIXTURE_TESTS.find((t) => t.id === id)
  if (!test) throw new Error(`Test not found: ${id}`)
  return test
}

export async function createTest(data: Omit<Test, 'id' | 'created_at'>): Promise<Test> {
  return apiFetch<Test>('/api/tests', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function updateTest(id: string, data: Partial<Test>): Promise<Test> {
  await delay()
  const idx = FIXTURE_TESTS.findIndex((t) => t.id === id)
  if (idx === -1) throw new Error(`Test not found: ${id}`)
  FIXTURE_TESTS[idx] = { ...FIXTURE_TESTS[idx], ...data }
  return FIXTURE_TESTS[idx]
}

export async function deleteTest(id: string): Promise<void> {
  await delay()
  const idx = FIXTURE_TESTS.findIndex((t) => t.id === id)
  if (idx !== -1) FIXTURE_TESTS.splice(idx, 1)
}
