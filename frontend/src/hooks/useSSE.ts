import { useEffect, useRef, useState } from 'react'
import type { JudgeResult, SSECompleteEvent, SSEProgressEvent } from '@/lib/types'

type SSEStatus = 'idle' | 'connecting' | 'streaming' | 'complete' | 'error'

interface SSEState {
  judgeResults: JudgeResult[]
  progress: SSEProgressEvent | null
  finalStats: SSECompleteEvent | null
  status: SSEStatus
  error: string | null
}

export function useSSE(runId: string | null): SSEState {
  const [state, setState] = useState<SSEState>({
    judgeResults: [],
    progress: null,
    finalStats: null,
    status: 'idle',
    error: null,
  })

  const esRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (!runId) return

    setState({
      judgeResults: [],
      progress: null,
      finalStats: null,
      status: 'connecting',
      error: null,
    })

    const es = new EventSource(`/api/runs/${runId}/stream`)
    esRef.current = es

    es.addEventListener('progress', (e) => {
      const data = JSON.parse(e.data) as SSEProgressEvent
      setState((prev) => ({ ...prev, status: 'streaming', progress: data }))
    })

    es.addEventListener('judge_result', (e) => {
      const data = JSON.parse(e.data) as JudgeResult
      setState((prev) => ({
        ...prev,
        status: 'streaming',
        judgeResults: [...prev.judgeResults, data],
      }))
    })

    es.addEventListener('complete', (e) => {
      const data = JSON.parse(e.data) as SSECompleteEvent
      setState((prev) => ({ ...prev, status: 'complete', finalStats: data }))
      es.close()
    })

    es.onerror = () => {
      setState((prev) => ({
        ...prev,
        status: 'error',
        error: 'Connection lost. Try refreshing.',
      }))
      es.close()
    }

    return () => {
      es.close()
    }
  }, [runId])

  return state
}
