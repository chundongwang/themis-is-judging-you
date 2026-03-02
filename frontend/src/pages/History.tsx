import { useEffect, useState } from 'react'
import { listRuns } from '@/api/runs'
import { RunListItem } from '@/components/RunListItem'
import type { Run } from '@/lib/types'

export function History() {
  const [runs, setRuns] = useState<Run[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listRuns()
      .then(setRuns)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold">Run History</h2>

      {loading ? (
        <p className="text-muted-foreground text-sm">Loading…</p>
      ) : runs.length === 0 ? (
        <p className="text-muted-foreground text-sm">No runs yet.</p>
      ) : (
        <div className="rounded-lg border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-muted/50">
              <tr>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Run ID</th>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Test</th>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Date</th>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Panel</th>
                <th className="text-left py-3 px-4 font-medium text-muted-foreground">Mean</th>
                <th className="py-3 px-4" />
              </tr>
            </thead>
            <tbody>
              {runs.map((run) => (
                <RunListItem key={run.id} run={run} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
