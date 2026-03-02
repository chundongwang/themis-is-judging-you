interface HistogramChartProps {
  data: { bucket: string; count: number }[]
}

export function HistogramChart({ data }: HistogramChartProps) {
  const maxCount = Math.max(...data.map((d) => d.count), 1)

  return (
    <div className="flex items-end gap-1 h-24">
      {data.map((d) => {
        const heightPct = (d.count / maxCount) * 100
        return (
          <div key={d.bucket} className="flex flex-col items-center flex-1 gap-1">
            <span className="text-xs text-muted-foreground">{d.count}</span>
            <div
              className="w-full bg-primary/70 rounded-t transition-all"
              style={{ height: `${heightPct}%`, minHeight: d.count > 0 ? '4px' : '0' }}
            />
            <span className="text-xs text-muted-foreground whitespace-nowrap">{d.bucket}</span>
          </div>
        )
      })}
    </div>
  )
}
