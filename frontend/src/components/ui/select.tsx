'use client';

import * as React from "react"
import { cn } from "@/lib/utils"

interface SelectContextType {
  value: string
  onValueChange: (value: string) => void
  open: boolean
  setOpen: (open: boolean) => void
  selectedLabel: string
  registerLabel: (val: string, label: string) => void
}

const SelectContext = React.createContext<SelectContextType>({
  value: '',
  onValueChange: () => {},
  open: false,
  setOpen: () => {},
  selectedLabel: '',
  registerLabel: () => {},
})

function getDisplayText(children: React.ReactNode): string {
  let text = ''
  React.Children.forEach(children, (child) => {
    if (typeof child === 'string' || typeof child === 'number') {
      text += String(child)
    }
  })
  return text
}

export function Select({
  value,
  onValueChange,
  children,
}: {
  value?: string
  onValueChange: (value: string) => void
  children: React.ReactNode
}) {
  const [open, setOpen] = React.useState(false)
  const [internalValue, setInternalValue] = React.useState('')
  const [labelMap, setLabelMap] = React.useState<Record<string, string>>({})

  const ctxValue = value !== undefined ? value : internalValue
  const ctxOnChange = onValueChange ?? setInternalValue
  const selectedLabel = labelMap[ctxValue] || ''

  const registerLabel = React.useCallback((val: string, label: string) => {
    setLabelMap(prev => ({ ...prev, [val]: label }))
  }, [])

  return (
    <SelectContext.Provider value={{ value: ctxValue, onValueChange: ctxOnChange, open, setOpen, selectedLabel, registerLabel }}>
      {children}
    </SelectContext.Provider>
  )
}

export function SelectTrigger({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { setOpen } = React.useContext(SelectContext)
  return (
    <button
      className={cn(
        "flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
        className
      )}
      onClick={() => setOpen(true)}
      {...props}
    >
      {children}
    </button>
  )
}

export function SelectValue({
  placeholder,
}: {
  placeholder?: string
}) {
  const { selectedLabel } = React.useContext(SelectContext)
  return <span>{selectedLabel || placeholder}</span>
}

export function SelectContent({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  const { open } = React.useContext(SelectContext)
  return (
    <div
      className={cn(
        "absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border bg-popover p-1 shadow-md",
        !open && "hidden",
        className,
      )}
      style={{ display: open ? undefined : 'none' }}
    >
      {children}
    </div>
  )
}

export function SelectItem({
  className,
  children,
  value,
  ...props
}: React.LiHTMLAttributes<HTMLLIElement> & { value: string }) {
  const { onValueChange, setOpen, registerLabel } = React.useContext(SelectContext)

  React.useEffect(() => {
    registerLabel(value, getDisplayText(children))
  }, [value, children, registerLabel])

  return (
    <li
      className={cn(
        "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 hover:bg-accent",
        className
      )}
      onClick={() => {
        onValueChange(value)
        setOpen(false)
      }}
      {...props}
    >
      {children}
    </li>
  )
}
