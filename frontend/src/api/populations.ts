import type { Population } from '@/lib/types'
import { delay } from './client'

const FIXTURE_POPULATIONS: Population[] = [
  {
    id: 'us-general',
    name: 'United States General Public',
    description: 'Broad US demographic sample across age, gender, income, and region.',
    dimensions: [
      {
        name: 'age',
        type: 'continuous',
        distribution: { fn: 'normal', mu: 38, sigma: 15, min: 18, max: 80 },
      },
      {
        name: 'gender',
        type: 'categorical',
        distribution: {
          fn: 'weighted',
          weights: [
            { value: 'Male', weight: 0.49 },
            { value: 'Female', weight: 0.49 },
            { value: 'Non-binary', weight: 0.02 },
          ],
        },
      },
      {
        name: 'occupation',
        type: 'categorical',
        distribution: {
          fn: 'weighted',
          weights: [
            { value: 'Professional', weight: 0.3 },
            { value: 'Creative', weight: 0.2 },
            { value: 'Trades', weight: 0.2 },
            { value: 'Student', weight: 0.15 },
            { value: 'Retired', weight: 0.15 },
          ],
        },
      },
    ],
  },
  {
    id: 'cn-mainland',
    name: 'China Mainland Urban',
    description: 'Urban Chinese demographic sample skewed toward younger professionals.',
    dimensions: [
      {
        name: 'age',
        type: 'continuous',
        distribution: { fn: 'normal', mu: 29, sigma: 8, min: 18, max: 60 },
      },
      {
        name: 'gender',
        type: 'categorical',
        distribution: {
          fn: 'weighted',
          weights: [
            { value: 'Male', weight: 0.51 },
            { value: 'Female', weight: 0.49 },
          ],
        },
      },
    ],
  },
]

export async function listPopulations(): Promise<Population[]> {
  await delay()
  return FIXTURE_POPULATIONS
}

export async function getPopulation(id: string): Promise<Population> {
  await delay()
  const pop = FIXTURE_POPULATIONS.find((p) => p.id === id)
  if (!pop) throw new Error(`Population not found: ${id}`)
  return pop
}

export async function createPopulation(data: Omit<Population, 'id'>): Promise<Population> {
  await delay()
  const pop: Population = { id: `pop-${Date.now()}`, ...data }
  FIXTURE_POPULATIONS.push(pop)
  return pop
}

export async function updatePopulation(id: string, data: Partial<Population>): Promise<Population> {
  await delay()
  const idx = FIXTURE_POPULATIONS.findIndex((p) => p.id === id)
  if (idx === -1) throw new Error(`Population not found: ${id}`)
  FIXTURE_POPULATIONS[idx] = { ...FIXTURE_POPULATIONS[idx], ...data }
  return FIXTURE_POPULATIONS[idx]
}

export async function deletePopulation(id: string): Promise<void> {
  await delay()
  const idx = FIXTURE_POPULATIONS.findIndex((p) => p.id === id)
  if (idx !== -1) FIXTURE_POPULATIONS.splice(idx, 1)
}
