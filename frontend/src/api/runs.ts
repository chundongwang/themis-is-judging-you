import type { Run } from '@/lib/types'
import { delay } from './client'

const FIXTURE_RUNS: Run[] = [
  {
    id: 'mock-run-id',
    test_id: 'test-001',
    executed_at: '2026-02-28T14:30:00Z',
    panel_size: 20,
    results: [
      {
        subject_id: 'subject-1',
        mean: 7.2,
        median: 7.5,
        std: 1.1,
        histogram: [
          { bucket: '1-2', count: 0 },
          { bucket: '3-4', count: 2 },
          { bucket: '5-6', count: 4 },
          { bucket: '7-8', count: 9 },
          { bucket: '9-10', count: 5 },
        ],
      },
    ],
    log_id: 'log-001',
  },
  {
    id: 'mock-run-2',
    test_id: 'test-002',
    executed_at: '2026-02-27T10:00:00Z',
    panel_size: 10,
    results: [
      {
        subject_id: 'subject-2',
        mean: 5.8,
        median: 6.0,
        std: 1.5,
        histogram: [
          { bucket: '1-2', count: 1 },
          { bucket: '3-4', count: 2 },
          { bucket: '5-6', count: 4 },
          { bucket: '7-8', count: 2 },
          { bucket: '9-10', count: 1 },
        ],
      },
    ],
    log_id: null,
  },
]

export async function listRuns(): Promise<Run[]> {
  await delay()
  return [...FIXTURE_RUNS].reverse()
}

export async function getRun(id: string): Promise<Run> {
  await delay()
  const run = FIXTURE_RUNS.find((r) => r.id === id)
  if (!run) throw new Error(`Run not found: ${id}`)
  return run
}

export async function createRun(testId: string): Promise<Run> {
  await delay()
  const run: Run = {
    id: `run-${Date.now()}`,
    test_id: testId,
    executed_at: new Date().toISOString(),
    panel_size: 10,
    results: [],
    log_id: null,
  }
  FIXTURE_RUNS.push(run)
  return run
}
