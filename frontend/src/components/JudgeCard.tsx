import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import type { JudgeResult } from '@/lib/types'

interface JudgeCardProps {
  result: JudgeResult
}

export function JudgeCard({ result }: JudgeCardProps) {
  const { judge, score, reason } = result

  return (
    <Card className="mb-3">
      <CardContent className="pt-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex flex-wrap gap-1.5 mb-2">
              {Object.entries(judge).map(([key, val]) => (
                <Badge key={key} variant="secondary" className="text-xs">
                  {key}: {val}
                </Badge>
              ))}
            </div>
            <p className="text-sm text-muted-foreground italic">"{reason}"</p>
          </div>
          <div className="shrink-0 text-right">
            <span className="text-3xl font-bold text-primary">{score}</span>
            <span className="text-sm text-muted-foreground">/10</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
