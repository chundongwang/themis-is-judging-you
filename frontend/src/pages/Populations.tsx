import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { PopulationCard } from '@/components/PopulationCard'
import { listPopulations, createPopulation, deletePopulation } from '@/api/populations'
import type { Population } from '@/lib/types'

export function Populations() {
  const [populations, setPopulations] = useState<Population[]>([])
  const [editTarget, setEditTarget] = useState<Population | null>(null)
  const [deleteTarget, setDeleteTarget] = useState<Population | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [newName, setNewName] = useState('')
  const [newDesc, setNewDesc] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    listPopulations().then(setPopulations)
  }, [])

  function openCreate() {
    setEditTarget(null)
    setNewName('')
    setNewDesc('')
    setDialogOpen(true)
  }

  function openEdit(pop: Population) {
    setEditTarget(pop)
    setNewName(pop.name)
    setNewDesc(pop.description)
    setDialogOpen(true)
  }

  async function handleSave() {
    if (!newName.trim()) return
    setSaving(true)
    try {
      if (editTarget) {
        // Update is mocked — just reload list
        setPopulations((prev) =>
          prev.map((p) =>
            p.id === editTarget.id ? { ...p, name: newName, description: newDesc } : p
          )
        )
      } else {
        const pop = await createPopulation({ name: newName, description: newDesc, dimensions: [] })
        setPopulations((prev) => [...prev, pop])
      }
      setDialogOpen(false)
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return
    await deletePopulation(deleteTarget.id)
    setPopulations((prev) => prev.filter((p) => p.id !== deleteTarget.id))
    setDeleteTarget(null)
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Populations</h2>
        <Button onClick={openCreate}>+ New population</Button>
      </div>

      <div className="space-y-4">
        {populations.map((pop) => (
          <PopulationCard
            key={pop.id}
            population={pop}
            onEdit={openEdit}
            onDelete={setDeleteTarget}
          />
        ))}
        {populations.length === 0 && (
          <p className="text-muted-foreground text-sm">No populations yet.</p>
        )}
      </div>

      {/* Create / Edit dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editTarget ? 'Edit population' : 'New population'}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-1.5">
              <Label htmlFor="pop-name">Name</Label>
              <Input
                id="pop-name"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="e.g. United States General Public"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="pop-desc">Description</Label>
              <Input
                id="pop-desc"
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
                placeholder="Short description…"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSave} disabled={saving || !newName.trim()}>
              {saving ? 'Saving…' : 'Save'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirmation */}
      <AlertDialog open={!!deleteTarget} onOpenChange={(open) => !open && setDeleteTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete "{deleteTarget?.name}"?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. Any tests using this population will be affected.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
