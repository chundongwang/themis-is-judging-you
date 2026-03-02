import type { Run } from '@/lib/types'
import { apiFetch } from './client'

export async function listRuns(): Promise<Run[]> {
  return apiFetch<Run[]>('/api/runs')
}

export async function getRun(id: string): Promise<Run> {
  return apiFetch<Run>(`/api/runs/${id}`)
}

export async function createRun(testId: string): Promise<Run> {
  return apiFetch<Run>('/api/runs', {
    method: 'POST',
    body: JSON.stringify({ test_id: testId }),
  })
}

export async function deleteRun(id: string): Promise<void> {
  await apiFetch<void>(`/api/runs/${id}`, { method: 'DELETE' })
}
