import { useEffect, useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { Progress } from '@/components/ui/progress'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { JudgeCard } from '@/components/JudgeCard'
import { ScoreStats } from '@/components/ScoreStats'
import { HistogramChart } from '@/components/HistogramChart'
import { useSSE } from '@/hooks/useSSE'
import { getRun } from '@/api/runs'
import { formatPct } from '@/lib/utils'
import type { Run } from '@/lib/types'

export function Results() {
  const { runId } = useParams<{ runId: string }>()
  const { state } = useLocation()
  const isLive = (state as { live?: boolean } | null)?.live === true

  // Live mode: use SSE
  const sse = useSSE(isLive ? (runId ?? null) : null)

  // Replay mode: load from API
  const [run, setRun] = useState<Run | null>(null)
  const [replayError, setReplayError] = useState<string | null>(null)

  useEffect(() => {
    if (!isLive && runId) {
      getRun(runId)
        .then(setRun)
        .catch((e: Error) => setReplayError(e.message))
    }
  }, [isLive, runId])

  if (!runId) return <p className="text-muted-foreground">No run ID provided.</p>

  // Derive display values from live or replay mode
  const finalStats = isLive
    ? sse.finalStats
    : run?.results[0]
      ? { mean: run.results[0].mean, median: run.results[0].median, std: run.results[0].std, histogram: run.results[0].histogram }
      : null

  const progressPct = isLive ? (sse.progress?.pct ?? 0) : 100
  const isComplete = isLive ? sse.status === 'complete' : run !== null

  if (replayError) {
    return <p className="text-destructive">Error loading run: {replayError}</p>
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Results</h2>
          <p className="text-sm text-muted-foreground font-mono">{runId}</p>
        </div>
        {isLive && !isComplete && (
          <span className="text-sm text-muted-foreground animate-pulse">Live ●</span>
        )}
      </div>

      {/* Progress bar (live only) */}
      {isLive && !isComplete && (
        <div className="space-y-1">
          <Progress value={progressPct} />
          <p className="text-xs text-muted-foreground text-right">{formatPct(progressPct)} complete</p>
        </div>
      )}

      <Tabs defaultValue="feed">
        <TabsList>
          <TabsTrigger value="feed">Judge Feed</TabsTrigger>
          <TabsTrigger value="summary" disabled={!isComplete}>
            Summary
          </TabsTrigger>
        </TabsList>

        <TabsContent value="feed">
          <ScrollArea className="h-[60vh] pr-2">
            {isLive ? (
              sse.judgeResults.length === 0 ? (
                <p className="text-muted-foreground text-sm mt-4">
                  {sse.status === 'connecting' ? 'Connecting…' : 'Waiting for judges…'}
                </p>
              ) : (
                sse.judgeResults.map((r, i) => <JudgeCard key={i} result={r} />)
              )
            ) : (
              <p className="text-muted-foreground text-sm mt-4">
                Individual judge results not available in replay mode.
              </p>
            )}
            {sse.error && <p className="text-destructive text-sm mt-2">{sse.error}</p>}
          </ScrollArea>
        </TabsContent>

        <TabsContent value="summary">
          {finalStats && (
            <div className="space-y-6 mt-2">
              <ScoreStats mean={finalStats.mean} median={finalStats.median} std={finalStats.std} />
              <div>
                <p className="text-sm font-medium mb-3">Score distribution</p>
                <HistogramChart data={finalStats.histogram} />
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
