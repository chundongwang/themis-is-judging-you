import { Link } from 'react-router-dom'
import { Badge } from '@/components/ui/badge'
import { formatDate, formatScore } from '@/lib/utils'
import type { Run } from '@/lib/types'

interface RunListItemProps {
  run: Run
}

export function RunListItem({ run }: RunListItemProps) {
  const firstResult = run.results?.[0]

  return (
    <tr className="border-b hover:bg-muted/50 transition-colors">
      <td className="py-3 px-4 text-sm font-mono text-muted-foreground">{run.id.slice(0, 12)}…</td>
      <td className="py-3 px-4 text-sm">{run.test_id}</td>
      <td className="py-3 px-4 text-sm">{formatDate(run.executed_at)}</td>
      <td className="py-3 px-4 text-sm">
        <Badge variant="secondary">{run.panel_size} judges</Badge>
      </td>
      <td className="py-3 px-4 text-sm font-semibold">
        {firstResult ? formatScore(firstResult.mean) : '—'}
      </td>
      <td className="py-3 px-4">
        <Link
          to={`/results/${run.id}`}
          className="text-sm text-primary hover:underline"
        >
          View →
        </Link>
      </td>
    </tr>
  )
}
