import { formatScore } from '@/lib/utils'

interface ScoreStatsProps {
  mean: number
  median: number
  std: number
}

export function ScoreStats({ mean, median, std }: ScoreStatsProps) {
  const stats = [
    { label: 'Mean', value: formatScore(mean) },
    { label: 'Median', value: formatScore(median) },
    { label: 'Std Dev', value: formatScore(std) },
  ]

  return (
    <div className="grid grid-cols-3 gap-4 text-center">
      {stats.map(({ label, value }) => (
        <div key={label} className="bg-muted rounded-lg p-4">
          <p className="text-2xl font-bold text-primary">{value}</p>
          <p className="text-xs text-muted-foreground mt-1">{label}</p>
        </div>
      ))}
    </div>
  )
}
