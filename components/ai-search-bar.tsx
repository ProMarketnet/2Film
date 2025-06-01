"use client"

import { useState } from "react"
import { Search, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useChat } from "ai/react"

interface AISearchBarProps {
  onResults: (results: any) => void
}

export function AISearchBar({ onResults }: AISearchBarProps) {
  const [searchQuery, setSearchQuery] = useState("")

  const { messages, append, isLoading } = useChat({
    api: "/api/chat",
    onFinish: (message) => {
      // Process AI response and show results
      onResults({
        query: searchQuery,
        response: message.content,
        suggestions: extractSuggestions(message.content),
      })
    },
  })

  const extractSuggestions = (content: string) => {
    // Extract movie/show suggestions from AI response
    const lines = content.split("\n")
    return lines
      .filter((line) => line.includes("•") || line.includes("-") || line.includes("1.") || line.includes("2."))
      .slice(0, 4)
      .map((line) => line.replace(/^[•\-\d.]\s*/, "").trim())
      .filter((line) => line.length > 0)
  }

  const handleAISearch = async () => {
    if (!searchQuery.trim()) return

    await append({
      role: "user",
      content: `Help me find movies or shows: ${searchQuery}. Please provide specific recommendations with brief descriptions.`,
    })
  }

  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
      <Input
        type="text"
        placeholder="Ask AI: 'Find me something like The Matrix' or search titles..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && handleAISearch()}
        className="w-96 pl-10 pr-24 bg-gray-800/50 border-gray-600 text-white placeholder-gray-400 focus:border-teal-400"
        disabled={isLoading}
      />
      <Button
        onClick={handleAISearch}
        disabled={isLoading || !searchQuery.trim()}
        className="absolute right-1 top-1/2 transform -translate-y-1/2 bg-teal-400 text-black hover:bg-teal-500 px-3 py-1 text-sm flex items-center gap-1"
      >
        <Sparkles className="w-3 h-3" />
        {isLoading ? "AI..." : "Ask AI"}
      </Button>
    </div>
  )
}
