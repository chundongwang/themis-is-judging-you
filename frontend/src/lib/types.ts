// Population types
export interface Distribution {
  fn: 'normal' | 'skewed_normal' | 'uniform' | 'weighted'
  mu?: number
  sigma?: number
  min?: number
  max?: number
  weights?: { value: string; weight: number }[]
}

export interface DimensionConfig {
  name: string
  type: 'continuous' | 'categorical'
  distribution: Distribution
}

export interface Population {
  id: string
  name: string
  description: string
  dimensions: DimensionConfig[]
}

// Test types
export interface ScaleConfig {
  min: number
  max: number
  label: string
}

export interface Subject {
  id: string
  text: string
  image: string | null
}

export interface Test {
  id: string
  name: string
  created_at: string
  prompt_template: string
  scale: ScaleConfig
  population_id: string
  panel_size: number
  subjects: Subject[]
}

// Judge types
export interface JudgeProfile {
  id: string
  population_id: string
  dimensions: Record<string, string | number>
}

// Run types
export interface SubjectResult {
  subject_id: string
  mean: number
  median: number
  std: number
  histogram: { bucket: string; count: number }[]
}

export interface Run {
  id: string
  test_id: string
  executed_at: string
  panel_size: number
  results: SubjectResult[]
  log_id: string | null
}

// Judge result (from SSE stream)
export interface JudgeResult {
  judge: Record<string, string | number>
  score: number
  reason: string
}

// SSE event types
export interface SSEProgressEvent {
  completed: number
  total: number
  pct: number
}

export interface SSECompleteEvent {
  mean: number
  median: number
  std: number
  histogram: { bucket: string; count: number }[]
}
