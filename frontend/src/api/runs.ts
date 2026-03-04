import type { Run } from '@/lib/types'
import { apiFetch } from './client'

export async function listRuns(): Promise<Run[]> {
  return apiFetch<Run[]>('/api/runs')
}

export async function getRun(id: string): Promise<Run> {
  return apiFetch<Run>(`/api/runs/${id}`)
}

export async function createRun(
  populationId: string,
  panelSize: number,
  subjectImage: string | null = null,
): Promise<Run> {
  return apiFetch<Run>('/api/runs/quick', {
    method: 'POST',
    body: JSON.stringify({
      population_id: populationId,
      panel_size: panelSize,
      subject_image: subjectImage,
    }),
  })
}

export async function getRunLog(id: string): Promise<{ entries: import('@/lib/types').JudgeResult[] }> {
  return apiFetch(`/api/runs/${id}/log`)
}

export async function deleteRun(id: string): Promise<void> {
  await apiFetch<void>(`/api/runs/${id}`, { method: 'DELETE' })
}
