"use client"

import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { MovieCard } from "./movie-card"
import { useRef } from "react"

interface ContentSectionProps {
  title: string
  movies: Array<{
    title: string
    year: string
    rating: number
    genre: string
    description: string
    imageUrl: string
    streamingServices: string[]
  }>
  showSeeAll?: boolean
}

export function ContentSection({ title, movies, showSeeAll = true }: ContentSectionProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const scrollAmount = 400
      scrollRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      })
    }
  }

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white">{title}</h2>
        {showSeeAll && (
          <Button variant="ghost" className="text-sm text-teal-400 hover:text-teal-300 hover:bg-transparent">
            See All
          </Button>
        )}
      </div>

      <div className="relative group">
        {/* Navigation Arrows */}
        <Button
          onClick={() => scroll("left")}
          className="absolute -left-4 top-1/2 transform -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 rounded-full p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          size="sm"
        >
          <ChevronLeft className="w-5 h-5 text-white" />
        </Button>

        {/* Horizontal Scrolling Container */}
        <div
          ref={scrollRef}
          className="flex space-x-4 overflow-x-auto pb-4 scrollbar-hide scroll-smooth"
          style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
        >
          {movies.map((movie, index) => (
            <MovieCard key={index} {...movie} isHorizontal={true} />
          ))}
        </div>

        <Button
          onClick={() => scroll("right")}
          className="absolute -right-4 top-1/2 transform -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 rounded-full p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          size="sm"
        >
          <ChevronRight className="w-5 h-5 text-white" />
        </Button>
      </div>
    </div>
  )
}
