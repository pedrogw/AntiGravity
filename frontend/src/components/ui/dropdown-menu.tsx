'use client';

import * as React from "react"
import { cn } from "@/lib/utils"

export function DropdownMenu({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(false)
  const ref = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div ref={ref} className="relative inline-block text-left">
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child) && child.type === DropdownMenuContent) {
          return open ? child : null
        }
        if (React.isValidElement(child) && child.type === DropdownMenuTrigger) {
          return React.cloneElement(child as React.ReactElement<{ onClick?: () => void }>, {
            onClick: () => setOpen(!open),
          })
        }
        return child
      })}
    </div>
  )
}

export function DropdownMenuTrigger({
  children,
  className,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button className={cn("", className)} {...props}>
      {children}
    </button>
  )
}

export function DropdownMenuContent({
  children,
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "absolute right-0 z-50 mt-1 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 shadow-md",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function DropdownMenuItem({
  children,
  className,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "relative flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 hover:bg-accent",
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

export function DropdownMenuSeparator({
  className,
}: {
  className?: string
}) {
  return <div className={cn("-mx-1 my-1 h-px bg-muted", className)} />
}

export function DropdownMenuLabel({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn("px-2 py-1.5 text-sm font-semibold", className)}>
      {children}
    </div>
  )
}
