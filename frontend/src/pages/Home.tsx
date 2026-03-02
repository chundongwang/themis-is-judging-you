import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { listPopulations } from '@/api/populations'
import { createRun } from '@/api/runs'
import type { Population } from '@/lib/types'

export function Home() {
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [populations, setPopulations] = useState<Population[]>([])
  const [selectedPopulation, setSelectedPopulation] = useState('')
  const [panelSize, setPanelSize] = useState('20')
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    listPopulations().then(setPopulations)
  }, [])

  function handleFile(f: File) {
    setFile(f)
    const url = URL.createObjectURL(f)
    setPreview(url)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!selectedPopulation) return
    setLoading(true)
    try {
      const run = await createRun('test-001')
      navigate(`/results/${run.id}`, { state: { live: true } })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold tracking-tight mb-3">
          Country Simulator
        </h1>
        <p className="text-muted-foreground text-lg">
          Get your photo rated by a synthetic panel of judges drawn from any demographic population.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Upload zone */}
        <div
          className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
            isDragging ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
          }`}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {preview ? (
            <div className="flex flex-col items-center gap-3">
              <img src={preview} alt="preview" className="max-h-48 rounded-lg object-cover" />
              <p className="text-sm text-muted-foreground">{file?.name}</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="text-4xl">📸</div>
              <p className="font-medium">Drop a photo here</p>
              <p className="text-sm text-muted-foreground">or click to browse — JPG, PNG, WEBP</p>
            </div>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />
        </div>

        {/* Population select */}
        <div className="space-y-2">
          <Label htmlFor="population">Judge population</Label>
          <Select value={selectedPopulation} onValueChange={setSelectedPopulation}>
            <SelectTrigger id="population">
              <SelectValue placeholder="Select a population…" />
            </SelectTrigger>
            <SelectContent>
              {populations.map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  {p.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Panel size */}
        <div className="space-y-2">
          <Label htmlFor="panel-size">Panel size (number of judges)</Label>
          <Input
            id="panel-size"
            type="number"
            min={1}
            max={500}
            value={panelSize}
            onChange={(e) => setPanelSize(e.target.value)}
          />
        </div>

        <Button
          type="submit"
          size="lg"
          className="w-full"
          disabled={loading || !selectedPopulation}
        >
          {loading ? 'Starting run…' : 'Rate my photo ✨'}
        </Button>
      </form>
    </div>
  )
}
