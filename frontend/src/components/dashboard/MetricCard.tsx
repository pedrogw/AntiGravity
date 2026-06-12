import { Card, CardContent } from '@/components/ui/card'

interface Props {
  title: string
  value: string | number
  description?: string
}

export function MetricCard({ title, value, description }: Props) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="text-sm font-medium text-muted-foreground">{title}</div>
        <div className="mt-2 text-3xl font-bold">{value}</div>
        {description && (
          <div className="mt-1 text-xs text-muted-foreground">{description}</div>
        )}
      </CardContent>
    </Card>
  )
}
