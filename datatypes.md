"use client"

import type React from "react"
import { forwardRef, useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Send, Smile, Paperclip, Mic, Image, FileText, Plus } from 'lucide-react'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { cn } from "@/lib/utils"

interface InputBarProps {
  onSendMessage: (message: string) => void
  onAttachmentClick?: () => void
  onImageAttach?: () => void
  onDocumentAttach?: () => void
  onAudioRecord?: () => void
  disabled?: boolean
  isLoading?: boolean
  placeholder?: string
  className?: string
}

export const InputBar = forwardRef<HTMLTextAreaElement, InputBarProps>(
  ({ 
    onSendMessage, 
    onAttachmentClick, 
    onImageAttach,
    onDocumentAttach,
    onAudioRecord,
    disabled = false, 
    isLoading = false, 
    placeholder = "Type your message...",
    className 
  }, ref) => {
    const [message, setMessage] = useState("")
    const [isComposing, setIsComposing] = useState(false)
    const [isFocused, setIsFocused] = useState(false)
    const [hasContent, setHasContent] = useState(false)
    const textareaRef = useRef<HTMLTextAreaElement | null>(null)
    const formRef = useRef<HTMLFormElement>(null)

    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault()
      if (message.trim() && !disabled) {
        onSendMessage(message)
        setMessage("")
        
        // Reset height after sending
        if (textareaRef.current) {
          textareaRef.current.style.height = "40px"
        }
      }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey && !isComposing) {
        e.preventDefault()
        handleSubmit(e)
      }
    }

    // Auto-resize textarea as content grows
    useEffect(() => {
      const currentRef = ref && typeof ref !== "function" ? ref.current : textareaRef.current
      if (currentRef) {
        currentRef.style.height = "40px"
        currentRef.style.height = `${Math.min(currentRef.scrollHeight, 150)}px`
      }
      
      setHasContent(message.trim().length > 0)
    }, [message, ref])

    // Focus the textarea when component mounts
    useEffect(() => {
      const timer = setTimeout(() => {
        const currentRef = ref && typeof ref !== "function" ? ref.current : textareaRef.current
        if (currentRef && !disabled) {
          currentRef.focus()
        }
      }, 100)
      
      return () => clearTimeout(timer)
    }, [disabled, ref])

    const handlePaste = (e: React.ClipboardEvent) => {
      // Check if paste contains an image
      const items = e.clipboardData.items
      let hasImage = false
      
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1 && onImageAttach) {
          hasImage = true
          // Handle image paste (you would implement detailed logic here)
          onImageAttach()
          break
        }
      }
      
      // Provide visual feedback for paste if needed
      if (hasImage) {
        e.preventDefault() // Prevent default text paste for images
      }
    }

    return (
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className={cn(
          "border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 p-3 sticky bottom-0 shadow-[0_-2px_10px_rgba(0,0,0,0.05)]",
          className
        )}
      >
        <div className={cn(
          "relative flex items-center gap-2 rounded-2xl border transition-all duration-200",
          isFocused ? "border-blue-500 shadow-[0_0_0_2px_rgba(59,130,246,0.2)]" : "border-input",
          disabled && "opacity-70 cursor-not-allowed",
          hasContent && "pr-2"
        )}>
          {/* Attachment Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-9 w-9 rounded-full text-muted-foreground hover:text-foreground hover:bg-blue-50 transition-colors ml-1"
                disabled={disabled || isLoading}
              >
                <Plus className="h-5 w-5" />
                <span className="sr-only">Add attachment</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" side="top" className="w-48">
              <DropdownMenuItem onClick={onImageAttach} className="flex items-center gap-2 cursor-pointer">
                <Image className="h-4 w-4" />
                <span>Image</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onDocumentAttach} className="flex items-center gap-2 cursor-pointer">
                <FileText className="h-4 w-4" />
                <span>Document</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onAttachmentClick} className="flex items-center gap-2 cursor-pointer">
                <Paperclip className="h-4 w-4" />
                <span>Other files</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Text Input */}
          <div className="relative flex-1">
            <Textarea
              ref={(node) => {
                // Handle both the forwarded ref and the local ref
                if (typeof ref === 'function') {
                  ref(node)
                } else if (ref) {
                  ref.current = node
                }
                textareaRef.current = node
              }}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              onCompositionStart={() => setIsComposing(true)}
              onCompositionEnd={() => setIsComposing(false)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              onPaste={handlePaste}
              placeholder={placeholder}
              className={cn(
                "min-h-[40px] max-h-[150px] w-full resize-none border-0 bg-transparent py-3 px-2",
                "focus-visible:ring-0 focus-visible:ring-offset-0 text-base placeholder:text-muted-foreground",
                "scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent"
              )}
              disabled={disabled || isLoading}
              rows={1}
            />
          </div>

          {/* Emoji Button */}
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="h-9 w-9 rounded-full text-muted-foreground hover:text-foreground hover:bg-blue-50 transition-colors"
                      disabled={disabled || isLoading}
                    >
                      <Smile className="h-5 w-5" />
                      <span className="sr-only">Add emoji</span>
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-64 p-2" align="end" side="top">
                    <div className="grid grid-cols-8 gap-1">
                      {["😊", "👍", "🙏", "❤️", "😂", "🎉", "🤔", "👀", 
                        "✅", "⭐", "🔥", "💯", "👋", "🚀", "💡", "📄",
                        "👏", "💪", "🙌", "🎯", "💰", "⏰", "📱", "💻"].map((emoji) => (
                        <Button
                          key={emoji}
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 rounded-md p-0 hover:bg-blue-50"
                          onClick={() => {
                            setMessage((prev) => prev + emoji)
                            // Focus back on textarea after emoji selection
                            if (textareaRef.current) textareaRef.current.focus()
                          }}
                        >
                          {emoji}
                        </Button>
                      ))}
                    </div>
                  </PopoverContent>
                </Popover>
              </TooltipTrigger>
              <TooltipContent side="top">Add emoji</TooltipContent>
            </Tooltip>
          </TooltipProvider>

          {/* Voice Recording Button */}
          {onAudioRecord && (
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="h-9 w-9 rounded-full text-muted-foreground hover:text-foreground hover:bg-blue-50 transition-colors"
                    disabled={disabled || isLoading}
                    onClick={onAudioRecord}
                  >
                    <Mic className="h-5 w-5" />
                    <span className="sr-only">Voice message</span>
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top">Record voice message</TooltipContent>
              </Tooltip>
            </TooltipProvider>
          )}

          {/* Send Button */}
          <div className={cn(hasContent ? "opacity-100" : "opacity-0", "transition-opacity duration-200 mr-1")}>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    type="submit"
                    size="icon"
                    disabled={!message.trim() || disabled || isLoading}
                    className={cn(
                      "h-9 w-9 rounded-full p-0 transition-all",
                      message.trim() 
                        ? "bg-blue-600 hover:bg-blue-700 text-white" 
                        : "bg-gray-200 text-gray-400"
                    )}
                  >
                    {isLoading ? (
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                    <span className="sr-only">Send message</span>
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top">Send message</TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>
        
        {/* Character counter (optional, appears when approaching limit) */}
        {message.length > 0 && message.length > 200 && (
          <div className="text-xs text-muted-foreground text-right mt-1 pr-2">
            {message.length}/2000
          </div>
        )}
      </form>
    )
  },
)

InputBar.displayName = "InputBar"