'use client';

import * as React from "react"
import { cn } from "@/lib/utils"

interface SelectContextType {
  value: string
  onValueChange: (value: string) => void
  open: boolean
  setOpen: (open: boolean) => void
}

const SelectContext = React.createContext<SelectContextType>({
  value: '',
  onValueChange: () => {},
  open: false,
  setOpen: () => {},
})

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

  const ctxValue = value !== undefined ? value : internalValue
  const ctxOnChange = onValueChange ?? setInternalValue

  return (
    <SelectContext.Provider value={{ value: ctxValue, onValueChange: ctxOnChange, open, setOpen }}>
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
  const { value } = React.useContext(SelectContext)
  return <span>{value || placeholder}</span>
}

export function SelectContent({
  className,
  children,
}: {
  className?: string
  children: React.ReactNode
}) {
  const { open } = React.useContext(SelectContext)
  if (!open) return null

  return (
    <div
      className={cn(
        "absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border bg-popover p-1 shadow-md",
        className
      )}
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
  const { onValueChange, setOpen } = React.useContext(SelectContext)
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
