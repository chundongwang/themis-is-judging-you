import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import type { Population } from '@/lib/types'

interface PopulationCardProps {
  population: Population
  onEdit: (pop: Population) => void
  onDelete: (pop: Population) => void
}

export function PopulationCard({ population, onEdit, onDelete }: PopulationCardProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-base">{population.name}</CardTitle>
            <CardDescription className="mt-1">{population.description}</CardDescription>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => onEdit(population)}>
              Edit
            </Button>
            <Button variant="destructive" size="sm" onClick={() => onDelete(population)}>
              Delete
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-1.5">
          {population.dimensions.map((dim) => (
            <Badge key={dim.name} variant="outline" className="text-xs">
              {dim.name} · {dim.type}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
